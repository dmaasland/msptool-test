import asyncio
from datetime import datetime, timedelta
from urllib.parse import urljoin

import httpx

from .const import *
from .decorators import *
from .enum import *
from .models import *


class EsetMspAdministrator2:
    def __init__(self, username: str, password: str, verify: bool = True):
        self.client = httpx.AsyncClient(verify=verify, timeout=HTTP_TIMEOUT)
        self.username = username
        self.password = password
        self.token_info: TokenGetReponse | None = None
        self.limit = asyncio.Semaphore(HTTP_LIMIT)

    async def __aenter__(self):
        await self.authenticate()
        return self

    async def __aexit__(self, type, value, traceback):
        await self.client.aclose()

    async def version(self) -> VersionResponse:
        return VersionResponse(**(await self.api_request(VERSION_BASE)).json())

    async def billing_report_divisions_under_selected_distributor(
        self, year: int, month: int, division_ids: list[str]
    ) -> None:
        json_data = BillingReportDivisionsUnderSelectedDistributorRequest(
            year=year, month=month, division_ids=division_ids  # pyright: ignore
        ).dict(by_alias=True)

        await self.api_request(
            BILLING_REPORT_DIVISION_UNDER_SELECTED_DISTRIBUTOR,
            method=HttpMethod.POST,
            json_data=json_data,
        )

    async def billing_report_my_company(
        self, year: int, month: int
    ) -> BillingReportMyCompanyResponse:
        json_data = BillingReportMyCompanyRequest(year=year, month=month).dict()

        response = BillingReportMyCompanyResponse(
            **(
                await self.api_request(
                    BILLING_REPORT_MY_COMPANY, method=HttpMethod.POST, json_data=json_data
                )
            ).json()
        )

        return response

    async def company_descendants(
        self,
        company_id: str,
        entity_type: EntityType = EntityType.ANY,
        skip: int = 0,
        take: int = 100,
    ) -> CompanyDescendantsResponse:
        json_data = CompanyDescendantsRequest(
            skip=skip, take=take, company_id=company_id, entity_type=entity_type
        ).dict(by_alias=True)
        try:
            response = CompanyDescendantsResponse(
                **(
                    await self.api_request(
                        COMPANY_DESCENDANTS, method=HttpMethod.POST, json_data=json_data
                    )
                ).json()
            )
        except httpx.HTTPStatusError:
            response = CompanyDescendantsResponse(companies=[])
        return response

    @ratelimit(time=15, total=15)
    async def usage_report_monthly_products(
        self,
        company_id: str,
        from_date: str,
        to_date: str,
        codes: list | None = None,
        skip: int = 0,
        take: int = 100,
    ) -> UsageReportMonthlyProductsResponse:
        if codes is None:
            codes = []

        json_data = UsageReportMonthlyProductsRequest(
            company_id=company_id,
            skip=skip,
            take=take,
            from_date=from_date,  # pyright: ignore
            to_date=to_date,  # pyright: ignore
        ).dict(by_alias=True)

        response = UsageReportMonthlyProductsResponse(
            **(
                await self.api_request(
                    USAGE_REPORT_MONTHLY_PRODUCTS, method=HttpMethod.POST, json_data=json_data
                )
            ).json()
        )

        return response

    @ratelimit(time=15, total=30)
    async def usage_report_selected_companies_products(
        self, company_ids: list[str], from_date: str, to_date: str, skip: int = 0, take: int = 100
    ) -> UsageReportSelectedCompaniesProductsResponse:
        json_data = UsageReportSelectedCompaniesProductsRequest(
            company_ids=company_ids,
            skip=skip,
            take=take,
            from_date=from_date,  # pyright: ignore
            to_date=to_date,  # pyright: ignore
        ).dict(by_alias=True)

        response = UsageReportSelectedCompaniesProductsResponse(
            **(
                await self.api_request(
                    USAGE_REPORT_SELECTED_COMPANIES_PRODUCTS,
                    method=HttpMethod.POST,
                    json_data=json_data,
                )
            ).json()
        )

        return response

    async def token_get(self) -> TokenGetReponse:
        json_data = TokenGetRequest(username=self.username, password=self.password).dict()
        token_info = TokenGetReponse(
            **(
                await self.api_request(TOKEN_GET, method=HttpMethod.POST, json_data=json_data)
            ).json()
        )

        return token_info

    async def token_renew(self) -> TokenRenewResponse:
        if self.token_info is None:
            raise ValueError

        json_data = TokenRenewRequest(
            refresh_token=self.token_info.refresh_token  # pyright: ignore
        ).dict(by_alias=True)
        token_info = TokenRenewResponse(
            **(
                await self.api_request(TOKEN_RENEW, method=HttpMethod.POST, json_data=json_data)
            ).json()
        )

        return token_info

    async def authenticate(self) -> None:
        if self.token_info is None:
            self.token_info = await self.token_get()

        if self.token_info.refresh_token_expiry < (datetime.now() - timedelta(minutes=1)):
            self.token_info.refresh_token = (await self.token_get()).refresh_token

        if self.token_info.access_token_expiry < (datetime.now() - timedelta(seconds=10)):
            self.token_info.access_token = (await self.token_renew()).access_token

    async def api_request(
        self,
        endpoint: str,
        json_data: dict | None = None,
        method: HttpMethod = HttpMethod.GET,
    ) -> httpx.Response:
        resp = await self._raw_request(uri=endpoint, method=method, json_data=json_data)
        return resp

    async def _raw_request(
        self, uri: str, json_data: dict | None = None, method: HttpMethod = HttpMethod.GET
    ) -> httpx.Response:
        if not type(method) == HttpMethod:
            raise ValueError

        if self.token_info is not None:
            self.client.headers.update({"Authorization": f"Bearer {self.token_info.access_token}"})

        kwargs = {}

        if json_data:
            kwargs.update({"json": json_data})

        url = urljoin(BASE_URL, uri)
        req = getattr(self.client, method)

        async with self.limit:
            resp = await req(url, **kwargs)

            resp.raise_for_status()
            return resp
