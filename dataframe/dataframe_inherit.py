"""Inherit DataFrame.

http://devanla.com/case-for-inheriting-from-pandas-dataframe.html


"""

import pandas as pd

class StudentsDF(pd.DataFrame):
    SCORES = 'scores'
    NAMES = 'names'

    @property
    def _constructor(self):
        return StudentsDF

x = StudentsDF(data=dict(names=['Alice', 'Bob'],
                         scores=[60, 50]),
               index=[100, 200])

type(x)  # __main__.StudentDF
x


y = StudentsDF(data={StudentsDF.NAMES: ['Alice', 'Bob'],
                     StudentsDF.SCORES: [60, 50]},
               index=[100, 200])
type(y)
y
