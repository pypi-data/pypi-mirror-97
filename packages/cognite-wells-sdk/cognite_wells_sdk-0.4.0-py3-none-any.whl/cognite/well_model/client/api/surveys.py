import logging
from typing import Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.models import Survey, SurveyData, SurveyDataRequest

logger = logging.getLogger("WellsAPI")


class SurveysAPI(BaseAPI):
    def __init__(self, wells_client: APIClient):
        super().__init__(wells_client)

        @extend_class(Survey)
        def data(survey) -> Optional[SurveyData]:
            return self.get_data(data_request=SurveyDataRequest(id=survey.id))

    def get_trajectory(self, wellbore_id: int) -> Optional[Survey]:
        """
        Get trajectory from a cdf asset id

        @param wellbore_id: cdf asset id
        @return: Survey object
        """
        path = self._get_path(f"/wellbores/{wellbore_id}/trajectory")
        response: Response = self.wells_client.get(path)
        survey: Survey = Survey.parse_obj(response.json())
        return survey

    def get_data(self, data_request: SurveyDataRequest) -> Optional[SurveyData]:
        """
        Get data from a survey id and other parameters

        @param data_request: data request object
        @return: SurveyData object
        """
        path = self._get_path("/surveys/data")
        response: Response = self.wells_client.post(path, data_request.json())
        survey_data: SurveyData = SurveyData.parse_obj(response.json())
        return survey_data
