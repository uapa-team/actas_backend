import json
import datetime
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from django.http import JsonResponse
from .models import Request, get_fields
from .helpers import QuerySetEncoder
from .writter import UnifiedWritter
from .cases import *  # pylint: disable=wildcard-import,unused-wildcard-import


@api_view(["GET"])
@permission_classes((AllowAny,))
def check(request):
    return JsonResponse({"Ok?": "Ok!"}, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    if username is None or password is None:
        return JsonResponse({'error': 'Contraseña o usuario vacío o nulo.'},
                            status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Error en ActasDB, usuario sin permisos en la aplicación.'},
                            status=HTTP_403_FORBIDDEN)
    user = LDAPBackend().authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({'error': 'Error en LDAP, contraseña o usuario no válido.'},
                            status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': token.key},
                        status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def programs_defined(_):
    return JsonResponse(Request.get_programs(), status=HTTP_200_OK)


@api_view(["GET"])
def info_cases(request):
    print(request.GET.get('cls'))
    if request.GET.get('cls') == '' or request.GET.get('cls') is None:
        return JsonResponse(Request.get_cases(), status=HTTP_200_OK)
    else:
        for type_case in Request.get_subclasses():
            if type_case.__name__ == request.GET.get('cls'):
                return JsonResponse(get_fields(type_case()))
        return JsonResponse({'response': 'Not found'}, status=HTTP_404_NOT_FOUND)


@api_view(["GET", "PATCH", "POST"])
def case(request):
    if request.method == 'GET':
        responses = Request.get_cases_by_query(request.GET.dict())
        return JsonResponse(responses, safe=False, encoder=QuerySetEncoder)
    if request.method == 'POST':
        body = json.loads(request.body)
        subs = [c.__name__ for c in Request.get_subclasses()]
        errors = []
        inserted_items = []
        for item_request in body['items']:
            item_request['user'] = str(request.user)
            case = Request.get_subclasses()[subs.index(item_request['_cls'])]
            item_request['_cls'] = case.get_entire_name()
            new_request = case().from_json(case.translate(json.dumps(item_request)))
            try:
                inserted_items += [new_request.save()]
            except ValidationError as e:
                errors += [e.message]
        return JsonResponse({'inserted_items': inserted_items, 'errors': errors},
                            status=HTTP_200_OK, encoder=QuerySetEncoder, safe=False)
    if request.method == 'PATCH':
        body = json.loads(request.body)
        subs = [c.__name__ for c in Request.get_subclasses()]
        errors = []
        edited_items = []
        not_found = []
        for item_request in body['items']:
            try:
                Request.get_case_by_id(item_request['_id'])
            except ValueError:
                not_found += [item_request['_id']]
                continue
            except KeyError:
                not_found += [item_request['_id']]
                continue
            item_request['user'] = request.user
            item_request['_id'] = item_request['_id']
            case = Request.get_subclasses()[subs.index(item_request['_cls'])]
            item_request['_cls'] = case.get_entire_name()
            new_request = case().from_json(case.translate(
                json.dumps(item_request)), True)
            try:
                new_request.save()
            except ValidationError as e:
                errors += [e.message]
            else:
                edited_items += [new_request]
        return JsonResponse({'edited_items': edited_items,
                             'errors': errors, 'not_found': not_found},
                            status=HTTP_400_BAD_REQUEST if edited_items == [] else HTTP_200_OK,
                            encoder=QuerySetEncoder, safe=False)


@api_view(["GET"])
def get_docx_genid(request):
    caseid = request.GET.get('caseid')
    pre = request.GET.get('pre') == 'true'
    generator = UnifiedWritter()
    try:
        generator.generate_case_example_by_id(caseid, pre)
    except KeyError:
        return HttpResponse('Not found :c', status=404)
    return HttpResponse(generator.filename)


@api_view(["GET"])
def get_docx_gencode(request, bycode):
    caseid = request.GET.get('caseid')
    pre = request.GET.get('pre') == 'true'
    if bycode == '':
        raise NotImplementedError
    elif bycode == '':
        raise NotImplementedError
    else:
        raise NotImplementedError

    generator = UnifiedWritter()
    try:
        generator.generate_case_example_by_id(caseid, pre)
    except KeyError:
        return HttpResponse('Not found :c', status=404)
    return HttpResponse(generator.filename)


@api_view(["GET", "POST"])
def docx_gen_by_date(request):
    try:
        body = json.loads(request.body)
        start_date = body['cm']['start_date']
        end_date = body['cm']['end_date']
    except json.decoder.JSONDecodeError:
        return HttpResponse("Bad Request", status=400)
    filename = 'public/acta' + \
        start_date.split(':')[0] + '_' + end_date.split(':')[0] + '.docx'
    generator = CouncilMinuteGenerator()
    try:
        generator.add_cases_from_date(start_date, end_date)
    except IndexError:
        return HttpResponse('No cases in date range specified', status=401)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["GET", "POST"])
def docx_gen_by_number(request):
    try:
        body = json.loads(request.body)
        consecutive_minute = body['consecutive_minute']
        year = body['year']
    except json.decoder.JSONDecodeError:
        return HttpResponse("Bad Request", status=400)
    filename = 'public/acta' + \
        year + '_' + consecutive_minute + '.docx'
    generator = CouncilMinuteGenerator()
    try:
        generator.add_case_from_year_and_council_number(
            consecutive_minute, year)
    except IndexError:
        return HttpResponse('No cases with specified number and year', status=401)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["GET", "POST"])
def docx_gen_pre_by_number(request):
    try:
        body = json.loads(request.body)
        consecutive_minute = body['consecutive_minute']
        year = body['year']
    except json.decoder.JSONDecodeError:
        return HttpResponse("Bad Request", status=400)
    filename = 'public/preacta' + \
        year + '_' + consecutive_minute + '.docx'
    generator = PreCouncilMinuteGenerator()
    try:
        generator.add_case_from_year_and_council_number(
            consecutive_minute, year)
    except IndexError:
        return HttpResponse('No cases with specified number and year', status=401)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["GET", "POST"])
def docx_gen_with_array(request):
    try:
        body = json.loads(request.body)
        array = body['array']
    except json.decoder.JSONDecodeError:
        return HttpResponse("Bad Request", status=400)
    filename = 'public/acta' + \
        str(datetime.date.today()) + '.docx'
    generator = CouncilMinuteGenerator()
    try:
        generator.add_cases_from_array(array)
    except IndexError:
        return HttpResponse('Empty list', status=400)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["GET", "POST"])
def docx_gen_pre_by_id(request, cm_id):
    filename = 'public/preacta' + cm_id + '.docx'
    try:
        # pylint: disable=no-member
        request_by_id = Request.objects.get(id=cm_id)
    except mongoengine.DoesNotExist:
        return HttpResponse('Does not exist', status=404)
    generator = PreCouncilMinuteGenerator()
    generator.add_case_from_request(request_by_id)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["GET", "POST"])
def docx_gen_pre_by_date(request):
    try:
        body = json.loads(request.body)
        start_date = body['cm']['start_date']
        end_date = body['cm']['end_date']
    except json.decoder.JSONDecodeError:
        return HttpResponse("Bad Request", status=400)
    filename = 'public/preacta' + \
        start_date.split(':')[0] + '_' + end_date.split(':')[0] + '.docx'
    generator = PreCouncilMinuteGenerator()
    try:
        generator.add_cases_from_date(start_date, end_date)
    except IndexError:
        return HttpResponse('No cases in date range specified', status=401)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["POST"])
def docx_gen_pre_with_array(request):
    try:
        body = json.loads(request.body)
        array = body['array']
    except json.decoder.JSONDecodeError:
        return HttpResponse("Bad Request", status=400)
    filename = 'public/preacta' + \
        str(datetime.date.today()) + '.docx'
    generator = PreCouncilMinuteGenerator()
    try:
        generator.add_cases_from_array(array)
    except IndexError:
        return HttpResponse('Empty list', status=400)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["GET"])
@permission_classes((AllowAny,))
def allow_generate(request):
    if request.user == 'acica_fibog':
        return JsonResponse({'allowed_to_generate': [
            {'ALL': 'Generar todas las solicitudes estudiantiles'},
            {'ARC_CIAG': 'Generar las solicitudes del Área Curricular de' +
             ' Ingeniería Civil y Agrícola'},
            {'PRE_CIVI': 'Generar las solicitudes del pregrado en Ingeniería Civil'},
            {'PRE_AGRI': 'Generar las solicitudes del pregrado en Ingeniería Agrícola'},
            {'POS_ARCA': 'Generar las solicitudes de posgrados pertenecientes' +
             ' al Área curricular de Ingeniería Civil y Agrícola'},
        ]},
            status=HTTP_200_OK,
            safe=False)
    elif request.user == 'acimm_fibog':
        return JsonResponse({'allowed_to_generate': [
            {'ALL': 'Generar todas las solicitudes estudiantiles'},
            {'ARC_MEME': 'Generar las solicitudes del Área Curricular de' +
             ' Ingeniería Mecánica y Mecatrónica'},
            {'PRE_MECA': 'Generar las solicitudes del pregrado en Ingeniería Mecánica'},
            {'PRE_METR': 'Generar las solicitudes del pregrado en Ingeniería Mecatrónica'},
            {'POS_ARMM': 'Generar las solicitudes de posgrados pertenecientes' +
             ' al Área curricular de Ingeniería Mecánica y Mecatrónica'},
        ]},
            status=HTTP_200_OK,
            safe=False)
    elif request.user == 'aciee_fibog':
        return JsonResponse({'allowed_to_generate': [
            {'ALL': 'Generar todas las solicitudes estudiantiles'},
            {'ARC_ELEL': 'Generar las solicitudes del Área Curricular de' +
             ' Ingeniería Eléctrica y Electrónica'},
            {'PRE_ELCT': 'Generar las solicitudes del pregrado en Ingeniería Eléctrica'},
            {'PRE_ETRN': 'Generar las solicitudes del pregrado en Ingeniería Electrónica'},
            {'POS_AREE': 'Generar las solicitudes de posgrados pertenecientes' +
             ' al Área curricular de Ingeniería Eléctrica y Electrónica'},
        ]},
            status=HTTP_200_OK,
            safe=False)
    elif request.user == 'aciqa_fibog':
        return JsonResponse({'allowed_to_generate': [
            {'ALL': 'Generar todas las solicitudes estudiantiles'},
            {'ARC_QIAM': 'Generar las solicitudes del Área Curricular de' +
             ' Ingeniería Química y Ambiental'},
            {'PRE_QUIM': 'Generar las solicitudes del pregrado en Ingeniería Química'},
            {'POS_ARQA': 'Generar las solicitudes de posgrados pertenecientes' +
             ' al Área curricular de Ingeniería Química y Ambiental'},
        ]},
            status=HTTP_200_OK,
            safe=False)
    elif request.user == 'acisi_fibog':
        return JsonResponse({'allowed_to_generate': [
            {'ALL': 'Generar todas las solicitudes estudiantiles'},
            {'ARC_SIIN': 'Generar las solicitudes del Área Curricular de' +
             ' Ingeniería de Sistemas e Industrial'},
            {'PRE_SIST': 'Generar las solicitudes del pregrado en Ingeniería de Sistemas y Computación'},
            {'PRE_INDU': 'Generar las solicitudes del pregrado en Ingeniería Industrial'},
            {'POS_ARSI': 'Generar las solicitudes de posgrados pertenecientes' +
             ' al Área curricular de Ingeniería de Sistemas e Industrial'},
        ]},
            status=HTTP_200_OK,
            safe=False)
    else:
        return JsonResponse({'error': 'username without choices'},
                            status=HTTP_400_BAD_REQUEST,
                            safe=False)


@api_view(["GET"])
@permission_classes((AllowAny,))
def generate_spec(_):
    return JsonResponse({'': ''})
