import json
import datetime
import mongoengine
from mongoengine.errors import ValidationError
from django.contrib.auth import authenticate
from django_auth_ldap.backend import LDAPBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request, get_fields
from .helpers import QuerySetEncoder
from .docx import CouncilMinuteGenerator
from .docx import PreCouncilMinuteGenerator
from .cases import *


@api_view(["GET"])
@permission_classes((AllowAny,))
def index(request):
    return HttpResponse("Working!")


@api_view(["GET"])
def cases_defined(request):
    if request.method == 'GET':
        response = {
            'cases': [
                {'code': type_case.__name__, 'name': type_case.full_name}
                for type_case in Request.get_subclasses()]
        }
        return JsonResponse(response)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    if username is None or password is None:
        return Response({'error': 'Contraseña o usuario vacío o nulo.'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Error en ActasDB, usuario sin permisos en la aplicación.'},
                        status=HTTP_403_FORBIDDEN)
    user = LDAPBackend().authenticate(request, username=username, password=password)
    if not user:
        return Response({'error': 'Error en LDAP, contraseña o usuario no válido.'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(["GET"])
def info_cases(request, case_id):
    if request.method == 'GET':
        for type_case in Request.get_subclasses():
            if type_case.__name__ == case_id:
                return JsonResponse(get_fields(type_case()))
        return JsonResponse({'response': 'Not found'}, status=404)


@api_view(["POST"])
@csrf_exempt  # Esto va solo para evitar la verificacion de django
def filter_request(request):
    if request.method == 'POST':
        # Generic Query for Request modelstart_date.split(':')[0] + '_' + end_date.split(':')[0]
        # To make a request check http://docs.mongoengine.org/guide/querying.html#query-operators
        params = json.loads(request.body)
        # pylint: disable=no-member
        responses = Request.objects.filter(
            **params).order_by('-date')
        return JsonResponse(responses, safe=False, encoder=QuerySetEncoder)


@api_view(["POST"])
@csrf_exempt  # Esto va solo para evitar la verificacion de django
def insert_request(request):
    body = json.loads(request.body)
    shell = json.dumps({'_cls': 'Request'})
    subs = [c.__name__ for c in Request.get_subclasses()]
    case = Request.get_subclasses()[subs.index(body['_cls'])]
    shell = json.dumps({'_cls': case.get_entire_name()})
    new_request = case().from_json(
        case.translate(shell))
    new_request.user = body['user']
    try:
        response = new_request.save()
        response._cls = case.get_entire_name()
        response.save()
        return JsonResponse({'id': str(response.id)}, safe=False)
    except ValidationError as e:
        return HttpResponse(e.message, status=400)


@api_view(["GET", "POST"])
@csrf_exempt
def docx_gen_by_id(request, cm_id):
    # pylint: disable=no-member
    filename = 'public/acta' + cm_id + '.docx'
    try:
        request_by_id = Request.objects.get(id=cm_id)
    except mongoengine.DoesNotExist:
        return HttpResponse('Does not exist', status=404)
    generator = CouncilMinuteGenerator()
    generator.add_case_from_request(request_by_id)
    generator.generate(filename)
    return HttpResponse(filename)


@api_view(["PATCH"])
@csrf_exempt
def update_cm(request, cm_id):
    if request.method == 'PATCH':
        # pylint: disable=no-member
        try:
            case = Request.objects.get(id=cm_id)
        except mongoengine.DoesNotExist:
            return HttpResponse('Does not exist', status=404)
        body = json.loads(request.body)
        body['_id'] = cm_id
        case = case.__class__
        _cls = body['_cls'] = case.__name__
        obj = case.from_json(case.translate(
            json.dumps(body)), True)
        obj._cls = case.get_entire_name()
        obj.save()
        return JsonResponse(obj, safe=False, encoder=QuerySetEncoder)


@api_view(["GET", "POST"])
@csrf_exempt
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
@csrf_exempt
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


@api_view(["POST"])
@csrf_exempt
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


@api_view(["POST"])
@csrf_exempt
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
@csrf_exempt
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


@api_view(["POST"])
@csrf_exempt
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
@csrf_exempt
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


@csrf_exempt
@api_view(["POST"])
def insert_many(request):
    body = json.loads(request.body)
    subs = [c.__name__ for c in Request.get_subclasses()]
    errors = []
    inserted_items = []
    for item_request in body['items']:
        item_request['user'] = body['user']
        case = Request.get_subclasses()[subs.index(item_request['_cls'])]
        item_request['_cls'] = case.get_entire_name()
        new_request = case().from_json(case.translate(json.dumps(item_request)))
        try:
            inserted_items += [new_request.save()]
        except ValidationError as e:
            errors += [e.message]
    return JsonResponse({'inserted_items': inserted_items, 'errors': errors},
                        status=HTTP_200_OK, encoder=QuerySetEncoder, safe=False)
