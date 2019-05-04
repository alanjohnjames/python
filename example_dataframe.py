
#%%
# https://jakevdp.github.io/PythonDataScienceHandbook/03.07-merge-and-join.html

import sys

import IPython
import numpy as np
import pandas as pd

#%%
df1 = pd.DataFrame({'employee': ['Bob', 'Jake', 'Lisa', 'Sue'],
                    'group': ['Accounting', 'Engineering', 'Engineering', 'HR']})
df2 = pd.DataFrame({'employee': ['Lisa', 'Bob', 'Jake', 'Sue'],
                    'hire_date': [2004, 2008, 2012, 2014]})

#%% display('df1', 'df2')
df1

#%% display('df1', 'df2')
df2
