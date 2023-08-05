from cognite.well_model.client._api_client import APIClient


class BaseAPI:
    def __init__(self, wells_client: APIClient):
        self.wells_client: APIClient = wells_client

    def _get_path(self, base_url: str) -> str:
        cluster = self.wells_client._config.cluster
        project = self.wells_client._config.project
        if cluster and cluster.requires_cluster_selection:
            return f"/{project}{base_url}?env={cluster}"
        return f"/{project}{base_url}"
