from docx import Document
from django.test import TestCase
from council_minutes.models import Subject, Request, Professor


class AAUTestCase(TestCase):

    def test_can_create_cm(self):
        """AAUT can write on CM correctly"""
        # pylint: disable=no-member
        document = Document()
        request = Request.objects.get(id='5da67f49d76fda9c14c66e42')
        request.cm(document)
