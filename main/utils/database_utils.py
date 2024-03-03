from collections import defaultdict
from main.models import Address, Review, State, City, Country
from django.core.cache import cache

import logging

logger = logging.getLogger()

###############################################################################
# ADDRESS TABLE
###############################################################################
def get_address_pk(full_address) -> Address:
    if full_address:
        cached = cache.get(f'address_{full_address}')
        if not cached:
            address_pk = Address.objects.get(full_address=full_address)
            cache.set(f'address_{full_address}', address_pk)
        return cache.get(f'address_{full_address}')


def address_pk_exists(full_address) -> bool:
    return Address.objects.filter(full_address=full_address).exists()
###############################################################################
# COUNTRY TABLE
###############################################################################
def save_country(country: str) -> Country | None:
    if country:
        return Country.objects.get_or_create(name=country)[0]


def get_countries():
    cached = cache.get('countries')
    if not cached:
        countries = Country.objects.all().values_list('name', flat=True)
        cache.set('countries', countries)
    return cache.get('countries')


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
    if country:
        cached = cache.get(f'{country}_states')
        if not cached:
            country_obj = Country.objects.get(name=country)
            states = State.objects.filter(country=country_obj).values_list('name', flat=True)
            cache.set(f'{country}_states', states)
        return cache.get(f'{country}_states')


def get_state(state: str, country: Country) -> State:
    return State.objects.get(country=country, name=state)
###############################################################################
# CITY TABLE
###############################################################################
def save_city(state: State, city: str) -> City | None:
    if state and city:
        return City.objects.get_or_create(state=state, name=city)[0]
    return None


def get_cities(state: str, country: str):
    cached = cache.get(f'{state}_{country}_cities')
    if not cached:
        country_obj = Country.objects.get(name=country)
        state_obj = State.objects.get(name=state, country=country_obj)
        cities = City.objects.filter(state=state_obj).values_list('name', flat=True)
        cache.set(f'{state}_{country}_cities', cities)
    return cache.get(f'{state}_{country}_cities')


def get_city(city: str, state: State) -> City:
    return City.objects.get(name=city, state=state)
###############################################################################
# REVIEW TABLE
###############################################################################
def get_reviews(address_pk: Address):
    cached = cache.get(f'{address_pk}_reviews')
    if not cached:
        reviews = Review.objects.filter(address_id=address_pk)
        cache.set(f'{address_pk}_reviews', reviews)
    return cache.get(f'{address_pk}_reviews')

def get_city_reviews(city, state, country):
    cached = cache.get(f'{city}_{state}_{country}_reviews')
    if not cached:
        country_obj = get_country(country)
        state_obj = get_state(state, country_obj)
        city_obj = get_city(city, state_obj)
        addresses = Address.objects.filter(city=city_obj)
        reviews = {}
        for address in addresses:
            address_reviews = get_reviews(address.pk)
            if address_reviews:
                reviews[address.full_address] = address_reviews
        cache.set(f'{city}_{state}_{country}_reviews', reviews)
    return cache.get(f'{city}_{state}_{country}_reviews')
