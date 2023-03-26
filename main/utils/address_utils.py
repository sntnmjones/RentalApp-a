from django.core.validators import RegexValidator


# Google street address format in regex
def get_address_regex_validator() -> RegexValidator:
    """
    Produce a regex validator for street addresses in the Google street address format
    """
    return RegexValidator(
        regex=r"^\d{0,5}[-]?\d{0,3}\s{1}[a-zA-z\s]*((\s)Ln\.|Dr\.|St\.|Ct\.|Ave\.)?,\s[a-zA-z\s]*,\s[A-Z]{2}$",
        message='Please enter a valid street address in the format of "123 Main Street, AnyTown, CA"',
    )
