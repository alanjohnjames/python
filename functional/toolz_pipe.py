# %%

import json
from dataclasses import dataclass, replace

from toolz import compose_left, do, pipe

import _io

# %%
#
# Imperative.
#

DATA = dict(key="Json Key", value="Json Value")
TEXT = json.dumps(DATA)

FILENAME1 = "filename1.json"

io = open(FILENAME1, mode='w')
chars = io.write(TEXT)
io.close()
print(f"Wrote the file `{FILENAME1}` with {chars} characters.")


# %%
#
# Object-Oriented.
#

FILENAME2 = "filename2.json"

@dataclass
class File:
    """File."""

    name: str
    io: _io.TextIOWrapper = None
    chars: int = 0

    def write(self, text):
        """Write file."""
        self.io = open(self.name, mode='w')
        self.chars = self.io.write(text)
        self.io.close()
        return self

    def show(self):
        """Show file."""
        print(f"Wrote the file `{self.name}` with {self.chars} characters.")


File(FILENAME2).write(TEXT).show()


# %%
#
# Functional.
#

FILENAME3 = "filename3.json"

@dataclass(frozen=True)
class File:
    """File."""

    name: str
    io: _io.TextIOWrapper = None
    chars: int = 0


def write(filename, text):
    """Write file."""
    return pipe(File(filename),
                lambda file: replace(file, io=open(file.name, mode='w')),
                lambda file: replace(file, chars=file.io.write(text)),
                lambda file: do(lambda file: file.io.close(), file))


def show(file):
    """Show file."""
    print(f"Wrote the file `{file.name}` with {file.chars} characters.")


compose_left(write, show)(FILENAME3, TEXT)


# %%
