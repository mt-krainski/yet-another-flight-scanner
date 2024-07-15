import asyncio
from functools import wraps

import click

from yafs.flights import get_flights


def as_coroutine(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--origin-airport",
    "-o",
    nargs=2,
    default=["Ottawa", "YOW"],
    help=(
        "Origin airport, this parameter must be passed as two values, e.g. "
        "`--origin-airport Ottawa YOW`"
    ),
)
@click.option(
    "--destination-airport",
    "-d",
    nargs=2,
    required=True,
    help=(
        "Destination airport, this parameter must be passed as two values, e.g. "
        "`--destination-airport Montreal YUL`"
    ),
)
@click.option("--departure-date", required=True)
@click.option("--return-date", required=True)
@as_coroutine
async def command(
    origin_airport,
    destination_airport,
    departure_date,
    return_date,
):
    data = await get_flights(
        origin_airport[0],
        origin_airport[1],
        destination_airport[0],
        destination_airport[1],
        departure_date,
        return_date,
    )
    print(data)


if __name__ == "__main__":
    command()
