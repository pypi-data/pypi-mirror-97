import logging
from typing import List, Optional

from requests import Response

from cognite.well_model._asset_model import Asset
from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.api.surveys import SurveysAPI
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.models import Measurement, MeasurementType, Survey, Wellbore, WellIds

logger = logging.getLogger("WellboresAPI")


class WellboresAPI(BaseAPI):
    def __init__(self, wells_client: APIClient, survey_api: SurveysAPI):
        super().__init__(wells_client)
        self.survey_api = survey_api

        # wrap all wellbores with a lazy method
        @extend_class(Wellbore)
        def trajectory(wellbore) -> Optional[Survey]:
            return survey_api.get_trajectory(wellbore.id)

        @extend_class(Wellbore)
        def source_assets(wellbore, source_label: Optional[str] = None) -> List[Asset]:
            return self.get_sources(wellbore_id=wellbore.id, source_label=source_label)

    def get_by_id(self, wellbore_id: int) -> Wellbore:
        """
        Get wellbore from a cdf asset id

        @param wellbore_id: cdf asset id
        @return: Wellbore object
        """
        path: str = self._get_path(f"/wellbores/{wellbore_id}")
        response: Response = self.wells_client.get(url_path=path)
        wb: Wellbore = Wellbore.parse_raw(response.text)
        return wb

    def get_from_well(self, well_id: int) -> List[Wellbore]:
        """
        get wellbores from a well id

        @param well_id: well id of interest
        @return: wellbores that has the well of interest as parent
        """
        path: str = self._get_path(f"/wells/{well_id}/wellbores")
        response: Response = self.wells_client.get(url_path=path)
        return [Wellbore.parse_obj(x) for x in response.json()]

    def get_from_wells(self, well_ids: List[int]) -> List[Wellbore]:
        """
        Return multiple wellbores from multiple input well ids

        @param well_ids: list of well ids we want the wellbores from
        @return: list of wellbores
        """
        path: str = self._get_path("/wellbores/bywellids")
        ids = WellIds(items=well_ids)
        well_ids_serialized = ids.json()
        response: Response = self.wells_client.post(url_path=path, json=well_ids_serialized)
        return [Wellbore.parse_obj(x) for x in response.json()]

    def get_measurement(self, wellbore_id: int, measurement_type: MeasurementType) -> List[Measurement]:
        """
        retrieve measurements for a wellbore

        @param wellbore_id: The wellbore id of interest
        @param measurement_type: The measurement type of interest
        @return: list of measurements
        """
        path: str = self._get_path(f"/wellbores/{wellbore_id}/measurements/{measurement_type}")
        response: Response = self.wells_client.get(url_path=path)
        return [Measurement.parse_obj(x) for x in response.json()["items"]]

    def get_sources(self, wellbore_id: int, source_label: Optional[str] = None) -> List[Asset]:
        """
        Return all source assets associated to a wellbore

        @param wellbore_id: The wellbore id of interest
        @param source_label: the source label for the wellbore object
        @return: list of assets
        """
        path: str = f"/wellbores/{wellbore_id}/sources"
        if source_label is not None:
            path += f"/{source_label}"
        path = self._get_path(path)
        response: Response = self.wells_client.get(url_path=path)
        assets: List[Asset] = [Asset.parse_obj(x) for x in response.json()]
        return assets
