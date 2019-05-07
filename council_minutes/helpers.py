from django.core.serializers.json import DjangoJSONEncoder

class QuerySetEncoder(DjangoJSONEncoder):

    def default(self, querySet):
        json = {}
        for element in querySet:
            json[str(element.id)] = {}
            for field in element._fields_ordered[1:]:
                json[str(element.id)][field] = str(element[field])

        return json