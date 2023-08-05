from dataclasses import field
from typing import Callable, Dict, List, Optional, Union

import cognite
from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.ingestion import IngestionAPI
from cognite.well_model.client.api.surveys import SurveysAPI
from cognite.well_model.client.api.wellbores import WellboresAPI
from cognite.well_model.client.api.wells import WellsAPI
from cognite.well_model.client.utils._client_config import ClientConfig, Cluster


class CogniteWellsClient:
    """
    All services are made available through this object. See examples below.

    @param api_key (str): API key
    @param project (str): Project. Defaults to project of given API key.
    @param client_name (str): A user-defined name for the client. Used to identify number of unique applications/scripts
            running on top of CDF.
    @param base_url (str): Base url to send requests to.
    @param max_workers (int): Max number of workers to spawn when parallelizing data fetching. Defaults to 10.
    @param headers (Dict): Additional headers to add to all requests.
    @param timeout (int): Timeout on requests sent to the api. Defaults to 30 seconds.
    @param token (Union[str, Callable]): token (Union[str, Callable[[], str]]): A jwt or method which takes no arguments
            and returns a jwt to use for authentication.
    @param token_url (str): Optional url to use for token generation
    @param token_client_id (str): Optional client id to use for token generation.
    @param token_client_secret (str): Optional client secret to use for token generation.
    @param token_scopes (list): Optional list of scopes to use for token generation.
    @param token_custom_args (Dict): Optional additional arguments to use for token generation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        project: Optional[str] = None,
        cluster: Cluster = None,
        client_name: str = None,
        base_url: Optional[str] = None,
        max_workers: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        token: Optional[Union[str, Callable[[], str], None]] = None,
        token_url: Optional[str] = None,
        token_client_id: Optional[str] = None,
        token_client_secret: Optional[str] = None,
        token_scopes: Optional[List[str]] = None,
        token_custom_args: Dict[str, str] = field(default_factory=dict),
    ):
        self._config = ClientConfig(
            api_key=api_key,
            project=project,
            cluster=cluster,
            client_name=client_name,
            base_url=base_url,
            max_workers=max_workers,
            headers=headers,
            timeout=timeout,
            token=token,
            token_url=token_url,
            token_client_id=token_client_id,
            token_client_secret=token_client_secret,
            token_scopes=token_scopes,
            token_custom_args=token_custom_args,
        )

        self._api_client = APIClient(self._config, cognite_client=self)
        self.surveys = SurveysAPI(wells_client=self._api_client)
        self.wellbores = WellboresAPI(wells_client=self._api_client, survey_api=self.surveys)
        self.wells = WellsAPI(wells_client=self._api_client, wellbores_api=self.wellbores)
        self.ingestion = IngestionAPI(wells_client=self._api_client)

    @property
    def version(self) -> str:
        """
        Getter to return the current version of the SDK from the root __init__.py script
        @return: a string representation of the version number
        """
        return cognite.__version__

    @property
    def config(self) -> ClientConfig:
        """Returns a config object containing the configuration for the current client.
        @return: the configuration object.
        """
        return self._config
