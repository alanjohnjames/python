"""
Proposal description

Dataclasses were added in Python 3.7.

It would be nice for pandas to support dataclasses.

For example could be possible to construct dataframe from by calling
`.from_dataclasses` or just `.DataFrame(data=dataclass_list)`.

There should be also possibility to do `.to_dataclasses`.

https://github.com/pandas-dev/pandas/issues/21910

"""

import pandas as pd
import pytest
from dataclasses import dataclass
from dataclasses import asdict

#
# dataclasses
#

@dataclass
class SimpleDataObject:
    field_a: int
    field_b: str

dataclass_object1 = SimpleDataObject(1, 'a')
dataclass_object2 = SimpleDataObject(2, 'b')

#
# tests
#

@pytest.mark.skip(reason="Expected Behaviour: Dataclasses to DataFrame.")
def test_expected_behaviour_dataclass_to_dataframe():
    """Dataclasses to DataFrame."""
    df = pd.DataFrame(data=[dataclass_object1, dataclass_object2])
    df.dtypes == ['field_a', 'field_b']
    df.dtypes == ['int', 'str']


@pytest.mark.skip(reason="Expected Behaviour: DataFrame to Dataclasses.")
def test_expected_behaviour_dataframe_to_dataclass():
    """DataFrame to Dataclasses."""
    df = pd.DataFrame(columns=['field_a', 'field_b'], data=[[1, 'a'], [2, 'b']])
    dataclass_list = df.to_dataclasses()
    dataclass_list == [dataclass_object1, dataclass_object2]


def test_dataclass_equal():

    x = SimpleDataObject(field_a=2, field_b='f')

    assert x == SimpleDataObject(field_a=2, field_b='f')


def test_dataclass_to_dataframe():

    _df = pd.DataFrame(columns=['field_a', 'field_b'], data=[[1, 'a'], [2, 'b']])

    dataclass_objects = [dataclass_object1, dataclass_object2]

    df = pd.DataFrame([asdict(x) for x in dataclass_objects])

    print(df)
    """   field_a field_b
    0        1       a
    1        2       b
    """

    assert _df.equals(df)


def test_dataframe_to_dataclass():

    _df = pd.DataFrame(columns=['field_a', 'field_b'], data=[[1, 'a'], [2, 'b']])

    dataclass_objects = [dataclass_object1, dataclass_object2]

    df = pd.DataFrame([asdict(x) for x in dataclass_objects])

    assert _df.equals(df)

    records = df.to_dict(orient='records')

    record_objects = [SimpleDataObject(**rec) for rec in records]

    assert record_objects == dataclass_objects
