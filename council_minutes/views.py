from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Test, Request
from .helpers import QuerySetEncoder
import json
from mongoengine.errors import ValidationError
from django.views.decorators.csrf import csrf_exempt #Esto va solo para evitar la verificacion de django


def index(request):
    return HttpResponse("¡Actas trabajando!")

def request(request):
    req = Test.objects
    
    return JsonResponse(req, safe=False, encoder=QuerySetEncoder)

@csrf_exempt #Esto va solo para evitar la verificacion de django
def insert_request(request):
    if request.method == 'POST':
        
        new_request = Request().from_json(request.body)

        try:
            response = new_request.save()
            return HttpResponse(request.body, status=200)

        except ValidationError as e:
            return HttpResponse(e.message, status=400)

    else:
        return HttpResponse('Bad Request', status=400)