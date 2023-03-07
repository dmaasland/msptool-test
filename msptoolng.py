#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta

from ema2 import EsetMspAdministrator2
from ema2.enum import *
from ema2.models import *
from settings import *

CUSTOMERS: dict[str, dict[str, BillingReport]] = {}


async def selected_companies_products(
    ema: EsetMspAdministrator2, company_ids: list[str], from_date: str, to_date: str
):
    companies = await ema.usage_report_selected_companies_products(
        company_ids=company_ids, from_date=from_date, to_date=to_date
    )

    for company in companies.companies:
        parent = CUSTOMERS[company.company_id]["parent"]
        price_day = None

        print(f"{company.company_name}")

        for product in company.products:
            for category in parent.categories:
                if category.category_code == product.code:
                    price_day = category.price_day
                    break

            total_price = (
                round(price_day * product.seat_days, 5) if price_day is not None else "unknown"
            )

            print(f"|__{product.name}")
            print(f"      Seat days: {product.seat_days}")
            print(f"      Seats: {product.seats}")
            print(f"      Seat price: {price_day}")
            print(f"      Total Price: {total_price}")


async def descendants(
    ema: EsetMspAdministrator2, report: BillingReport
) -> CompanyDescendantsResponse:
    descendants = await ema.company_descendants(
        company_id=report.company_id, entity_type=EntityType.MANAGED_BY_MSP
    )

    for company in descendants.companies:
        CUSTOMERS.update({company.public_id: {"parent": report}})
    return descendants


def split_customers() -> list[list[str]]:
    """
    Split the customer list into lists of 450 items
    """
    SPLIT = 450
    customer_list = list(CUSTOMERS.keys())
    return [
        customer_list[i * SPLIT : (i + 1) * SPLIT]
        for i in range((len(customer_list) + SPLIT - 1) // SPLIT)
    ]


def get_dates() -> tuple[str, str, str, str]:
    last_month = datetime.today().replace(day=1) - timedelta(days=1)
    year = last_month.strftime("%Y")
    month = last_month.strftime("%m")
    last_day = last_month.strftime("%d")
    first_day = last_month.replace(day=1).strftime("%d")

    from_date = f"{year}-{month}-{first_day}"
    to_date = f"{year}-{month}-{last_day}"

    return from_date, to_date, year, month


async def main() -> None:
    from_date, to_date, year, month = get_dates()

    async with EsetMspAdministrator2(username=USERNAME, password=PASSWORD, verify=False) as ema:
        my_company = await ema.billing_report_my_company(int(year), int(month))

        async with asyncio.TaskGroup() as tg:
            for report in my_company.report:
                # Skip companies without revenue
                if report.total_source == 0.0:
                    continue

                tg.create_task(descendants(ema, report))

        async with asyncio.TaskGroup() as tg:
            customer_chunks = split_customers()
            for chunk in customer_chunks:
                tg.create_task(
                    selected_companies_products(ema, chunk, from_date=from_date, to_date=to_date)
                )


if __name__ == "__main__":
    asyncio.run(main())
