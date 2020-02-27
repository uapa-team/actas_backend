from .models import Request, RequestChanges
from mongoengine.errors import ValidationError

def update_request(params):
    assert 'id' in params, "Object hasn't 'id' key"
    target = Request.get_case_by_id(params['id'])
    del params['id']
    keys = set(params.keys()).intersection(set(target._fields.keys()))
    differences = {}
    for key in keys:
        if target[key] != params[key]:
            differences[key] = target[key]
            target[key] = params[key]
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
