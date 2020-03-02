import json
from .models import Request, RequestChanges
from mongoengine.errors import ValidationError

def update_request(data):
    assert 'id' in data, "Object hasn't 'id' key"
    target = Request.get_case_by_id(data['id'])
    del data['id']
    params = translation(target, data)
    #An object built from data it's necessary to compare including data type
    copy = target.__class__().from_json(json.dumps(params))
    keys = set(params.keys()).intersection(set(target._fields.keys()))
    differences = {}
    for key in keys:
        if target[key] != copy[key]:
            differences[key] = target[key]
            target[key] = copy[key]
    try:
        target.save()
        if differences != {}:
            RequestChanges(
                request_id=target, 
                user=params['user'],
                changes=differences
            ).save()
        return target
    except ValidationError as e:
        return {'error': e.message}

def translation(obj, data):
    Json = json.dumps(data)
    response = json.loads(obj.__class__.translate(Json))
    return response