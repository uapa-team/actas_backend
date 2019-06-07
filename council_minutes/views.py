import mongoengine
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Request
from .helpers import QuerySetEncoder, Translator
from .docx import CouncilMinuteGenerator
from .helpers import QuerySetEncoder
import os
import json
from mongoengine.errors import ValidationError
from django.views.decorators.csrf import csrf_exempt #Esto va solo para evitar la verificacion de django


def index(request):
    return HttpResponse("¡Actas trabajando!")

@csrf_exempt #Esto va solo para evitar la verificacion de django
def filter_request(request):
    if request.method == 'POST':
        #Generic Query for Request model
        #To make a request check http://docs.mongoengine.org/guide/querying.html#query-operators
        params = json.loads(request.body)
        response = Request.objects.filter(**params).order_by('req_acad_prog')
        return JsonResponse(response, safe=False, encoder=QuerySetEncoder)
    
    else:
        return HttpResponse('Bad Request', status=400)


@csrf_exempt #Esto va solo para evitar la verificacion de django
def insert_request(request):
    if request.method == 'POST':
        new_request = Request().from_json(Translator.translate(request.body))
        try:
            response = new_request.save()
            
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
        request_by_id = Request.objects.get(id = cm_id)
    except mongoengine.DoesNotExist:
        return HttpResponse('Does not exist', status=404)
    generator = CouncilMinuteGenerator()
    generator.add_case_from_request(request_by_id)
    generator.generate(filename)
    return HttpResponse(filename)

@csrf_exempt
def docx_gen_by_date(request):
    try:
        body = json.loads(request.body)
        start_date=body['cm']['start_date']
        end_date=body['cm']['end_date']
    except (json.decoder.JSONDecodeError):
        return HttpResponse("Bad Request", status=400)
    filename = 'public/acta' + start_date.split(':')[0] + '_' + end_date.split(':')[0] + '.docx'
    generator = CouncilMinuteGenerator()
    try:
        generator.add_cases_from_date(start_date, end_date)
    except IndexError:
        return HttpResponse('No cases in date range specified', status=401)
    generator.generate(filename)
    return HttpResponse(filename)