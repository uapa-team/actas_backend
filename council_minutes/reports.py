# pylint: disable=wildcard-import,unused-wildcard-import
import json
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from mongoengine.errors import ValidationError
from .models import Request, Person, SubjectAutofill, GroupsInfo, Subgroup
from .helpers import querydict_to_dict
from .writter import UnifiedWritter
from .updater import update_request
from .cases import *

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def report(request):
    body = json.loads(request.body)
    if 'map' not in body or 'reduce' not in body:
        return JsonResponse({'error': "'map' and 'reduce' must be passed into the body"}, 
        status=HTTP_400_BAD_REQUEST)

    cases = Request.get_cases_by_query(querydict_to_dict(request.GET))
    try:
        res = cases.map_reduce(
        map_f = body['map'], 
        reduce_f = body['reduce'],
        output = 'inline')

        results = []
        for r in res:
            results.append({
                "key": str(r.key),
                "value": str(r.value)
            })
        return JsonResponse({"results": results}, status=HTTP_200_OK)
    except:
        return JsonResponse({'error': "'map' or 'reduce' function aren't correctly formed"}, 
        status=HTTP_406_NOT_ACCEPTABLE)
    
    