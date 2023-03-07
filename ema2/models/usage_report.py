import pydantic

from ._functions import *


class UsageReportProducts(pydantic.BaseModel):
    code: int
    name: str
    license_type: int
    seat_days: int
    seats: int

    class Config:
        alias_generator = to_lower_camel


class UsageReportCompanies(pydantic.BaseModel):
    products: list[UsageReportProducts]
    company_id: str
    company_name: str
    total_usage: int
    total_seats: int

    class Config:
        alias_generator = to_lower_camel


class UsageReportMonthlyProductsRequest(pydantic.BaseModel):
    skip: int
    take: int
    from_date: str = pydantic.Field(alias="from")
    to_date: str = pydantic.Field(alias="to")
    company_id: str

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class UsageReportMonthlyProductsResponse(pydantic.BaseModel):
    products: list[UsageReportProducts]


class UsageReportSelectedCompaniesProductsRequest(pydantic.BaseModel):
    skip: int
    take: int
    from_date: str = pydantic.Field(alias="from")
    to_date: str = pydantic.Field(alias="to")
    company_ids: list[str]

    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True


class UsageReportSelectedCompaniesProductsResponse(pydantic.BaseModel):
    companies: list[UsageReportCompanies]
