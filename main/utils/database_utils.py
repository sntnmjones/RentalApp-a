from main.models import Address, Property, Review
import logging

logger = logging.getLogger()


def get_address_pk(street, city, state):
    """
    Get Address primary key for an address
    """
    addresses = Address.objects.filter(
        city=city,
        state=state,
        street=street,
    )
    if addresses == 0:
        return None
    elif len(addresses) > 1:
        raise SystemError("More than one address result")
    return addresses[0].pk


def get_property_pk(street, city, state) -> Property:
    if property_pk_exists(street, city, state):
        return Property.objects.get(
            address__city=city,
            address__state=state,
            address__street=street,
        )
    return None


def property_pk_exists(street, city, state) -> bool:
    return Property.objects.filter(
        address__city=city,
        address__state=state,
        address__street=street
    ).exists()


def get_reviews(property_pk):
    return Review.objects.filter(property_id=property_pk)
