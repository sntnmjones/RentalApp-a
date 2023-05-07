from main.models import Address, Review
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


def get_address_pk(street, city, state) -> Address:
    if address_pk_exists(street, city, state):
        return Address.objects.get(
            city=city,
            state=state,
            street=street,
        )
    return None


def address_pk_exists(street, city, state) -> bool:
    return Address.objects.filter(
        city=city,
        state=state,
        street=street
    ).exists()


def get_reviews(address_pk):
    return Review.objects.filter(address_id=address_pk)
