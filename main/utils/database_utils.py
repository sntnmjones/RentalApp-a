from collections import defaultdict
from main.models import Address, Review, State, City, Country
from django.db.models.query import QuerySet

import logging

logger = logging.getLogger()

###############################################################################
# ADDRESS TABLE
###############################################################################
def get_address_pk(full_address) -> Address | None:
    if address_pk_exists(full_address):
        return Address.objects.get(full_address=full_address)
    return None


def address_pk_exists(full_address) -> bool:
    return Address.objects.filter(full_address=full_address).exists()
###############################################################################
# COUNTRY TABLE
###############################################################################
def save_country(country: str) -> Country | None:
    if country:
        return Country.objects.get_or_create(name=country)[0]


def get_countries():
    return Country.objects.all().values_list('name', flat=True)


def get_country(country: str) -> Country:
    return Country.objects.get(name=country)
###############################################################################
# STATE TABLE
###############################################################################
def save_state(country: Country, state: str) -> State | None:
    if country and state:
        return State.objects.get_or_create(country=country, name=state)[0]
    return None


def get_states(country: str):
    country_obj = Country.objects.get(name=country)
    return State.objects.filter(country=country_obj).values_list('name', flat=True)


def get_state(state: str, country: Country) -> State:
    return State.objects.get(country=country, name=state)
###############################################################################
# CITY TABLE
###############################################################################
def save_city(state: State, city: str) -> City | None:
    if state and city:
        return City.objects.get_or_create(state=state, name=city)[0]
    return None


def get_cities(state: State):
    state_obj = State.objects.get(name=state)
    return City.objects.filter(state=state_obj).values_list('name', flat=True)


def get_city(city: str, state: State) -> City:
    return City.objects.get(name=city, state=state)
###############################################################################
# REVIEW TABLE
###############################################################################
def get_reviews(address_pk: Address):
    return Review.objects.filter(address_id=address_pk)


def get_city_reviews(city, state, country):
    country_obj = get_country(country)
    state_obj = get_state(state, country_obj)
    city_obj = get_city(city, state_obj)
    addresses = Address.objects.filter(city=city_obj)
    reviews = {}
    for address in addresses:
        address_reviews = get_reviews(address.pk)
        if address_reviews:
            reviews[address.full_address] = address_reviews
    if len(reviews) > 0:
        return reviews
    return None
