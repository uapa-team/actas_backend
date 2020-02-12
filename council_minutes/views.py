# pylint: disable=wildcard-import,unused-wildcard-import
import json
import datetime
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from mongoengine.errors import ValidationError
from .models import Request, Person, SubjectAutofill
from .helpers import QuerySetEncoder, get_fields, get_period_choices
from .writter import UnifiedWritter
from .cases import *


@api_view(["GET"])
@permission_classes((AllowAny,))
def check(request):
    return JsonResponse({"Ok?": "Ok!"}, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    # pylint: disable=no-member
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
def details(_):
    programs = Request.get_programs()
    programs.update({'periods': [period[0] for period in get_period_choices()]})
    return JsonResponse(programs, status=HTTP_200_OK, safe=False)


@api_view(["GET"])
def info_cases(request):
    if request.GET.get('cls') == '' or request.GET.get('cls') is None:
        return JsonResponse(Request.get_cases(), status=HTTP_200_OK)
    else:
        for type_case in Request.get_subclasses():
            if type_case.__name__ == request.GET.get('cls'):
                return JsonResponse(get_fields(type_case))
        return JsonResponse({'response': 'Not found'}, status=HTTP_404_NOT_FOUND)


@api_view(["GET", "PATCH", "POST"])
def case(request):
    if request.method == 'GET':
        responses = Request.get_cases_by_query(querydict_to_dict(request.GET))
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
                req = Request.get_case_by_id(item_request['_id'])
            except (ValueError, KeyError):
                not_found += [item_request['_id']]
                continue
            item_request['user'] = request.user.username
            case = req.__class__
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


def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data


@api_view(["GET"])
def get_docx_genquerie(request):
    query_dict = querydict_to_dict(request.GET)
    try:
        precm = query_dict['pre'] == 'true'
        del query_dict['pre']
    except KeyError:
        return JsonResponse({'error': "'pre' Key not provided"}, status=HTTP_400_BAD_REQUEST)

    generator = UnifiedWritter()
    generator.filename = 'public/' + \
        str(request.user) + str(datetime.date.today()) + '.docx'
    generator.generate_document_by_querie(query_dict, precm)
    return JsonResponse({'url': generator.filename}, status=HTTP_200_OK)

@api_view(["POST"])
def autofill(request):
    # pylint: disable=no-member
    body = json.loads(request.body)
    if 'field' not in body:
        return JsonResponse({'error':'"field" key is not in body'}, status=HTTP_400_BAD_REQUEST)
    try:
        if body['field'] == 'name':
            if 'student_dni' not in body:
                return JsonResponse({'error':'"student_dni" key is not in body'}, status=HTTP_400_BAD_REQUEST)
            try:
                student = Person.objects.filter(student_dni=body['student_dni'])[0]
            except IndexError:
                return JsonResponse({'error':'dni not found'}, status=HTTP_204_NO_CONTENT)
            else:
                return JsonResponse({'student_dni': student.student_dni,
                'student_dni_type': student.student_dni_type,
                'student_name': student.student_name}, status=HTTP_200_OK)
        elif body['field'] == 'subject':
            if 'subject_code' not in body:
                return JsonResponse({'error':'"subject_code" key is not in body'}, status=HTTP_400_BAD_REQUEST)
            try:
                subject = SubjectAutofill.objects.filter(subject_code=body['subject_code'])[0]
            except IndexError:
                return JsonResponse({'error':'subject code not found'}, status=HTTP_204_NO_CONTENT)
            else:
                return JsonResponse({'subject_code': subject.subject_code,
                'subject_name': subject.subject_name}, status=HTTP_200_OK)
    except ValueError:
        return JsonResponse({'error':'field "field" no encontrado'}, safe=False, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def allow_generate(request):
    username = request.user.username
    options = {}
    options['ALL'] = {
        'display': 'Generar todas las solicitudes estudiantiles',
        'filter': ''
    }

    if username == 'acica_fibog':
        options['ARC_CIAG'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Civil y Agrícola',
            'filter': 'academic_program__in=2541&academic_program__in=2542&academic_program__in=2886&academic_program__in=2696&academic_program__in=2699&academic_program__in=2700&academic_program__in=2701&academic_program__in=2705&academic_program__in=2706&academic_program__in=2887'
        }
        options['PRE_CIVI'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Civil',
            'filter': 'academic_program=2542'
        }
        options['PRE_AGRI'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Agrícola',
            'filter': 'academic_program=2541'
        }
        options['POS_ARCA'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular de Ingeniería Civil y Agrícola',
            'filter': 'academic_program__in=2886&academic_program__in=2696&academic_program__in=2699&academic_program__in=2700&academic_program__in=2701&academic_program__in=2705&academic_program__in=2706&academic_program__in=2887'
        }
    elif username == 'acimm_fibog':
        options['ARC_MEME'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Mecánica y Mecatrónica',
            'filter': 'academic_program__in=2547&academic_program__in=2548&academic_program__in=2710&academic_program__in=2709&academic_program__in=2839&academic_program__in=2682'
        }
        options['PRE_MECA'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Mecánica',
            'filter': 'academic_program=2547'
        }
        options['PRE_METR'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Mecatrónica',
            'filter': 'academic_program=2548'
        }
        options['POS_ARMM'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular de Ingeniería Mecánica y Mecatrónica',
            'filter': 'academic_program__in=2710&academic_program__in=2709&academic_program__in=2839&academic_program__in=2682'
        }
    elif username == 'aciee_fibog':
        options['ARC_ELEL'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Eléctrica y Electrónica',
            'filter': 'academic_program__in=2544&academic_program__in=2545&academic_program__in=2691&academic_program__in=2698&academic_program__in=2703&academic_program__in=2865&academic_program__in=2685'
        }
        options['PRE_ELCT'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Eléctrica',
            'filter': 'academic_program=2544'
        }
        options['PRE_ETRN'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Electrónica',
            'filter': 'academic_program=2545'
        }
        options['POS_AREE'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular de Ingeniería Eléctrica y Electrónica',
            'filter': 'academic_program__in=2691&academic_program__in=2698&academic_program__in=2703&academic_program__in=2865&academic_program__in=2685'
        }
                
    elif username == 'aciqa_fibog':
        options['ARC_QIAM'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería Química y Ambiental',
            'filter': 'academic_program__in=2549&academic_program__in=2704&academic_program__in=2562&academic_program__in=2686'
        }
        options['PRE_QUIM'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Química',
            'filter': 'academic_program=2549'
        }
        options['POS_ARQA'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular de Ingeniería Química y Ambiental',
            'filter': 'academic_program__in=2704&academic_program__in=2562&academic_program__in=2686'
        }
    elif username == 'acisi_fibog' or username == 'daescobarp':
        options['ARC_SIIN'] = {
            'display': 'Generar las solicitudes del Área Curricular de Ingeniería de Sistemas e Industrial',
            'filter': 'academic_program__in=2879&academic_program__in=2546&academic_program__in=2896&academic_program__in=2708&academic_program__in=2882&academic_program__in=2702&academic_program__in=2707&academic_program__in=2684&academic_program__in=2838'
        }
        options['PRE_SIST'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería de Sistemas',
            'filter': 'academic_program=2879'
        }
        options['PRE_INDU'] = {
            'display': 'Generar las solicitudes del pregrado en Ingeniería Industrial',
            'filter': 'academic_program=2546'
        }
        options['POS_ARSI'] = {
            'display': 'Generar las solicitudes de posgrados pertenecientes al Área curricular de Ingeniería de Sistemas e Industrial',
            'filter': 'academic_program__in=2896&academic_program__in=2708&academic_program__in=2882&academic_program__in=2702&academic_program__in=2707&academic_program__in=2684&academic_program__in=2838'
        }
    return JsonResponse(options, status=HTTP_200_OK, safe=False)
