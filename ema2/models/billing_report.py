import pydantic

from ._functions import to_lower_camel


class BillingReportCategory(pydantic.BaseModel):
    category_code: int
    category: str
    seat_days: int
    tier: str
    pricelist: str
    price_day: float
    price_month: float
    total_source: float
    discounted_seat_dats: int | None
    discounted_price_final: int | None
    discounted: bool
    seats: int

    class Config:
        alias_generator = to_lower_camel


class BillingReport(pydantic.BaseModel):
    company_name: str
    company_id: str
    currency: str | None
    custom_identifier: str | None
    total_source: float
    year: int
    month: int
    categories: list[BillingReportCategory]

    class Config:
        alias_generator = to_lower_camel


class BillingReportDivisionsUnderSelectedDistributorRequest(pydantic.BaseModel):
    year: int
    month: int
    division_ids: list[str] = pydantic.Field(alias="divisionIds")

    class Config:
        allow_population_by_field_name = True


class BillingReportMyCompanyRequest(pydantic.BaseModel):
    year: int
    month: int


class BillingReportMyCompanyResponse(pydantic.BaseModel):
    report: list[BillingReport]
