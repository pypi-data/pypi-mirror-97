import oss2
import requests
from django.conf import settings


class OSS:
    def __init__(self):
        self.auth = oss2.Auth(
            settings.BLUEDOT_REST_FRAMEWORK['utils']['OSS']['access_key_id'], settings.BLUEDOT_REST_FRAMEWORK['utils']['OSS']['access_key_secret'])
        self.bucket = oss2.Bucket(
            self.auth, settings.BLUEDOT_REST_FRAMEWORK['utils']['OSS']['endpoint'], settings.BLUEDOT_REST_FRAMEWORK['utils']['OSS']['bucket_name'])

    def put_object_internet(self, url, path):
        try:
            _input = requests.get(url)
            return self.bucket.put_object(path, _input)
        except expression as identifier:
            print('put_object_internet', identifier)
            pass

    def put_object_bytes(self, data, path):
        try:
            return self.bucket.put_object(path, data)
        except expression as identifier:
            print('put_object_bytes', identifier)
            pass


OSS = OSS()
