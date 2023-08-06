import asyncio
import yarl
from typing import NamedTuple

import aiohttp

from . import constants
from .exceptions import CianStatusException


class Result(NamedTuple):
    pass


class Search:
    def __init__(
            self,
            client: CianClient,
            region: constants.Region,
            ad_type: constants.AdType,
            rooms: Sequence[constants.Room] = (),
            building_status: Optional[constants.BuildingStatus] = None,
            object_types: Sequence[constants.ObjectType] = (),
            advertiser: Optional[constants.Advertiser] = None,
    ):
        self._client = client
        self._loop = asyncio.get_event_loop()
        self._cache_results = []
        self._results_count = None

        self.region = region
        self.ad_type = ad_type
        self.rooms = rooms
        self.building_status = building_status
        self.object_types = object_types
        self.advertiser = advertiser

        self.page = 0

    def __len__(self):
        return self._results_count

    async def __aiter__(self):
        return self

    def __iter__(self):
        return self

    async def __anext__(self):
        if not self._cache_results:
            self.page += 1
            request_data = self._get_request_data(self)
            response_data = await self.client.a_request(request_data)
            self._results_count = response_data["aggregatedCount"] 
            self._cache_results = list(map(self._get_result, response_data["offersSerialized"]))

        return self._cache_results.pop(0)

    def __next__(self):
        return self._loop.run_until_complete(self.__anext__())

    @staticmethod
    def _get_result(data):
        return data

    def _get_request_data(self):
        data = {
            "_type": self.ad_type.value,
            "engine_version": {"type": "term", "value": 2},
            "page": {"type": "term", "value": self.page},
            "region": {"types": "term", "value": [self.region.value]},
        }
        if self.rooms:
            data["room"] = {
                "type": "terms",
                "value": [room.value for room in self._rooms],
            }
        if self.building_status:
            data["building_status"] = {"type": "term", "value": self.building_status.value}
        if self.object_type:
            data["object_type"] = {
                "type": "terms",
                "value": [object_type.value for object_type in self.object_types],
            }
        if self.advertiser:
            data["suburban_offer_filter"] = {"type": "term", "value": self.advertiser.value}

        return data


class CianClient:
    API_URL = yarl.URL("https://api.cian.ru/search-offers/v2/search-offers-desktop/")

    def __init__(self):
        self._session = aiohttp.ClientSession()
        self._loop = asyncio.get_event_loop()

    def __del__(self):
        self._loop.run_until_complete(self._session.close())
        self._loop.close()

    async def a_request(self, data: dict):
        request_args = {
            "url": self.API_URL,
            "json": {"jsonQuery": data},
        }
        async with self._session.post(**request_args) as response:
            payload = await response.json()
            status = payload["status"]
            if status != "ok":
                raise CianStatusException(status)
            return payload["data"]

    def request(self, data: dict):
        return self._loop.run_until_complete(self.a_request(data=data))

    def search(self, *args, **kwargs):
        return Search(self, *args, **kwargs)
