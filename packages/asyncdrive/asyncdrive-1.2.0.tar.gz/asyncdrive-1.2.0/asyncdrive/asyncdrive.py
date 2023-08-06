import aiohttp
import asyncio
import datetime
import io
import json
import os
import re
import shutil

from pathlib import Path
from .utils import create_jwt

parent_directory = Path(__file__).resolve().parent

MB = 4 * 256 * 1024
CHUNK_SIZE = 5 * MB


class AsyncRequest:

    def __init__(self, drive, *args, **kwargs):
        self.drive = drive
        self.args = args
        self.kwargs = kwargs

    async def __aenter__(self):
        await asyncio.sleep(self.drive.concurrent_requests // self.drive.ratelimit)
        async with self.drive.lock:
            await self.drive.ensure_valid_token()
        self.request = await self.drive.session.request(*self.args, **self.kwargs)
        return self.request

    async def __aexit__(self, type, value, traceback):
        try:
            if str(self.request.status)[0] not in ['2', '3']:
                raise Exception(
                    "Error {}: {}".format(self.request.status, await self.request.content.read()),
                    # f"Request: {self.args} {self.kwargs}, ",
                    f"Headers: {self.drive.session._default_headers}"
                )
            elif traceback:
                raise Exception(traceback)
        finally:
            self.drive.concurrent_requests -= 1
            self.request.close()


class AsyncFile:

    def __init__(self, drive, file_name, mode='r'):
        MODES = ['r', 'r+', 'rb', 'rb+', 'w', 'w+', 'wb', 'wb+']
        if mode not in MODES:
            raise Exception(f"Unsupported mode '{mode}'")

        self.drive = drive
        self.mode = mode

        self.metadata_ = {'name': file_name}

    @property
    def file_name(self):
        return self.metadata_['name']

    @property
    def cache_location(self):
        return f'{parent_directory}/asyncache/{self.file_name}'

    async def __aenter__(self):
        file_list = json.loads(await self.drive.list(q=f"name = '{self.file_name}'"))['files'] + [{}]
        self.file_id = file_list[0].get('id', None)

        if 'w' in self.mode:
            self.file = io.BytesIO() if 'b' in self.mode else io.StringIO()

        elif self.file_id:
            if self.drive.cache and os.path.exists(self.cache_location):
                with io.open(self.cache_location, self.mode) as file:
                    content = file.read()
                    self.file = io.BytesIO(content) if 'b' in self.mode else io.StringIO(content)
            else:
                bytes = await self.drive.get(self.file_id)
                self.file = io.BytesIO(bytes) if 'b' in self.mode else io.StringIO(bytes.decode('utf-8'))
        else:
            raise FileNotFoundError(f"File {self.file_name} not found")

        return self

    async def __aexit__(self, type, value, traceback):
        try:
            if traceback:
                raise Exception(traceback)

            if self.drive.cache:
                self.cache_file(self.file.getvalue())

            if hasattr(self, 'pending_delete'):
                await self.drive.delete(self.file_id)

            elif 'w' in self.mode and not self.file_id:
                await self.drive.create(
                    self.file.getvalue(), **self.metadata_, upload_type='multipart'
                )
            elif any(item in self.mode for item in ['w', '+']) and self.file_id:
                await self.drive.update(
                    self.file_id, self.file.getvalue(), **self.metadata_, upload_type='multipart'
                )
        finally:
            self.file.close()

    def __getattr__(self, attr):
        return getattr(self.file, attr)

    def metadata(self, *_, **kwargs):
        for key, value in kwargs.items():
            self.metadata_[key] = value

    def cache_file(self, value):
        if not os.path.exists(f"{parent_directory}/asyncache"):
            os.makedirs(f"{parent_directory}/asyncache")
        with io.open(self.cache_location, 'wb' if 'b' in self.mode else 'w') as file:
            file.write(value)

    def delete(self):
        if 'w' in self.mode or '+' in self.mode:
            self.pending_delete = True
        else:
            raise Exception("Cannot delete read-only file")


class ResumableUploadSession:

    def __init__(self, drive, data_length, upload_url=None, *_, **metadata):
        self.drive = drive
        self.data_length = data_length
        self.upload_url = upload_url
        self.metadata = metadata

        self.uploaded = 0
        self.max_retries = 3
        self.collected_bytes = b''
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        if not self.upload_url:
            self.upload_url = await self.get_upload_url()
            self.upload_id = re.findall("upload_id=(.*)", self.upload_url)[0]
        else:
            content_range = await self.get_content_range(self.upload_id)
            self.uploaded = re.findall("bytes=([0-9]*)-([0-9]*)", content_range)[0][1] + 1
        return self

    async def __aexit__(self, type, value, traceback):
        if traceback:
            raise Exception(traceback)

    async def upload(self, data):
        if type(data) == str:
            data = bytes(data, encoding='utf-8')

        self.collected_bytes += data

        async with self.lock:
            await self._upload()

    async def _upload(self):
        error_counter = 0
        while True:
            data_to_upload = self.collected_bytes[self.uploaded:self.uploaded + CHUNK_SIZE + 1]
            content_length = len(data_to_upload)

            if content_length == CHUNK_SIZE or self.data_length == len(self.collected_bytes):
                request_data = {
                    'method': 'PUT',
                    'url': 'https://www.googleapis.com/upload/drive/v3/files',
                    'params': f"uploadType=resumable&upload_id={self.upload_id}",
                    'headers': {
                        'Content-Length': str(content_length),
                        'Content-Range': f"bytes {self.uploaded}-{self.uploaded+content_length-1}/{self.data_length}"
                    },
                    'data': data_to_upload
                }
                async with self.drive.request(**request_data) as response:
                    if response.status == 308:
                        self.uploaded += len(data_to_upload)
                        error_counter = 0
                    elif response.status in (200, 201):
                        return None
                    else:
                        error_counter += 1
                if error_counter >= self.max_retries:
                    raise Exception('Upload interrupted')
            else:
                break

    async def get_upload_url(self):
         metadata, headers = self.drive.metadata_request(metadata=self.metadata)

         request_data = {
             'method': 'POST',
             'url': "https://www.googleapis.com/upload/drive/v3/files",
             'params': "uploadType=resumable",
             'headers': headers,
             'data': metadata
         }
         async with self.drive.request(**request_data) as response:
             return dict(response.headers)['Location']

    async def get_content_range(self, upload_id):
        request_data = {
            'method': 'PUT',
            'url': "https://www.googleapis.com/upload/drive/v3/files",
            'params': f"uploadType=resumable&upload_id={upload_id}",
            'headers': {
                'Content-Range': f'*/{self.data_length}'
            }
        }
        async with self.drive.request(**request_data) as response:
            return dict(response.headers)['Range']


class AsyncDrive:

    def __init__(self, cred_path, scopes, sub=None, ratelimit=10, cache=True):
        self.cred_path = cred_path
        self.scopes = scopes
        self.sub = sub
        self.ratelimit = ratelimit
        self.cache = cache

        self.session = aiohttp.ClientSession()
        self.lock = asyncio.Lock()
        self.token = None
        self.token_expiration_time = None
        self.concurrent_requests = 0
        self.request_types = {
            'media': self.media_request,
            'metadata': self.metadata_request,
            'multipart': self.multipart_request,
            'resumable': self.metadata_request
        }
        self.pending_requests = []

    async def refresh_token(self):
        PAYLOAD = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": create_jwt(self.cred_path)
        }
        self.token_expiration_time = datetime.datetime.now().timestamp() + 3500

        async with self.session.post(url="https://oauth2.googleapis.com/token",
                                params={"content-Type": "application/x-www-form-urlencoded"},
                                data=PAYLOAD) as response:
            self.token = json.loads(await response.text())["access_token"]
            self.session._default_headers = {'Authorization': f'Bearer {self.token}'}

    async def ensure_valid_token(self):
        if self.token:
            if datetime.datetime.now().timestamp() < self.token_expiration_time:
                return
        await self.refresh_token()

    def request(self, *args, **kwargs):
        self.concurrent_requests += 1
        return AsyncRequest(self, *args, **kwargs)

    def open(self, file_name, mode='r'):
        return AsyncFile(self, file_name, mode)

    def resumable_upload(self, content_length, *_, **kwargs):
        return ResumableUploadSession(self, content_length, **kwargs)

    def clear_cache(self):
        if os.path.exists(f"{parent_directory}/asyncache") and self.cache:
            shutil.rmtree(f"{parent_directory}/asyncache", ignore_errors=True)
        os.makedirs(f"{parent_directory}/asyncache")

    async def get(self, file_id, fields=None, download=True):
        params = f"?{'alt=media' if download else ''}" + \
                 f"{'&' if fields and download else ''}" + \
                 f"{('fields=' + ','.join(fields)) if fields else ''}"
        request_data = {
            'method': 'GET',
            'url': f'https://www.googleapis.com/drive/v3/files/{file_id}' + params
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def list(self, *_, **params):
        if 'q' in params:
            params['q'] = params['q'].replace(' ', '+').replace('=', '%3d').replace('\'', '%27')
        params = '?' + '&'.join('{}={}'.format(k,v) for k,v in params.items())
        request_data = {
            'method': 'GET',
            'url': f'https://www.googleapis.com/drive/v3/files{params}'
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def delete(self, file_id):
        request_data = {
            'method': 'DELETE',
            'url': f'https://www.googleapis.com/drive/v2/files/{file_id}'
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def create(self, data=None, *_, **kwargs):

        upload_type = kwargs.get('upload_type', 'metadata')
        data, headers = self.request_types[upload_type](data=data, metadata=kwargs)

        request_data = {
            'method': 'POST',
            'url': f"https://www.googleapis.com/{'upload/' if data else ''}drive/v3/files",
            'params': f"uploadType={upload_type}",
            'headers': headers,
            'data': data
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def update(self, file_id, data=None, *_, **kwargs):

        upload_type = kwargs.get('upload_type', 'metadata')
        data, headers = self.request_types[upload_type](data, kwargs)

        request_data = {
            'method': 'PATCH',
            'url': f"https://www.googleapis.com/{'upload/' if data else ''}drive/v3/files/{file_id}",
            'params': f"uploadType={upload_type}",
            'headers': headers,
            'data': data
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    def media_request(self, data, *_, **__):
        if type(data) == str:
            data = bytes(data, encoding='utf-8')
        headers = {
            'Content-Length': str(len(data)),
            'Content-Type': 'application/octet-stream'
        }
        return data, headers

    def metadata_request(self, metadata, *_, **__):
        metadata = json.dumps(metadata).encode('utf-8')
        headers = {
             'Content-Length': str(len(metadata)),
             'Content-Type': 'application/json'
        }
        return metadata, headers

    def multipart_request(self, data, metadata, *_, **__):
        if type(data) == str:
            data = bytes(data, encoding='utf-8')

        boundary = b"------123456"
        delim = b"\n--" + boundary + b"\n"
        closing = b"\n--" + boundary + b"--"

        data = delim + \
            b"Content-Type: application/json; charset=UTF-8\n\n" + \
            json.dumps(metadata).encode("utf-8") + \
            delim + \
            b"Content-Type: " + metadata.get("mimeType", "application/octet-stream").encode("utf-8") + b"\n\n" + \
            data + closing

        headers = {
            "Content-Type": "multipart/related; boundary='" +
            boundary.decode("utf-8") + "'",
            "Content-Length": str(len(data))
        }
        return data, headers
