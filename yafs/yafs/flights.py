from playwright.async_api import async_playwright

from yafs.utils import extract_numeric_and_non_numeric, insert_space_before_capital


async def _get_flights(
    browser,
    origin_airport_name,
    origin_airport_code,
    destination_airport_name,
    destination_airport_code,
    departure_date,
    return_date,
):
    page = await browser.new_page()
    await _go_to_google_flights(page)

    await _input_where_from(page, origin_airport_name, origin_airport_code)
    await _input_where_to(page, destination_airport_name, destination_airport_code)

    await _input_departure_date(page, departure_date)
    await _input_return_date(page, return_date)

    await _wait(page)
    await _press_escape(page)

    await _click_search(page)
    await _wait(page)

    await _hide_separate_tickets_filter(page)

    data = await _parse_results(
        page,
        origin_airport_name=origin_airport_name,
        origin_airport_code=origin_airport_code,
        destination_airport_name=destination_airport_name,
        destination_airport_code=destination_airport_code,
        departure_date=departure_date,
        return_date=return_date,
    )
    return data


async def _go_to_google_flights(page):
    await page.goto("https://www.google.com/travel/flights/search")  # noqa: SC200


async def _input_location(page, label, location_name, location_code):
    location = page.get_by_label(label, exact=True)
    await location.fill(location_name)
    await page.wait_for_timeout(2000)
    airport = page.get_by_text(location_code, exact=True)
    await airport.click()


async def _input_where_to(page, destination_name, destination_code):
    await _input_location(page, "Where to?", destination_name, destination_code)


async def _input_where_from(page, origin_name, origin_code):
    await _input_location(page, "Where from?", origin_name, origin_code)


async def _input_date(page, placeholder, date):
    date_input = page.get_by_placeholder(placeholder).nth(0)
    await page.wait_for_timeout(500)
    await date_input.fill(date)
    await page.wait_for_timeout(100)
    await date_input.press("Enter")
    await page.wait_for_timeout(100)


async def _input_departure_date(page, date):
    await _input_date(page, "Departure", date)


async def _input_return_date(page, date):
    await _input_date(page, "Return", date)


async def _wait(page, timeout=1000):
    await page.wait_for_timeout(timeout)


async def _press_escape(page):
    await page.keyboard.press("Escape")


async def _click_search(page):
    search = page.get_by_label("Search", exact=True)
    await page.wait_for_timeout(100)
    await search.click()


async def _hide_separate_tickets_filter(page):
    filters = page.get_by_label("All filters")
    await filters.click()
    await page.wait_for_timeout(1000)

    hide_separate = page.get_by_text("Hide separate tickets")
    await hide_separate.scroll_into_view_if_needed()
    await hide_separate.click()
    await page.wait_for_timeout(1000)
    await page.keyboard.press("Escape")


async def _parse_results(page, **kwargs):
    data = []
    for row in await page.get_by_role("listitem").all():
        texts = (await row.all_inner_texts())[0].split("\n")
        if "more flights" in texts[0]:
            continue
        direct_flight = False
        if "nonstop" in texts[6].lower():
            direct_flight = True

        price_str = texts[-2] if texts[-2] != "round trip" else texts[-3]
        price_components = extract_numeric_and_non_numeric(price_str)

        parsed_texts = {
            "departure": " ".join(texts[0].split()),
            "landing": " ".join(texts[2].split()),
            "airline": insert_space_before_capital(texts[3]),
            "duration": texts[4],
            "direct_flight": direct_flight,
            "price_currency": price_components[1],
            "price_unit": price_components[0],
        }
        if not direct_flight:
            parsed_texts["stops"] = texts[7]
        data.append(parsed_texts | kwargs)
    return data


async def get_flights(
    origin_airport_name: str,
    origin_airport_code: str,
    destination_airport_name: str,
    destination_airport_code: str,
    departure_date: str,
    return_date: str,
):
    """Get flights for the selected connection.

    Args:
        origin_airport_name (str): name of the origin airport
        origin_airport_code (str): code of the origin airport
        destination_airport_name (str): name of the destination airport
        destination_airport_code (str): code of the destination airport
        departure_date (str): date of departure, e.g. "21 Jul" or "21 July"
        return_date (str): return date, e.g. "28 Jul" or "28 July"

    Returns:
        list: List of dicts containing metadata of discovered connections
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        data = await _get_flights(
            browser,
            origin_airport_name,
            origin_airport_code,
            destination_airport_name,
            destination_airport_code,
            departure_date,
            return_date,
        )
        await browser.close()
    return data
