from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Test
from .helpers import QuerySetEncoder


def index(request):
    return HttpResponse("¡Actas trabajando!")

def request(request):
    req = Test.objects
    
    return JsonResponse(req, safe=False, encoder=QuerySetEncoder)
