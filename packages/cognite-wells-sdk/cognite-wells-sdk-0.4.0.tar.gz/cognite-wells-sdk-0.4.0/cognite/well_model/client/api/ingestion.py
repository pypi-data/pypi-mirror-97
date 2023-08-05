import logging
from typing import List

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.models import (
    CasingIngestion,
    CasingIngestionItems,
    GetSequenceDTO,
    Well,
    Wellbore,
    WellboreIngestion,
    WellboreIngestionItems,
    WellIngestion,
    WellIngestionItems,
)

logger = logging.getLogger("WellsAPI")


class IngestionAPI(BaseAPI):
    def __init__(self, wells_client: APIClient):
        super().__init__(wells_client)

    def ingest_casings(self, ingestions: List[CasingIngestion]) -> List[GetSequenceDTO]:
        path = self._get_path("/ingestion/casings")
        json = CasingIngestionItems(__root__=ingestions).json()
        response: Response = self.wells_client.post(path, json)
        return [GetSequenceDTO.parse_obj(r) for r in response.json()]

    def ingest_wells(self, ingestions: List[WellIngestion]) -> List[Well]:
        path = self._get_path("/ingestion/wells")
        json = WellIngestionItems(__root__=ingestions).json()
        response: Response = self.wells_client.post(path, json)
        return [Well.parse_obj(x) for x in response.json()]

    def ingest_wellbores(self, ingestions: List[WellboreIngestion]) -> List[Wellbore]:
        path = self._get_path("/ingestion/wellbores")
        json = WellboreIngestionItems(__root__=ingestions).json()
        response: Response = self.wells_client.post(path, json)
        return [Wellbore.parse_obj(x) for x in response.json()]
