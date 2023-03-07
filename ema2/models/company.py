import pydantic

from ..enum import *
from ._functions import to_lower_camel


class Companies(pydantic.BaseModel):
    name: str
    public_id: str
    type: EntityType
    status: int
    email: str

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class CompanyDescendantsRequest(pydantic.BaseModel):
    skip: int
    take: int
    company_id: str
    entity_type: EntityType

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class CompanyDescendantsResponse(pydantic.BaseModel):
    companies: list[Companies]
