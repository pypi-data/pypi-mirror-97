from pydantic import BaseModel


class WellsBaseModel(BaseModel):
    """
    The datamodel-code-generator program solves snake_case a bit opposite of
    what we want. We want to use `asset_id` in code, and `assetId` in json.
    Since it uses snake_case in the model and camelCase in the alias, we have to
    generate dict() and json() by alias, so that the output is true to the
    openapi spec.
    """

    def dict(self, by_alias=True, **kwargs):
        return super().dict(by_alias=by_alias, **kwargs)

    def json(self, by_alias=True, **kwargs):
        return super().json(by_alias=by_alias, **kwargs)
