from typing import Tuple, List
from django.core.validators import RegexValidator


def get_address_regex_validator() -> RegexValidator:
    """
    Produce a regex validator for street addresses in the Google street address format
    """
    return RegexValidator(
        regex=r"^\d{0,5}[-]?\d{0,3}\s{1}[a-zA-z\s]*((\s)Ln\.|Dr\.|St\.|Ct\.|Ave\.)?,\s[a-zA-z\s]*,\s[A-Z]{2}$",
        message='Please enter a valid street address in the format of "123 Main Street, AnyTown, CA"',
    )


def split_street(street: str) -> Tuple[str, str]:
    """
    Separate the street name and number, leaving dashes in place for storage
    """
    parts: List[str] = street.split("-")
    street_name_parts: List[str] = []
    while parts and not parts[-1].isdigit():
        street_name_parts.append(parts.pop())
    street_name: str = "-".join(reversed(street_name_parts))
    street_number: str = "-".join(parts)
    return street_number, street_name


def pretty_print_address(string: str) -> str:
    """
    Replace dashes with spaces and uppercase words
    """
    return string.replace("-", " ").title()


def get_address_dict(address: str) -> dict[str, str]:
    """
    Split address into a map of address fields
    """
    address_fields = address.split(", ")
    address_fields = [f.replace(" ", "-").lower() for f in address_fields]
    street_number, street_name = split_street(address_fields[0])
    return {
        "street": address_fields[0],
        "city": address_fields[1],
        "state": address_fields[2],
        "street_number": street_number,
        "street_name": street_name,
    }
