from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Request
from .helpers import QuerySetEncoder, Translator
import json
from mongoengine.errors import ValidationError
from django.views.decorators.csrf import csrf_exempt #Esto va solo para evitar la verificacion de django


def index(request):
    return HttpResponse("¡Actas trabajando!")

@csrf_exempt #Esto va solo para evitar la verificacion de django
def filter_request(request):
    if request.method == 'GET':
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
            return HttpResponse(request.body, status=200)

        except ValidationError as e:
            return HttpResponse(e.message, status=400)

    else:
        return HttpResponse('Bad Request', status=400)