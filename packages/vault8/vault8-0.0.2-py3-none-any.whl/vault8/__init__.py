"""
Python3 library for Vault8 service
"""

import io
import os
import time
import json
import hashlib
import requests

class Vault8():
    """
    Vault8 class implementation
    """
    def __init__(self, public_key: str, secret_key: str, service_url: str):
        self._public_key = public_key
        self._secret_key = secret_key
        self._service_url = service_url

    def image_url(self, uid: str, filters: list=None, image_name: str='image.jpg',
            current_time: int=None, until_time: int=None) -> str:
        """
        Return URL for image download
        """
        return self.generate_url_for(path=self.image_path(uid=uid, filters=filters,
            image_name=image_name), current_time=current_time, until_time=until_time)

    def upload_url(self, path: str='/upload',
            current_time: int=int(time.time()), until_time: int=int(time.time())+86400) -> str:
        """
        Return URL for image upload
        """
        return self.generate_url_for(path=path, current_time=current_time, until_time=until_time)

    def encode_token(self, path: str, current_time: int=None, until_time: int=None) -> str:
        """
        Create SecureURI: generate token
        """
        secure_token = '|'.join([self._public_key, self._secret_key, path])
        if current_time:
            secure_token = secure_token + '|' + str(current_time)
        if until_time:
            secure_token = secure_token + '|' + str(until_time)

        return hashlib.sha1(secure_token.encode()).hexdigest()[::-1]

    def image_path(self, uid: str, filters: list=None, image_name: str='image.jpg') -> str:
        """
        Return full path to image
        """
        if filters:
            return '/{0}/{1}/{2}'.format(uid, self.merged_filters(filters),
                requests.compat.quote(image_name))
        return '/{0}/{1}'.format(uid, requests.compat.quote(image_name))

    # pylint: disable=R0201
    def merged_filters(self, filters: list=None) -> str:
        """
        Merge filters to string (filters : list of tuples)
        Example: filters=[('resize_fill',1000,500), ('grayscale',)]
        """
        merged = ''

        if filters:
            for flt in filters:
                if len(flt) == 1:
                    merged = ','.join([merged, str(flt[0])])
                else:
                    merged = ','.join([merged, '-'.join(map(str,flt))])

        return merged.strip(',')

    def generate_url_for(self, path: str, current_time: int=None, until_time: int=None) -> str:
        """
        URL generator
        """
        uri = requests.compat.urljoin(self._service_url, path)
        query = {
            'p': self._public_key,
            's': self.encode_token(path=path, current_time=current_time, until_time=until_time)
        }
        if current_time:
            query['time'] = current_time
        if until_time:
            query['until'] = until_time

        return requests.Request(method='POST', url=uri, params=query).prepare().url

    def upload_image(self, file) -> dict:
        """
        Upload image
        'file' can be:
            - str with image URL - vault8 service will download image
            - IOBase object - file will be uploaded from object
        """
        if isinstance(file, str):
            options = {'url': file}
        elif isinstance(file, io.IOBase):
            options = {'file': file}
        elif isinstance(file, dict):
            options = file
        return self.__post_request(options)

    def __post_request(self, options: dict):
        try:
            if options.get('url'):
                return json.loads(self.__post_link(options))
            return json.loads(self.__post_file(options))
        except json.JSONDecodeError:
            return {'status': 'error', 'response': 'json decode error'}

    def __post_link(self, url: str):
        return requests.post(self.upload_url(), data=url).text

    def __post_file(self, file):
        return requests.post(self.upload_url(), files=file).text
