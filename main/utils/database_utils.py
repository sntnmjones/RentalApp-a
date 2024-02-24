from main.models import Address, Review
import logging

logger = logging.getLogger()


def get_address_pk(full_address):
    """
    Get Address primary key for an address
    """
    addresses = Address.objects.filter(full_address=full_address)
    if addresses == 0:
        return None
    elif len(addresses) > 1:
        raise SystemError("More than one address result")
    return addresses[0].pk


def get_address_pk(full_address) -> Address:
    if address_pk_exists(full_address):
        return Address.objects.get(full_address=full_address)
    return None


def address_pk_exists(full_address) -> bool:
    return Address.objects.filter(full_address=full_address).exists()


def get_reviews(address_pk):
    return Review.objects.filter(address_id=address_pk)

def user_reviewed_address(full_address, user) -> bool:
    if address_pk_exists(full_address):
        address_pk = get_address_pk(full_address)
        reviews = get_reviews(address_pk)
        for review in reviews:
            if review.user == user:
                return True

    return False
