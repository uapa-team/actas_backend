import json
import datetime
import mongoengine
from mongoengine.errors import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request, get_fields
from .helpers import QuerySetEncoder
from .docx import CouncilMinuteGenerator
from .docx import PreCouncilMinuteGenerator
from .cases import *


def index():
    return HttpResponse("Working!")


def cases_defined(request):
    if request.method == 'GET':
        response = {
            'cases': [
                {'code': type_case.__name__, 'name': type_case.full_name}
                for type_case in Request.__subclasses__()]
        }
        return JsonResponse(response)


def info_cases(request, case_id):
    if request.method == 'GET':
        for type_case in Request.__subclasses__():
            if type_case.__name__ == case_id:
                return JsonResponse(get_fields(type_case()))
        return JsonResponse({'response': 'Not found'}, status=404)


@csrf_exempt  # Esto va solo para evitar la verificacion de django
def filter_request(request):
    if request.method == 'POST':
        # Generic Query for Request modelstart_date.split(':')[0] + '_' + end_date.split(':')[0]
        # To make a request check http://docs.mongoengine.org/guide/querying.html#query-operators
        params = json.loads(request.body)
        # pylint: disable=no-member
        response = Request.objects.filter(
            **params).order_by('academic_program')
        return JsonResponse(response, safe=False, encoder=QuerySetEncoder)

    else:
        return HttpResponse('Bad Request', status=400)


@csrf_exempt  # Esto va solo para evitar la verificacion de django
def insert_request(request):
    body = json.loads(request.body)
    shell = json.dumps({'_cls': 'Request'})
    _cls = body['_cls'].split('.')[-1]
    subs = [c.__name__ for c in Request.__subclasses__()]
    case = Request.__subclasses__()[subs.index(_cls)]
    new_request = case().from_json(
        case.translate(shell.encode('utf-8')))
    new_request.user = body['user']
    try:
        response = new_request.save()
        response._cls = body['_cls']
        response.save()
        return JsonResponse({'id': str(response.id)}, safe=False)
    except ValidationError as e:
        return HttpResponse(e.message, status=400)


@csrf_exempt
def docx_gen_by_id(request, cm_id):
    filename = 'public/acta' + cm_id + '.docx'
    try:
        # pylint: disable=no-member
        request_by_id = Request.objects.get(id=cm_id)
    except mongoengine.DoesNotExist:
        return HttpResponse('Does not exist', status=404)
    generator = CouncilMinuteGenerator()
    generator.add_case_from_request(request_by_id)
    generator.generate(filename)
    return HttpResponse(filename)


@csrf_exempt
def update_cm(request, cm_id):
    if request.method == 'PATCH':
        try:
            # pylint: disable=no-member
            acta = Request.objects.get(id=cm_id)
        except mongoengine.DoesNotExist:
            return HttpResponse('Does not exist', status=404)
        # TODO: Se realizaron cambios en la forma de traducir
        json_body = json.loads(request.body)
        if hasattr(acta, 'old'):
            old = acta.old
        else:
            old = []
        old_obj = {}
        some_change = False
        if 'type_case' in json_body:
            if acta.type_case != json_body['type_case']:
                some_change = some_change or True
                old_obj.update({'type_case': acta.type_case})
                acta.type_case = json_body['type_case']
        if 'student_name' in json_body:
            if acta.student_name != json_body['student_name']:
                some_change = some_change or True
                old_obj.update({'student_name': acta.student_name})
                acta.student_name = json_body['student_name']
        if 'approval_status' in json_body:
            if acta.approval_status != json_body['approval_status']:
                some_change = some_change or True
                old_obj.update({'approval_status': acta.approval_status})
                acta.approval_status = json_body['approval_status']
        if 'student_dni' in json_body:
            if acta.student_dni != json_body['student_dni']:
                some_change = some_change or True
                old_obj.update({'student_dni': acta.student_dni})
                acta.student_dni = json_body['student_dni']
        if 'student_dni_type_case' in json_body:
            if acta.student_dni_type_case != json_body['student_dni_type_case']:
                some_change = some_change or True
                old_obj.update(
                    {'student_dni_type_case': acta.student_dni_type_case})
                acta.student_dni_type_case = json_body['student_dni_type_case']
        if 'academic_period' in json_body:
            if acta.academic_period != json_body['academic_period']:
                some_change = some_change or True
                old_obj.update({'academic_period': acta.academic_period})
                acta.academic_period = json_body['academic_period']
        if 'academic_program' in json_body:
            if acta.academic_program != json_body['academic_program']:
                some_change = some_change or True
                old_obj.update({'academic_program': acta.academic_program})
                acta.academic_program = json_body['academic_program']
        if 'justification' in json_body:
            if acta.justification != json_body['justification']:
                some_change = some_change or True
                old_obj.update({'justification': acta.justification})
                acta.justification = json_body['justification']
        if 'user' in json_body:
            if acta.user != json_body['user']:
                some_change = some_change or True
                old_obj.update({'user': acta.user})
                acta.user = json_body['user']
        if 'detail_cm' in json_body:
            if acta.detail_cm != json_body['detail_cm']:
                some_change = some_change or True
                old_obj.update({'detail_cm': acta.detail_cm})
                acta.detail_cm = json_body['detail_cm']
        if some_change:
            old_obj.update({'user_who_update': acta.user})
            old_obj.update({'datetime_update': datetime.datetime.now()})
            old.append(old_obj)
            acta.old = old
            acta.save()
            return HttpResponse('Changes updated successfully', status=200)
        return HttpResponse('No changes detected', status=204)


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
