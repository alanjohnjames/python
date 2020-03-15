# %%
# https://pypi.org/project/algebraic-data-types/
# https://github.com/jspahrsummers/adt#installation
#
# https://github.com/jspahrsummers/adt/blob/master/tests/test_maybe.py
# https://github.com/jspahrsummers/adt/blob/master/tests/test_list.py
#
# https://github.com/jspahrsummers/adt#installation
#
# pip install algebraic-data-types
#


@adt
class Tree:
    """tree."""

    EMPTY: Case
    LEAF: Case[int]
    NODE: Case["Tree", "Tree"]


Tree.EMPTY

Tree.LEAF(999)


t = Tree.NODE(Tree.EMPTY, Tree.LEAF(11))

t


L = TypeVar('L')
R = TypeVar('R')


@adt
class Either(Generic[L, R]):
    """Either."""

    LEFT = Case[L]
    RIGHT = Case[R]


Either.LEFT("to the left...")
