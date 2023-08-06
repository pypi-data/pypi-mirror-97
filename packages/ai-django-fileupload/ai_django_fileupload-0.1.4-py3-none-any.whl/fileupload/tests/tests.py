import json
import os
from unittest import mock
from tempfile import NamedTemporaryFile

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from fileupload.constants import UPLOADER_UPLOAD_DIRECTORY
from fileupload.models import upload_to
from fileupload.tests.test_utils import build_url
from model_mommy import mommy


class AttachmentListViewTests(TestCase):
    def setUp(self):
        """
        Set up all the tests
        """
        self.user = mommy.make(User)
        self.content_type_user = ContentType.objects.get(model="user")
        self.attachments = mommy.make('fileupload.Attachment',
                                      content_type=self.content_type_user,
                                      object_id=self.user.id,
                                      _create_files=True,
                                      _quantity=3)

    def test_show_all_attachments(self):
        """
        All existent attachments should be retrieved
        """
        response = self.client.get(build_url('upload-view', get={'content_type_id': self.content_type_user.id,
                                                                 'object_id': self.user.id}),
                                   HTTP_ACCEPT='application/json')
        response_files = json.loads(response.content)['files']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_files), len(self.attachments))


class AttachmentCreateViewTests(TestCase):

    ERROR_MSG = 'testing error'

    @staticmethod
    def create_test_file():
        test_file = NamedTemporaryFile()
        test_file.write('test123'.encode('utf-8'))
        test_file.seek(0)
        test_file.name = 'test.txt'
        return test_file

    @classmethod
    def setUpTestData(cls):
        """
        Set up all the tests
        """
        cls.user = mommy.make(User)
        cls.content_type_user = ContentType.objects.get(model="user")
        cls.attachment = mommy.make('fileupload.Attachment',
                                    content_type=cls.content_type_user,
                                    object_id=cls.user.id,
                                    _create_files=True)

    @override_settings(UPLOADER_ALLOW_FILETYPE=['.txt'], UPLOADER_ALLOW_FILETYPE_ERROR_MESSAGE=ERROR_MSG)
    def test_create_allow_filetype(self):
        data = {
            'file': self.create_test_file(),
            'content_type': self.content_type_user.id,
            'object_id': self.attachment.object_id
        }

        response = self.client.post(build_url('upload-new'), data=data, HTTP_ACCEPT='application/json')
        self.assertEqual(200, response.status_code)

    @override_settings(UPLOADER_DISALLOW_FILETYPE=[], UPLOADER_DISALLOW_FILETYPE_ERROR_MESSAGE=ERROR_MSG)
    def test_create_disallow_filetype(self):
        data = {
            'file': self.create_test_file(),
            'content_type': self.content_type_user.id,
            'object_id': self.attachment.object_id
        }
        response = self.client.post(build_url('upload-new'), data=data, HTTP_ACCEPT='application/json')
        self.assertEqual(200, response.status_code)

    @override_settings(UPLOADER_ALLOW_FILETYPE=[], UPLOADER_ALLOW_FILETYPE_ERROR_MESSAGE=ERROR_MSG)
    def test_create_allow_filetype_negative_case(self):

        data = {
            'file': self.create_test_file(),
            'content_type': self.content_type_user.id,
            'object_id': self.attachment.object_id
        }

        response = self.client.post(build_url('upload-new'), data=data, HTTP_ACCEPT='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(json.loads(response.content)['file'][0], self.ERROR_MSG)

    @override_settings(UPLOADER_DISALLOW_FILETYPE=['.txt'], UPLOADER_DISALLOW_FILETYPE_ERROR_MESSAGE=ERROR_MSG)
    def test_create_disallow_filetype_negative_case(self):
        data = {
            'file': self.create_test_file(),
            'content_type': self.content_type_user.id,
            'object_id': self.attachment.object_id
        }
        response = self.client.post(build_url('upload-new'), data=data, HTTP_ACCEPT='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(json.loads(response.content)['file'][0], self.ERROR_MSG)


class AttachmentUploadToTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mommy.make(User)
        cls.content_type_user = ContentType.objects.get(model="user")
        cls.attachment = mommy.make('fileupload.Attachment',
                                    content_type=cls.content_type_user,
                                    object_id=cls.user.id,
                                    _create_files=True)
        cls.filename = 'test_filename'

    def test_upload_to_default(self):
        self.assertEqual(os.path.dirname(upload_to(self.attachment, self.filename)) + '/', UPLOADER_UPLOAD_DIRECTORY)
        self.assertNotEqual(os.path.basename(upload_to(self.attachment, self.filename)), self.filename)

    @override_settings(UPLOADER_PERSIST_FILENAME=True)
    def test_upload_to_persist_filename(self):
        self.assertEqual(os.path.dirname(upload_to(self.attachment, self.filename)) + '/', UPLOADER_UPLOAD_DIRECTORY)
        self.assertEqual(os.path.basename(upload_to(self.attachment, self.filename)), self.filename)

    def test_upload_to_uuid_collision_avoidance(self):

        class UUIDReturn:
            hex = os.path.splitext(os.path.basename(self.attachment.file.name))[0]

            def __init__(self, hex=None):
                if hex:
                    self.hex = hex

        with mock.patch('uuid.uuid4', side_effect=[UUIDReturn(), UUIDReturn('NonExistingFile.txt')]):
            self.assertEqual(os.path.dirname(upload_to(self.attachment, os.path.basename(self.attachment.file.name)))
                             + '/', UPLOADER_UPLOAD_DIRECTORY)
        self.assertNotEqual(os.path.basename(upload_to(self.attachment, self.filename)), self.filename)

    @override_settings(UPLOADER_PERSIST_FILENAME=True)
    def test_upload_to_recursion_avoidance_persist_filename(self):
        self.assertEqual(os.path.dirname(upload_to(self.attachment, os.path.basename(self.attachment.file.name)))
                         + '/', UPLOADER_UPLOAD_DIRECTORY)
        self.assertEqual(os.path.basename(upload_to(self.attachment, self.filename)), self.filename)
