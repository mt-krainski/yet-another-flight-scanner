import re
from typing import Tuple


def extract_numeric_and_non_numeric(s: str) -> Tuple[int, str]:
    """Take the input argument and split out numeric and non-numeric components.

    E.g. this can take in value such as "CA$100" and it will return (100, "CA$")

    Args:
        s (str): string to be split

    Returns:
        Tuple[int, str]: tuple where the first value is the numeric component
            and the second value is the non-numeric component
    """
    # Find all non-numeric characters (prefix and suffix)
    non_numeric = "".join(re.findall(r"\D+", s))
    # Find all numeric characters
    numeric = "".join(re.findall(r"\d+", s))
    return int(numeric), non_numeric


def insert_space_before_capital(s: str) -> str:
    """Insert space before capital letter if not already there.

    This function will insert spaces before capital letters. This is meant to break up
    badly formatted strings, e.g. "TestTest" into "Test Test"

    Args:
        s (str): string to be broken up

    Returns:
        str: result
    """
    return re.sub(r"(?<!\s)(?=[A-Z])", " ", s)
