from ...models import Request
from mongoengine import DynamicDocument, DateField, StringField, ListField, IntField, FloatField


class Subject(DynamicDocument):
    name = StringField(required=True)
    code = StringField(required=True)
    credits = StringField(required=True)
    group = StringField(required=True)
    tipology = StringField(required=True)


class CASI(Request):
    subjects = ListField(Subject, required=True)
    advance = FloatField(required=True)
    enrolled_academic_periods = IntField(required=True)
    papa = FloatField(required=True)
    available_credits = IntField(required=True)
    current_credits = IntField(required=True)
    extra_analysis = ListField(StringField(required=True))
    nrc_answer = StringField()
