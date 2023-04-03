from main.models import Address, Property, Review
import logging

logger = logging.getLogger()


def get_address_pk(street_number, street_name, city, state):
    """
    Get Address primary key for an address
    """
    addresses = Address.objects.filter(
        city=city,
        state=state,
        street_number=street_number,
        street_name=street_name,
    )
    reviews = []
    if addresses == 0:
        return None
    elif len(addresses) > 1:
        raise SystemError("More than one address result")
    return addresses[0].pk


def get_property_pk(street_number, street_name, city, state):
    return Property.objects.get(
        address__city=city,
        address__state=state,
        address__street_number=street_number,
        address__street_name=street_name,
    )


def get_reviews(property_pk):
    return Review.objects.filter(property_id=property_pk)
