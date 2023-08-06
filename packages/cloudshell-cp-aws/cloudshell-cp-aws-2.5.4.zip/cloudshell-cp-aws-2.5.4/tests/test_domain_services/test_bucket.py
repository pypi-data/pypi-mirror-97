from unittest import TestCase

import botocore
from mock import Mock

from cloudshell.cp.aws.domain.services.s3.bucket import S3BucketService


class TestS3BucketService(TestCase):
    def setUp(self):
        self.bucket_service = S3BucketService()

    def test_get_body_of_object(self):
        obj = Mock()
        body = {'Body': Mock()}
        obj.get = Mock(return_value=body)
        data = self.bucket_service.get_body_of_object(obj)

        self.assertTrue(obj.get.called)
        self.assertEqual(data, body['Body'].read())

    def test_get_body_of_object_none(self):
        self.assertRaises(ValueError, self.bucket_service.get_body_of_object, None)

    def test_get_key(self):
        obj = Mock()
        s3_session = Mock()
        s3_session.Object = Mock(return_value=obj)

        obj.load = Mock()
        bucket_name = 'bucket'
        key = 'key'

        res = self.bucket_service.get_key(s3_session, bucket_name, key)

        self.assertTrue(s3_session.Object.called_with(bucket_name, key))
        self.assertTrue(obj.load.called)
        self.assertEqual(res, obj)

    def test_get_key_no_obj(self):
        s3_session = Mock()
        s3_session.Object = Mock(return_value=None)
        self.assertIsNone(self.bucket_service.get_key(s3_session, ' ', ' '))

    def test_get_key_none(self):
        self.assertRaises(ValueError, self.bucket_service.get_key, Mock(), '', 'something')
        self.assertRaises(ValueError, self.bucket_service.get_key, Mock(), '', None)

    def test_put_key(self):
        s3_session = Mock()
        value = Mock()
        bucket_name = 'bucket'
        key = 'key'

        self.bucket_service.put_key(s3_session, bucket_name, key, value)

        self.assertTrue(value.encode.called_with('utf-8'))
        self.assertTrue(s3_session.Bucket.called_with(bucket_name))
        self.assertTrue(s3_session.Bucket(bucket_name).put_object.called_with(value.encode(), key))

    def test_delete_key(self):
        s3_session = Mock()
        obj = Mock()
        s3_session.Object = Mock(return_value=obj)

        res = self.bucket_service.delete_key(s3_session, 'buck', 'key')

        self.assertTrue(s3_session.get_key.called_with('buck', 'key'))
        self.assertTrue(obj.delete.called)
        self.assertIsNotNone(res)

    def test_delete_key_false(self):
        s3_session = Mock()
        s3_session.Object = Mock(return_value=None)

        res = self.bucket_service.delete_key(s3_session, 'buck', 'key')

        self.assertTrue(s3_session.get_key.called_with('buck', 'key'))
        self.assertFalse(res)

    def test_delete_key_none(self):
        s3_session = Mock()
        s3_session.Object = Mock(return_value=None)

        res = self.bucket_service.delete_key(s3_session, 'buck', None)
        self.assertFalse(res)