import copy

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from test.backendtestcase import TestCase
from test.utils import second_equals_first
from src.cs_models.resources.File import (
    File,
    FileNotFoundException,
)


class FileResourceTestCase(TestCase):
    def setUp(self):
        super(FileResourceTestCase, self).setUp()
        self.inst = File()
        self.file1 = self.inst.create({
            'file_format': 'txt',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key1',
        })
        self.valid_data = {
            'file_format': 'txt',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
        }

    def test_create_validation_error(self):
        self.assertRaises(
            ValidationError,
            self.inst.create,
            {
                'file_format': '',
                's3_bucket_name': 'test-bucket',
                's3_key_name': 'key1',
            },
        )

        self.assertRaises(
            ValidationError,
            self.inst.create,
            {
                'file_format': 'txt',
                's3_bucket_name': '',
                's3_key_name': 'key1',
            },
        )

    def test_create_duplicate_s3_bucket_and_key(self):
        self.assertRaises(
            IntegrityError,
            self.inst.create,
            {
                'file_format': 'txt',
                's3_bucket_name': 'test-bucket',
                's3_key_name': 'key1',
            },
        )

    def test_create(self):
        data = {
            'file_format': 'pdf',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
            'content_length': None,
        }
        response = self.inst.create(data)
        second_equals_first(data, response)

    def test_create_content_length_not_null(self):
        data = {
            'file_format': 'pdf',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
            'content_length': 123123,
        }
        response = self.inst.create(data)
        second_equals_first(data, response)

    def test_read_validation_error(self):
        self.assertRaises(
            ValidationError,
            self.inst.read,
            {
                'file_format': '',
            },
        )

        self.assertRaises(
            ValidationError,
            self.inst.read,
            {
                's3_bucket_name': '',
            },
        )

    def test_read_all(self):
        # setup
        self.inst.create({
            'file_format': 'txt',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
        })
        response = self.inst.read({})
        self.assertEqual(len(response), 2)

    def test_read_with_params(self):
        # setup
        self.inst.create({
            'file_format': 'txt',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
        })
        response = self.inst.read({'s3_key_name': 'key2'})
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['s3_key_name'], 'key2')

        response = self.inst.read({'file_format': 'txt'})
        self.assertEqual(len(response), 2)

    def test_delete_not_found(self):
        invalid_id = 99999
        self.assertRaises(
            FileNotFoundException,
            self.inst.delete,
            invalid_id,
        )

    def test_delete(self):
        response = self.inst.read({'id': self.file1['id']})
        self.assertEqual(len(response), 1)
        response = self.inst.delete(id=self.file1['id'])
        self.assertEqual(response, 'Successfully deleted')
        response = self.inst.read({'id': self.file1['id']})
        self.assertEqual(len(response), 0)

    def test_create_if_does_not_exist(self):
        data = {
            'file_format': 'pdf',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
        }
        response1 = self.inst.create_if_does_not_exist(data)
        second_equals_first(data, response1)

        new_data = {
            'file_format': 'txt',
            's3_bucket_name': 'test-bucket',
            's3_key_name': 'key2',
        }
        response2 = self.inst.create_if_does_not_exist(new_data)
        self.assertEqual(response2['id'], response1['id'])
        second_equals_first(data, response2)

    def test_update(self):
        new_data = {
            's3_bucket_name': 'some-other-bucket',
            's3_key_name': 'some-other-key',
        }
        resp = self.inst.update(
            id=self.file1['id'],
            params=new_data,
        )
        second_equals_first(
            {
                'id': self.file1['id'],
                's3_bucket_name': new_data['s3_bucket_name'],
                's3_key_name': new_data['s3_key_name'],
            },
            resp,
        )

    def test_update_raises_exception_for_empty_value(self):
        new_data = {
            's3_bucket_name': 'some-other-bucket',
            's3_key_name': '',
        }

        args = []
        kwargs = {
            'id': self.file1['id'],
            'params': new_data,
        }

        self.assertRaises(
            ValidationError,
            self.inst.update,
            *args,
            **kwargs
        )

    def test_upsert_validation_error(self):
        self.assertRaises(
            ValidationError,
            self.inst.upsert,
            {
                's3_bucket_name': self.valid_data['s3_bucket_name'],
            }
        )

    def test_upsert_creates_new_entry(self):
        data = copy.copy(self.valid_data)
        self.assertEqual(1, len(self.inst.read({})))
        self.inst.upsert(data)
        self.assertEqual(2, len(self.inst.read({})))

    def test_upsert_updates_existing_row(self):
        data = {
            **self.file1,
            **{'content_length': 123231432},
        }
        resp = self.inst.upsert(data)
        self.assertEqual(self.file1['s3_bucket_name'], resp['s3_bucket_name'])
        self.assertEqual(self.file1['s3_key_name'], resp['s3_key_name'])
        self.assertEqual(data['content_length'], resp['content_length'])
        self.assertEqual(1, len(self.inst.read({})))
