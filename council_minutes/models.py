from django.db import models
from mongoengine import *


# Create your models here.

class Test(DynamicDocument):
    hola = StringField()