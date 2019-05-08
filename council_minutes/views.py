from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Test
from .helpers import QuerySetEncoder
import json
from django.views.decorators.csrf import csrf_exempt #Esto va solo para evitar la verificacion de django


def index(request):
    return HttpResponse("¡Actas trabajando!")

def request(request):
    req = Test.objects
    
    return JsonResponse(req, safe=False, encoder=QuerySetEncoder)

@csrf_exempt #Esto va solo para evitar la verificacion de django
def post(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        return HttpResponse(json.dumps(data), status=200)
    else:
        return JsonResponse({"not post":"not post"})