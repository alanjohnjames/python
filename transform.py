#
# Transform
#

import attr
from sumtypes import constructor, sumtype, match

print("Start...")


@sumtype
class Transform(object):
    Int_To_String = constructor(
        i=attr.ib(validator=attr.validators.instance_of(int)),
        s=attr.ib(validator=attr.validators.instance_of(str)))
    String_To_Int = constructor(
        s=attr.ib(validator=attr.validators.instance_of(str)),
        i=attr.ib(validator=attr.validators.instance_of(int)))


@match(Transform)
class transform(object):
    def Int_To_String(i, s):
        return str(i)
    def String_To_Int(s, i):
        return int(s)


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


def test_transform():
    """ Test... transform """
    i_to_s = Transform.Int_To_String(1, "")
    s_to_i = Transform.String_To_Int("2", 0)

    p = transform(i_to_s)
    q = transform(s_to_i)

    print("transform: p = {}".format(p))
    print("transform: q = {}".format(q))


def test_convert():
    """ Test... convert """
    i = Int_Or_String.Int(3)
    s = Int_Or_String.String("5")

    p = convert(i)
    q = convert(s)

    print("convert: p = {}".format(p))
    print("convert: q = {}".format(q))


if __name__ == '__main__':

    test_transform()
    test_convert()

    print("Finished...")
