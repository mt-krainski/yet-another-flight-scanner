from datetime import datetime, timedelta

import pytest

from yafs.flights import get_flights

pytest_plugins = ("pytest_asyncio",)

DEPARTURE_DELTA = timedelta(days=7)
RETURN_DELTA = timedelta(days=14)


@pytest.mark.asyncio
async def test_end_to_end():
    today = datetime.now()
    departure = today + DEPARTURE_DELTA
    return_ = today + RETURN_DELTA

    data = await get_flights(
        "Ottawa",
        "YOW",
        "Montreal",
        "YUL",
        departure.strftime("%d %b"),
        return_.strftime("%d %b"),
    )

    assert data is not None
    assert len(data) > 0
