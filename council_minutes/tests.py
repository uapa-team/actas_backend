from docx import Document
from django.test import TestCase
from council_minutes.models import Subject, Request, Professor


class TestCases(TestCase):

    unique_ids = [
        '5d83c4ec6a12d53c1de1b85c',
        '5d88f7696a12d53c1de23bd3',
        '5d88f97b6a12d53c1de23d6f',
        '5d96143d6a12d53c1de2db3d',
        '5d96263f6a12d53c1de2f3da',
        '5d9626d56a12d53c1de2f4c3',
        '5d962d5d6a12d53c1de2fe2b',
        '5d9642c36a12d53c1de31b5f',
        '5d964cc96a12d53c1de32814',
        '5d9654116a12d53c1de3343e',
        '5d9cac226a12d53c1de3ca8b',
        '5d9ce6146a12d53c1de3d586',
        '5d9cfb8d6a12d53c1de3e64f',
        '5d9e42526a12d53c1de3ff5b',
        '5d9e42676a12d53c1de3ff6b',
        '5da099006a12d53c1de42a92',
        '5da0a4a86a12d53c1de432cf',
        '5da0a5336a12d53c1de43346',
        '5da0b5fa6a12d53c1de439b5',
        '5da0b9536a12d53c1de43c76',
        '5da0c6df6a12d53c1de446e2',
        '5da0d4786a12d53c1de4508d',
        '5da0d5876a12d53c1de4514e',
        '5da0e3fd6a12d53c1de45468',
        '5da0e4136a12d53c1de4546f',
        '5da0e80a6a12d53c1de456c0',
        '5da24476d76fda9c14c65e74',
        '5da2448cd76fda9c14c65e81',
        '5da67f49d76fda9c14c66e42',
        '5da73005d76fda9c14c67188',
        '5da7390ed76fda9c14c67218',
        '5da73924d76fda9c14c6721f',
        '5da77051d76fda9c14c67774',
        '5da77060d76fda9c14c67786',
        '5da79db6d76fda9c14c67f76',
        '5da79dc3d76fda9c14c67f7c',
        '5da8980dd76fda9c14c68478',
        '5da9d65cd76fda9c14c69313',
        '5da9e52dd76fda9c14c69ab3',
        '5da9f14bd76fda9c14c6a484',
        '5da9fcb6d76fda9c14c6ab5f',
        '5daa31abd76fda9c14c6c0b7',
        '5dade4b7d76fda9c14c6c5f4',
        '5dade941d76fda9c14c6c79a',
        '5dadfdb9d76fda9c14c6cda2',
        '5dae1651d76fda9c14c6dcb0',
        '5dae1707d76fda9c14c6dd3a',
        '5dae1745d76fda9c14c6dd7b',
        '5dae349ed76fda9c14c6edac',
        '5dae34d6d76fda9c14c6edc7',
        '5daf2a62d76fda9c14c6f4ee',
        '5daf3640d76fda9c14c6f8fc',
        '5daf365ed76fda9c14c6f914',
        '5db0c532d76fda9c14c70ed2',
        '5db0c550d76fda9c14c70edc',
        '5db9fd1dd76fda9c14c7328c',
        '5db9fd29d76fda9c14c73296',
        '5dbb23b2d76fda9c14c741a0',
        '5dbb24ddd76fda9c14c742c4',
        '5dbb2b90d76fda9c14c746da',
        '5dbb2c47d76fda9c14c747a0',
        '5dbb35bfd76fda9c14c74d42',
        '5dbb365cd76fda9c14c74d92',
        '5dbb807cd76fda9c14c75719',
        '5dbb82ccd76fda9c14c75779'
    ]

    def test_cases_can_create_cm(self):
        # pylint: disable=no-member
        document = Document()
        for unique_id in self.unique_ids:
            request = Request.objects.get(id=unique_id)
            request.cm(document)

    def test_cases_can_create_pcm(self):
        # pylint: disable=no-member
        document = Document()
        for unique_id in self.unique_ids:
            request = Request.objects.get(id=unique_id)
            request.pcm(document)
