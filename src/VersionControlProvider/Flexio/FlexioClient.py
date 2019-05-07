from __future__ import annotations

from types import LambdaType
from typing import Dict, List

import requests
from requests import Response

from Core.ConfigHandler import ConfigHandler
from VersionControlProvider.Flexio.FlexioRessource import FlexioRessource


class Range:
    total: int = 0
    offset: int = 0
    limit: int = 0
    accept_range: int = 0

    def to_content_range(self) -> str:
        return '{offset!s}-{limit!s}'.format(offset=self.offset, limit=self.limit)

    @staticmethod
    def from_header_response(content_range: str) -> Range:
        a: List[str] = content_range.split('/')
        b: List[str] = a[0].split('-')
        r: Range = Range()
        r.total = int(a[-1])
        r.offset = int(b[0])
        r.limit = int(b[-1])
        return r


class FlexioClient:
    BASE_URL: str = 'https://my.flexio.io/api'
    CONTENT_RANGE = 'Content-Range'
    AUTHORIZATION = 'Authorization'
    ACCEPT_RANGE = 'Accept-Range'

    def __init__(self, config_handler: ConfigHandler):
        self.__config_handler: ConfigHandler = config_handler

    def __auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        if self.__config_handler.config.flexio.user_token:
            headers[self.AUTHORIZATION] = 'Bearer {user_token!s}'.format(
                user_token=self.__config_handler.config.flexio.user_token)
        else:
            raise AttributeError('No user token')
        return headers

    def __with_content_range(self, headers: Dict[str, str], range: Range) -> Dict[str, str]:
        headers[self.CONTENT_RANGE] = range.to_content_range()
        return headers

    def post_record(self, record: FlexioRessource) -> Response:
        url: str = '/'.join([self.BASE_URL, 'record', record.RESOURCE_ID])
        return requests.post(url, json=record.to_api_dict(), headers=self.__auth({}))

    def get_records(self, record: FlexioRessource, range: Range) -> Response:
        url: str = '/'.join([self.BASE_URL, 'record', record.RESOURCE_ID, 'paginate'])
        return requests.get(url, headers=self.__auth(self.__with_content_range({}, range)))

    # def get_user(self)->Response:

    def get_total(self, resource: FlexioRessource) -> Range:
        url: str = '/'.join([self.BASE_URL, 'record', resource.RESOURCE_ID, 'paginate'])
        range_min: Range = Range()
        range_min.offset = 0
        range_min.limit = 1

        resp: Response = requests.get(url, headers=self.__auth(self.__with_content_range({}, range_min)))
        # print(resp.status_code)
        # print(resp.headers)
        # print(resp.json())
        if not resp.status_code in [200, 206]:
            raise ConnectionError

        headers: dict = resp.headers
        range: Range = Range.from_header_response(headers.get(self.CONTENT_RANGE))
        range.accept_range = int(headers.get(self.ACCEPT_RANGE))
        return range

    def get_record(self, record: FlexioRessource) -> Dict:
        if record.id is not None:
            url: str = '/'.join([self.BASE_URL, 'record', record.SLUG, record.id])
            resp: Response = requests.get(url, headers=self.__auth())
            if not resp.status_code in [200]:
                raise ConnectionError
            return resp.json()
        else:
            recordDict: dict = record.to_api_dict()
            fullRange: Range = self.get_total(record)
            findedRecord: Dict = None
            resquestRange: Range = Range()
            resquestRange.accept_range = fullRange.accept_range
            resquestRange.offset = 0
            resquestRange.limit = fullRange.total if fullRange.total <= fullRange.accept_range else fullRange.accept_range
            while resquestRange.limit <= fullRange.total and findedRecord is None:
                resp: Response = self.get_records(record, resquestRange)
                if not resp.status_code in [200, 206]:
                    raise ConnectionError
                resp_part: Dict = resp.json()
                for r in resp_part:
                    shared_items = {k: r[k] for k in r if k in recordDict and r[k] == recordDict[k]}
                    if len(recordDict) == len(shared_items):
                        findedRecord = r
                        break
                resquestRange.offset = resquestRange.limit
                resquestRange.limit = resquestRange.limit + resquestRange.accept_range
            if findedRecord is None:
                raise FileNotFoundError
            return findedRecord
