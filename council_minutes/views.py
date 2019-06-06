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
# Esto va solo para evitar la verificacion de django
from django.views.decorators.csrf import csrf_exempt


def index(request):
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
        request_by_id = Request.objects.get(id=cm_id)
    except mongoengine.DoesNotExist:
        return HttpResponse('Does not exist', status=404)
    generator = CouncilMinuteGenerator()
    generator.add_case_from_request(request_by_id)
    generator.generate(filename)
    return HttpResponse(filename)


@ccsrf_exempt
def update_cm(request, cm_id):
