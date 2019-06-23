"""Monads in Python (with nice syntax)

Hacker News
https://news.ycombinator.com/item?id=4959680

"""

#%%
from dataclasses import dataclass

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

#%%
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

#%%
# dons' explanation will be better/more rigorous than mine, but in a more familiar syntax (Python), # let's say you've got some functions:

def get_user(id):
    # returns None if no such user exists
    try:
        return Database.users[id]
    except KeyError:
        return None

def send_message(user, message):
    Email(user.email, message).send()

def log(message):
    print(message)

#%%
def main1():
    user = get_user("user1")
    # uhoh -- this could be None and we didn't handle it!
    send_message(user, f"Hello {user.name}")
    log(f"Message sent.")

main1()

#%%
# So, we add a None check:
def main2():
    user = get_user("unknown_user")
    if user != None:
        send_message(user, f"Hello {user.name}")
    log(f"Was the message sent? I don't know.")

main2()

#%%
# But... what if we want to log the status of that send_message call?
from toolz.functoolz import curry

@curry
def send_message(user, msg):
    try:
        Email(user.email, msg).send()
        return None
    except Exception as e:
        return f"Failed to send message; {e}"

#%%
# (Note that this is a contrived example, please don't critique the general dumbness ;)).
# Now...
def main3():
    user = get_user(1)
    if user != None:
        response = send_message(user, f"Hello {user}")
        if response != None:
            log(response)
    log(f"Was the user found? Was the message sent? I don't know.")

main3()

#%%
# As you can see, it's getting a bit hairy.
# But, what if we had a class that dealt with the Nones for us? 
# This is what a monad is: an interface, that many different instances implement,
# which provides some behavior. The following only deals with single-argument functions, but:
class NoneMonad:
    def __init__(self, arg):
        self.arg = arg

    def bind(self, func):
        if self.arg != None:
            next_arg = func(self.arg)
            return NoneMonad(next_arg)
        else:
            return NoneMonad(None)

#%%
# Now, we...
def main4(user_id):
    return (NoneMonad(user_id)
                .bind(get_user)
                .bind(send_message(msg="Hello user."))
                .bind(log))

#%%5
main4(1)

#%%
main4('user1')

# And, boom, the Nones are handled. Real, non-contrived Monads do more (and implement other behaviours -- like in dons' example, the Either response, or the Maybe monad, etc.), but hopefully this demonstrates the strength. Haskell's typically used as the example language, because there's syntax sugar in Haskell for making dealing with Monads prettier :).

# Having finally grokked them, it surprised me how simple the concept is. I think for people (like me!) coming from Java, Python, etc. who've not had to deal with the concept, there's this sort of imbued myth that they're a much more difficult concept than they really are. It's as simple as: a Monad is an interface, that can be implemented, that provides a construct for executing code in.

# Please forgive any blinding mistakes I've made in my code.

#%%
#
# Curry.
# 
from toolz.functoolz import curry

@curry
def send_message(user="", msg="<No Message>", email=True):
    try:
        print(f"Sending {'email' if email else 'letter'} to {user} which says {msg}")
        return None
    except Exception as e:
        return f"Failed to send message; {e}"

send_email = send_message(msg="Hi there!", email=False)

send_email(user="Steve")

#%%
message_steve = send_message(user="Steve")

message_steve(msg="Goodbye!")

