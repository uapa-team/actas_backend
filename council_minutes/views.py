import json
import datetime
import mongoengine
from mongoengine.errors import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request
from .helpers import QuerySetEncoder, Translator
from .docx import CouncilMinuteGenerator
# Esto va solo para evitar la verificacion de django


def index():
    return HttpResponse("¡Actas trabajando!")


@csrf_exempt  # Esto va solo para evitar la verificacion de django
def filter_request(request):
    if request.method == 'POST':
        # Generic Query for Request model
        # To make a request check http://docs.mongoengine.org/guide/querying.html#query-operators
        params = json.loads(request.body)
        response = Request.objects.filter(**params).order_by('req_acad_prog')
        return JsonResponse(response, safe=False, encoder=QuerySetEncoder)

    else:
        return HttpResponse('Bad Request', status=400)


@csrf_exempt  # Esto va solo para evitar la verificacion de django
def insert_request(request):
    if request.method == 'POST':
        new_request = Request().from_json(Translator.translate(request.body))
        try:
            new_request.save()
            return HttpResponse(request.body, status=201)
        except ValidationError as e:
            print()
            print(e)
            return HttpResponse(e.message, status=400)
    else:
        return HttpResponse('Bad Request', status=400)


@csrf_exempt
def docx_gen_by_id(request, cm_id):
    filename = 'public/acta' + cm_id + '.docx'
    try:
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
            acta = Request.objects.get(id=cm_id)
        except mongoengine.DoesNotExist:
            return HttpResponse('Does not exist', status=404)
        json_body = json.loads(Translator.translate(request.body))
        if hasattr(acta, 'old'):
            old = acta.old
        else:
            old = []
        old_obj = {}
        some_change = False
        if 'type' in json_body:
            if acta.type != json_body['type']:
                some_change = some_change or True
                old_obj.update({'type': acta.type})
                acta.type = json_body['type']
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
        if 'student_dni_type' in json_body:
            if acta.student_dni_type != json_body['student_dni_type']:
                some_change = some_change or True
                old_obj.update({'student_dni_type': acta.student_dni_type})
                acta.student_dni_type = json_body['student_dni_type']
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
    except (json.decoder.JSONDecodeError):
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
