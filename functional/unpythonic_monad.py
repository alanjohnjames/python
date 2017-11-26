"""

Unpythonic

https://unpythonic.com/01_06_monads/

Code examples tsken from `unpythonic.com`

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
