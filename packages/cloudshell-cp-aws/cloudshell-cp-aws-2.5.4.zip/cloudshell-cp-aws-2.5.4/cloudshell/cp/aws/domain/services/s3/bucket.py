import botocore


class S3BucketService(object):
    def __init__(self):
        pass

    @staticmethod
    def get_body_of_object(obj):
        """
        Will load a S3 object and download it content
        :param obj: S3 Object
        :return: str it body data
        """
        if not obj:
            raise ValueError('S3 object cannot be None')
        object_body = obj.get()
        body_stream = object_body['Body']
        data = body_stream.read()
        return data

    @staticmethod
    def get_key(s3_session, bucket_name, key):
        """
        Gets the provided key if exists, otherwise returns None
        :param s3_session: S3 Session
        :param bucket_name: The bucket name
        :type bucket_name: str
        :param key: The in the bucket
        :type key: str
        :return:
        """
        try:
            if not key:
                raise ValueError('S3 object key cannot be empty')

            if not bucket_name:
                raise ValueError('S3 bucket name cannot be empty')

            obj = s3_session.Object(bucket_name, key)
            obj.load()
        except ValueError:
            raise
        except Exception:
            # todo: write to log
            obj = None
        return obj

    @staticmethod
    def put_key(s3_session, bucket_name, key, value):
        """
        Puts a key in s3
        :param s3_session: S3 session
        :param bucket_name: bucket name
        :type bucket_name: str
        :param key: Key name
        :type key: Key name
        :param value: The key value
        :type value: str
        :return:
        """
        bytes_arr = value.encode('utf-8')
        return s3_session.Bucket(bucket_name).put_object(Body=bytes_arr, Key=key)

    def delete_key(self, s3_session, bucket, key):
        """
        Will delete the key if exist
        :param s3_session: S3 Session
        :param bucket: The bucket name
        :type bucket: str
        :param key: The key to delete
        :type key: str
        :return:
        """
        if not key:
            return False

        obj = self.get_key(s3_session, bucket, key)
        if not obj:
            return False

        return obj.delete()
