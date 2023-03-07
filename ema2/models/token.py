from datetime import datetime, timedelta

import pydantic


class TokenGetRequest(pydantic.BaseModel):
    username: str
    password: str


class TokenGetReponse(pydantic.BaseModel):
    access_token: str = pydantic.Field(alias="accessToken")
    refresh_token: str = pydantic.Field(alias="refreshToken")
    access_token_expiry: datetime = datetime.now() + timedelta(minutes=1)
    refresh_token_expiry: datetime = datetime.now() + timedelta(minutes=30)


class TokenRenewRequest(pydantic.BaseModel):
    refresh_token: str = pydantic.Field(alias="refreshToken")

    class Config:
        allow_population_by_field_name = True


class TokenRenewResponse(pydantic.BaseModel):
    access_token: str = pydantic.Field(alias="accessToken")
    refresh_token: str = pydantic.Field(alias="refreshToken")
    access_token_expiry: datetime = datetime.now() + timedelta(minutes=1)
    refresh_token_expiry: datetime = datetime.now() + timedelta(minutes=30)
