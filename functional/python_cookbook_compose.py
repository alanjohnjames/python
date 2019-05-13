"""
Steven F Lott - Modern Python Cookbook

https://mariapilot.noblogs.org/files/2017/05/MODERN-PYTHON-COOKBOOK.pdf


Martelli - Python Cookbook (2nd edition)

http://barbra-coco.dyndns.org/yuri/Python/python-cookbook-2nd-edition.pdf

16.5 Composing Functions

"""


#%%

def sqrt(x):
    import math
    return math.sqrt(x)

def sin(x):
    import math
    return math.sin(x)


#%%

def compose(f, g, *args_for_f, **kwargs_for_f):
        ''' compose functions.  compose(f, g, x)(y) = f(g(y), x)) '''
        def fg(*args_for_g, **kwargs_for_g):
            return f(g(*args_for_g, **kwargs_for_g), *args_for_f, **kwargs_for_f)
        return fg


#%%

sqrt_sin = compose(sqrt, sin)

sqrt_sin(0.5) == sqrt(sin(0.5))


#%%

def sqrt_logged(x, log):
    import math
    return math.sqrt(x), log + " / Did Sqrt..."

def sin_logged(x, log):
    import math
    return math.sin(x), log + " / Did Sin..."

#%%

def mcompose(f, g, *args_for_f, **kwargs_for_f):
    ''' compose functions.  mcompose(f, g, x)(y) = f(*g(y), x)) '''
    def fg(*args_for_g, **kwargs_for_g):
        mid = g(*args_for_g, **kwargs_for_g)
        if not isinstance(mid, tuple):
            mid = (mid,)
        return f(*(mid+args_for_f), **kwargs_for_f)
    return fg



#%%

sqrt_sin_logged = mcompose(sqrt_logged, sin_logged)

sqrt_sin_logged(0.5, log="") # == sqrt(sin(0.5))


#%%
# https://mathieularose.com/function-composition-in-python/

def double(x):
    return x * 2

def inc(x):
    return x + 1

def dec(x):
    return x - 1

inc_and_double = compose(double, inc)

inc_and_double(10) == 22

#%%

import functools

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)),
                            functions, lambda x: x)

inc_double_and_dec = compose(dec, double, inc)
inc_double_and_dec(10) == 21

#%%
