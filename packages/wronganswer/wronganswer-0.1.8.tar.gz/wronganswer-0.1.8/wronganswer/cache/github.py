import os
import hashlib
import json
from tempfile import NamedTemporaryFile
from urllib.request import urlopen, Request, urlretrieve
from urllib.parse import urlencode
from .user import UserCacheStore
from .zip import ArchiveReader


class CacheHTTPClient:
    version_salt = '1.0'

    def __init__(self):
        base_url = (os.environ.get('ACTIONS_CACHE_URL', None) or os.environ.get('ACTIONS_RUNTIME_URL', None) or '').replace('pipelines', 'artifactcache')
        assert base_url, "Cache Service Url not found, unable to restore cache."
        self.base_url = base_url
        self.token = os.environ.get('ACTIONS_RUNTIME_TOKEN', '')
        self.version = os.environ.get('ACTIONS_CACHE_VERSION', '')

    def post_json(self, resource, body):
        response = urlopen(
            Request(
                self.get_cache_api_url(resource),
                method='POST',
                data=json.dumps(body).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json;api-version=6.0-preview.1"}))
        if response.code == 204:
            return
        assert response.headers.get_content_type() == "application/json"
        return json.load(response)

    def get_cache_api_url(self, resource):
        return f"{self.base_url}_apis/artifactcache/{resource}"

    def get_cache_version(self, path):
        return hashlib.new('sha256', "|".join([path, self.version_salt, self.version]).encode()).hexdigest()

    def reserve_cache(self, key, path):
        version = self.get_cache_version(path)
        response = self.post_json('caches', {"key": key, "version": version})
        return response.get("cacheId", None) or -1

    def upload_file(self, cache_id, path, size):
        with open(path, 'rb') as f:
            urlopen(
                Request(
                    self.get_cache_api_url(f"caches/{cache_id}"),
                    method='PATCH',
                    data=f,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Range": f"bytes 0-{size-1}/*",
                        "Authorization": f"Bearer {self.token}",
                        "Accept": "application/json;api-version=6.0-preview.1",
                        "Content-Length": f"{size}"}))

    def commit_cache(self, cache_id, file_size):
        self.post_json(f"caches/{cache_id}", {"size": file_size})

    def save_cache(self, cache_id, path):
        size = os.path.getsize(path)
        self.upload_file(cache_id, path, size)
        self.commit_cache(cache_id, size)

    def get_cache_entry(self, key, path):
        version = self.get_cache_version(path)
        resource = 'cache?' + urlencode({"keys": key, "version": version})
        response = urlopen(
            Request(
                self.get_cache_api_url(resource),
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/json;api-version=6.0-preview.1"}))
        if response.code == 204:
            return

        data = json.load(response)
        url = data.get("archiveLocation", None)
        assert url, "Cache not found"
        return url


class GithubActionCacheWriter:

    def __init__(self, client, path, key, writer):
        self.client = client
        self.path = path
        self.key = key
        self.writer = writer

    def save(self):
        self.writer.save()
        cache_id = self.client.reserve_cache(self.key, self.path)
        assert cache_id != -1, f"Unable to reserve cache with key {self.key}, another job may be creating this cache"
        self.client.save_cache(cache_id, self.path)

    def add(self, name):
        return self.writer.add(name)


class GithubActionCacheStore(UserCacheStore):

    def __init__(self):
        super().__init__()
        self.client = CacheHTTPClient()

    def get(self, oj, pid):
        cache = super().get(oj, pid)
        if cache is not None:
            return cache

        path = self._path(oj, pid)
        key = f'testcases|{oj}|{pid}'
        url = self.client.get_cache_entry(key, path)
        if url is None:
            return

        temp = os.path.join(self.basedir, "temp")
        os.makedirs(temp, exist_ok=True)
        f = NamedTemporaryFile(dir=temp)
        urlretrieve(url, f.name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        os.link(f.name, path)
        return ArchiveReader(path)

    def create(self, oj, pid):
        path = self._path(oj, pid)
        key = f'testcases|{oj}|{pid}'
        writer = super().create(oj, pid)
        return GithubActionCacheWriter(self.client, path, key, writer)
