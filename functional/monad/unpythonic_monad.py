"""

Unpythonic

https://unpythonic.com/01_06_monads/

Code examples taken from `unpythonic.com`

"""


class Perhaps(object):
    def __init__(self, value):
        self.value = value

    def bind(self, fn):
        if self.value is None:
            return self
        return fn(self.value)

    def get_value(self):
        return self.value

# And our getters will now returns 'Perhaps' objects:

def get_address(company):
    return Perhaps(company.get('address') or None)

def get_street(address):
    return Perhaps(address.get('street') or None)

def get_street_from_company(company):
    return (Perhaps(company)
        .bind(get_address)
        .bind(get_street)
        .get_value())


def test_perhaps():

    company = {
        'name': 'Company Inc.',
        'address': {
            'street': 'Street Name',
            'zipcode': 'ZZ 12345'
        }
    }

    street = get_street_from_company(company)

    print("street = {}".format(street))


#
# 
#

import re
from functools import reduce

# Unit: Our "wrapper" function
def validated_data(data, errors=None):
    """Wrap <data> up in a dict with any <errors> provided"""
    return {
        'data': data,
        'errors': errors or {}
    }


# Bind: Apply a function to a "wrapped" value
def bind_validated_data(vd, fn):
    """ Apply each validator, using its returned data and merging any errors """
    result = fn(vd['data'])
    return {
        'data': result['data'],
        'errors': dict(vd['errors'], **result['errors'])
    }


# Usage: Functions that accept unwrapped values and return wrapped ones.

def validate_name(data):
    if not data.get('name'):
        return validated_data(data, {'name': 'No name found'})
    return validated_data(data)


def clean_phone(data):
    """ Replace all non-numeric characters in the phone field """
    phone = data.get('phone')
    if phone:
        data['phone'] = re.sub(r'[^0-9]', '', phone)
        return validated_data(data)
    return validated_data(data, {'phone': 'Please provide a phone number'})


def validate(data):
    # Take note! This is a handy way to thread data through functions.
    return reduce(
        bind_validated_data,
        [validate_name, clean_phone],
        data)


def test_validated_data():

    data = {
        'data': {
            'name': 'First Second',
            'phone': '+123-456-789'
        },
        'errors': {}
    }

    valid_data = validate(data)

    print("Valid data = {}".format(valid_data))
