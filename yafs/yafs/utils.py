import re


def extract_numeric_and_non_numeric(s):
    # Find all non-numeric characters (prefix and suffix)
    non_numeric = "".join(re.findall(r"\D+", s))
    # Find all numeric characters
    numeric = "".join(re.findall(r"\d+", s))
    return numeric, non_numeric


def insert_space_before_capital(s):
    return re.sub(r"(?<!\s)(?=[A-Z])", " ", s)
