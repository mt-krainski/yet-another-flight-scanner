import asyncio
import json
from functools import wraps

import click
from slugify import slugify

from yafs.flights import get_flights

MAX_RETRIES = 10


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
@click.option(
    "--result-filename",
    required=False,
    help=(
        "Results will be stored in this file. If not provided, a combination of "
        "parameter names will be used"
    ),
)
@as_coroutine
async def yafs(
    origin_airport,
    destination_airport,
    departure_date,
    return_date,
    result_filename,
):
    for i in range(MAX_RETRIES):
        try:
            data = await get_flights(
                origin_airport[0],
                origin_airport[1],
                destination_airport[0],
                destination_airport[1],
                departure_date,
                return_date,
            )
        except Exception as e:
            print(
                f"Run failed due to {e}. This was attempt {i + 1}/{MAX_RETRIES}. "
                "Restarting..."
            )
        else:
            break
    else:
        raise Exception(f"Run failed {MAX_RETRIES} times. Aborting.")

    if result_filename is None:
        result_filename = (
            f"{origin_airport[1]}-{destination_airport[1]}-{slugify(departure_date)}-"
            f"{slugify(return_date)}.json"
        )

    with open(result_filename, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    yafs()
