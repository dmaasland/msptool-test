import pydantic


class VersionResponse(pydantic.BaseModel):
    version: str
