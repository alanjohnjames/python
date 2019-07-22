"""Monads in Python (with nice syntax)

Hacker News
https://news.ycombinator.com/item?id=4959680

"""

#%% Imports.

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from toolz.curried import do
from toolz.functoolz import curry

#%% Setup.

@dataclass
class User:
    name: str
    email: str

@dataclass
class Database:
    users = {
        "user1": User("Alan", "alan@mail.com"),
        "user2": User("Sue", "sue@mail.com"),
    }

@dataclass
class Email:
    to: str
    message: str
    sent: bool = False

    def __repr__(self):
        return f"To: {self.to}\nMessage: {self.message}"

    def send(self):
        self.sent = True if not self.sent else False
        return True if self.sent else False

#%% Dons' explanation will be better/more rigorous than mine, but in a more familiar syntax (Python),

# Let's say you've got some functions:

def get_user(id):
    # returns None if no such user exists
    try:
        return Database.users[id]
    except KeyError:
        return None

def send_message1(user, message):
    Email(user.email, message).send()

def log(message):
    print(f"LOG: {datetime.now()}: {message}")


def main1():
    user = get_user("user1")
    # uhoh -- this could be None and we didn't handle it!
    send_message1(user, f"Hello {user.name}")
    log(f"Message sent.")

def test_main1():
    main1()
    # Message sent.


#%% So, we add a None check:

def main2():
    user = get_user("unknown_user")
    if user != None:
        send_message1(user, f"Hello {user.name}")
    log(f"Was the message sent? I don't know.")

def test_main2():
    main2()
    # Was the message sent? I don't know.


#%% But... what if we want to log the status of that send_message call?

# NOTE: Making use of `curry` to make `send_message2` compatible with `NoneMonad` later on.

@curry
def send_message2(user, msg):  # TODO: def may_throw(arg, func):
    try:
        send_message1(user, msg)
        return None  # TODO: return "Message sent." ?
    except Exception as e:
        return f"Failed to send message; {e}"

# Now...

def main3():
    user = get_user("user1")
    if user != None:
        response = send_message2(user, f"Hello {user}")
        if response != None:
            log(response)  # Does not get called!
    log(f"Was the user found? user = {user}")
    log(f"Was the message sent? response = {response}")

def test_main3():
    main3()
    # Was the user found? user = User(name='Alan', email='alan@mail.com')
    # Was the message sent? response = None

#%% As you can see, it's getting a bit hairy.
# But, what if we had a class that dealt with the Nones for us?
# This is what a monad is: an interface, that many different instances implement,
# which provides some behavior. The following only deals with single-argument functions, but:

@dataclass
class NoneMonad:
    arg: Any

    def bind(self, func):
        if self.arg != None:
            next_arg = func(self.arg)
            return NoneMonad(next_arg)
        else:
            return NoneMonad(None)

# Now, we...

def main4(user_id):
    return (NoneMonad(user_id)
                .bind(get_user)
                .bind(do(send_message2(msg="Hello user.")))
                .bind(log))

def test_main4_unknown_user():
    main4('unknown_user')
    # NoneMonad(arg=None)


def test_main4_user1():
    main4('user1')
    # User(name='Alan', email='alan@mail.com')

    print(f"type(t) = {main4('user1')}.")

# And, boom, the Nones are handled. Real, non-contrived Monads do more (and implement other behaviours -- like in dons' example, the Either response, or the Maybe monad, etc.), but hopefully this demonstrates the strength. Haskell's typically used as the example language, because there's syntax sugar in Haskell for making dealing with Monads prettier :).

# Having finally grokked them, it surprised me how simple the concept is. I think for people (like me!) coming from Java, Python, etc. who've not had to deal with the concept, there's this sort of imbued myth that they're a much more difficult concept than they really are. It's as simple as: a Monad is an interface, that can be implemented, that provides a construct for executing code in.

# Please forgive any blinding mistakes I've made in my code.


#%% Try using `curry`

@curry
def send_message_curry(user, msg, email=True):
    try:
        print(f"Sending {'email' if email else 'letter'} to {user} which says {msg}")
        return None
    except Exception as e:
        return f"Failed to send message; {e}"


def test_main5():
    send_email = send_message_curry(msg="Hi there!", email=False)
    send_email(user="Steve")

    message_steve = send_message_curry("Steve")
    message_steve(msg="Goodbye!")
