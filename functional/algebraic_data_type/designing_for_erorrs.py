"""Designing for errors.

Unhappy paths are requirements too!

This code implements the basic error handling example in slides 129-135 of;
    https://www.slideshare.net/ScottWlaschin/railway-oriented-programming?ref=https://fsharpforfunandprofit.com/rop/

References:
    https://www.slideshare.net/ScottWlaschin/railway-oriented-programming
    https://fsharpforfunandprofit.com/posts/exceptions/

Uses:
    https://pypi.org/project/algebraic-data-types/

"""

# %%

from dataclasses import dataclass
from typing import Callable, Union

# from toolz import curry
# from toolz.curried import pipe


# %%
#
# Simple types.
#


class EmailAddress(str):
    """Email Address."""


class Name(str):
    """Name."""


# %%
#
# Error.
#

class NameMustNotBeBlank:
    """Name must not be blank."""


class EmailMustNotBeBlank:
    """Email must not be blank."""


@dataclass
class EmailNotValid:
    """Email not valid."""

    email: EmailAddress


class Error:
    """Error."""

    types = Union[NameMustNotBeBlank,
                  EmailMustNotBeBlank,
                  EmailNotValid]

    NAME_MUST_NOT_BE_BLANK = NameMustNotBeBlank
    EMAIL_MUST_NOT_BE_BLANK = EmailMustNotBeBlank
    EMAIL_NOT_VALID = EmailNotValid


# %%
def unhandled_type(x) -> str:
    """Unhandled type."""
    # https://github.com/python/mypy/issues/5818
    # This function (stolen mostly verbatim from TypeScript
    # https://www.typescriptlang.org/docs/handbook/advanced-types.html#exhaustiveness-checking):
    return f"Unhandled type: `{type(x).__name__}`"


def error_message(err: Error.types, default_handler: Callable = unhandled_type) -> Callable:
    """Error message."""
    return {
        isinstance(err, Error.NAME_MUST_NOT_BE_BLANK): lambda: "Name must not be blank",
        isinstance(err, Error.EMAIL_MUST_NOT_BE_BLANK): lambda: "Email must not be blank",
        isinstance(err, Error.EMAIL_NOT_VALID): lambda: f"Email `{err.email}` is not valid."
    }.get(True, default_handler)


# %%

errors = [
    Error.NAME_MUST_NOT_BE_BLANK(),
    Error.EMAIL_MUST_NOT_BE_BLANK(),
    Error.EMAIL_NOT_VALID(EmailAddress('name@email.com')),
]

messages = list(map(error_message, errors))

[msg() for msg in messages]

#%%
