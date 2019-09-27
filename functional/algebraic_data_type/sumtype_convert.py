#
# Transform
#

import attr
from sumtypes import constructor, sumtype, match

print("Start...")


@sumtype
class Int_Or_String(object):
    Int = constructor(
        i=attr.ib(validator=attr.validators.instance_of(int)))
    String = constructor(
        s=attr.ib(validator=attr.validators.instance_of(str)))


@match(Int_Or_String)
class convert(object):
    def Int(i): return str(i)
    def String(s): return int(s)


def test_convert():
    """ Test... convert """
    i = Int_Or_String.Int(3)
    s = Int_Or_String.String("5")

    p = convert(i)
    q = convert(s)

    print("convert: p = {}".format(p))
    print("convert: q = {}".format(q))


if __name__ == '__main__':

    test_convert()

    print("Finished...")
