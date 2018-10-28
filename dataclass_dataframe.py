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


@dataclass
class SimpleDataObject:
    field_a: int
    field_b: str

dataclass_object1 = SimpleDataObject(1, 'a')
dataclass_object2 = SimpleDataObject(2, 'b')


@pytest.mark.skip(reason="Expected Behaviour: Dataclasses to DataFrame.")
def test_dataclass_to_dataframe():
    """Dataclasses to DataFrame."""
    df = pd.DataFrame(data=objects)
    df.dtypes == ['field_a', 'field_b']
    df.dtypes == ['int', 'str']


@pytest.mark.skip(reason="Expected Behaviour: DataFrame to Dataclasses.")
# pytest.skip(reason="")
def test_dataframe_to_dataclass():
    """DataFrame to Dataclasses."""
    df = pd.DataFrame(columns=['field_a', 'field_b'], data=[[1, 'a'], [2, 'b']])
    dataclass_list = df.to_dataclasses()
    dataclass_list == [dataclass_object1, dataclass_object2]


@dataclass
class SimpleDataObject:
    field_a: int
    field_b: str


x = SimpleDataObject(field_a=2, field_b='f')

assert x == SimpleDataObject(field_a=2, field_b='f')


def test_objects_to_dataframe():

    dataclass_objects = [dataclass_object1, dataclass_object2]

    df = pd.DataFrame([asdict(x) for x in dataclass_objects])

    print(df)

    """   field_a field_b
    0        1       a
    1        2       b
    """

    assert True


def test_dataframe_to_objects():

    dataclass_objects = [dataclass_object1, dataclass_object2]

    df = pd.DataFrame([asdict(x) for x in dataclass_objects])

    records = df.to_dict(orient='records')

    record_objects = [SimpleDataObject(*rec.values()) for rec in records]

    assert True
