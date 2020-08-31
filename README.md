# ndl-tools
[![CI](https://github.com/nathan5280/ndl-tools/workflows/Test/badge.svg)](https://github.com/nathan5280/ndl-tools/actions)
[![coverage](https://codecov.io/gh/nathan5280/ndl-tools/master/graph/badge.svg)](https://codecov.io/gh/nathan5280/ndl-tools)
[![pypi](https://img.shields.io/pypi/v/ndl-tools.svg)](https://pypi.python.org/pypi/ndl-tools)
[![versions](https://img.shields.io/pypi/pyversions/ndl-tools.svg)](https://github.com/nathan5280/ndl-tools)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/nathan5280/ndl-tools/blob/master/LICENSE)

Tools for sorting and diffing nested dictionaries and lists.  

The focus of the package is to support API testing.  Hashing two object trees or 
nested dictionaries to compare them works great when they are 
actually equal. If they aren't equal finding out why can become quite tedious.

Are these equal?
```python
obj1 = {"a": 1, "b": 2}
obj2 = {"b": 2, "a": 1}
```

What about a set that is mapped into a list when converted to JSON.
```python
obj1 = [1, 2, 3, 4]
obj2 = [4, 3, 2, 1]
```

```python
from datetime import datetime

obj1 = {"start_date": datetime.date(1999, 1, 1)}
obj2 = {"start_date": datetime.date(2020, 8, 19)}
```

The dictionary isn't to bad to get sorted and compared correctly, but it gets messy when one 
of the values is another dictionary, list or set.  The list case needs to be sorted or not sorted
depending on the context of the object and if it is a list or a set.  And finally, the date one
is hard to keep up to date in your test cases because the dates keep shifting. It isn't to bad if you 
can use something like freezegun to go back in time, but if the payload comes from an external 
service it can be a mess.

## Concepts
| Term | Definition |
| :--- | :--- |
| Differ | Entry point to support diff of two Nested-Dict-Lists (NDL). |
| DiffResult | Result of calling diff() in a Differ object.   It acts like a bool for simple asserts, but also provides a two column colored difference of the two NDL. |
| ListSorter | Classes that can be selectively applied to lists in the NDL either sort or not sort a list. |
| Normalizer | Classes that can be applied to leaf elements to transform them to match from the left and right NDLs. |
| Selector | Classes used to select what elements in the traversal of the NDL a given ListSorter or Normalizer is applied. |
| Sorter | Entry point to NDL sorter functionality. This normally isn't used directly as it sits behind the Differ. |

## Examples
### Float Precision
```python
from ndl_tools import Differ

OBJ_1 = {"a": 1.0, "b": 2.01}
OBJ_2 = {"a": 1.01, "b": 2.011}


def float_mismatch():
    differ = Differ()
    result = differ.diff(OBJ_1, OBJ_2)
    assert not result
    print(result.support)
```
<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-precision-fail.png?raw=true" height="75"/>

Note the highlights on the differences.  Red will indicate that something was deleted and blue that
something was changed and yellow that something was added.

#### Match
Lets apply the *FloatRoundNormalizer* when we do the diff and see if we can get the NDLs to match.

```python
from ndl_tools import Differ, FloatRoundNormalizer

OBJ_1 = {"a": 1.0, "b": 2.01}
OBJ_2 = {"a": 1.01, "b": 2.011}


def float_match():
    differ = Differ()
    float_round_normalizer = FloatRoundNormalizer(places=1)
    result = differ.diff(OBJ_1, OBJ_2, normalizers=[float_round_normalizer])
    assert result
    print(result.support)
```

<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-precision-pass.png?raw=true" height="75"/>


#### Selector to Apply Different Nomalizers
```python
from ndl_tools import Differ, FloatRoundNormalizer, ListLastComponentSelector

OBJ_1 = {"a": 1.0, "b": 2.01}
OBJ_2 = {"a": 1.01, "b": 2.011}


def float_two_precision_match():
    differ = Differ()
    # Normalize the 'a' element to 1 decimal place.
    a_selector = ListLastComponentSelector(component_names=["a"])
    one_float_round_normalizer = FloatRoundNormalizer(places=1, selectors=[a_selector])

    # Normalize the 'b' element to 2 decimal places.
    b_selector = ListLastComponentSelector(component_names=["b"])
    two_float_round_normalizer = FloatRoundNormalizer(
        places=2, selectors=[b_selector]
    )

    result = differ.diff(OBJ_1, OBJ_2, normalizers=[two_float_round_normalizer, one_float_round_normalizer])
    assert result
    print(result.support)
```

<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-two-precision-pass.png?raw=true" height="75"/>

Each of the Normalizers can have a different selector or use the default which is to apply it to
all elements.  The list of Normalizers are called in order until one normalizes the element or all 
normalizers are exhausted.  There is an art to figuring out how to minimize the number of 
Normalizers and  Selectors you need to get two NDLs to match.   If you start getting to 
the point where you have many of them it might be time to think about doing some 
prework on the NDL before comparing them.

# Normalizers
Normalizers are designed to be easily extensible.  Checkout the existing [Normalizers](https://github.com/nathan5280/ndl-tools/blob/develop/src/ndl_tools/normalizer.py)
You can easily see ways to extend these to support exponential numbers, dates, ...

| Normalizer | Usage |
| :--- | :---|
| FloatRoundNormalizer | Round a floating point number to a set number of places. |
| TodayDateNormalizer | Set the date to datetime.date.today(). |
| StrTodayDateNormalizer | Convert a string representation of a date to string representation of today.  Useful if one of the NDLs was read from JSON and the dates weren't converted. |
| PathNormalizer | Replace path with N last components of path. Good when there are absolute paths. |

Have some fun building your own Normalizers.   It only takes a few lines in the __init__() and _normalize() methods.

>[!WARNING]
>If a normalizer was applied to an element, but doesn't actually normalize it, the normalizer should raise NotNormalizedError()

# Selectors
Selectors determine if the normalizer they are attached to will be applied to a given element.  Again 
there is an art to figuring out the minimum number needed or the minimum that are still clear. 

While this isn't the most efficient way to rewrite the example above that rounds both 'a' and 'b' to 
one decimal place, it does show how multiple selectors can be applied to a single normalizer.

```python
from ndl_tools import Differ, FloatRoundNormalizer, ListLastComponentSelector

OBJ_1 = {"a": 1.0, "b": 2.01}
OBJ_2 = {"a": 1.01, "b": 2.011}


def selector_chaining_match():
    differ = Differ()

    a_selector = ListLastComponentSelector(component_names=["a"])
    b_selector = ListLastComponentSelector(component_names=["b"])
    float_round_normalizer = FloatRoundNormalizer(places=1, selectors=[a_selector, b_selector])

    result = differ.diff(OBJ_1, OBJ_2, normalizers=[float_round_normalizer])
    assert result
    print(result.support)
```

<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/selector-multiple-pass.png?raw=true" height="75"/>

There are a few selectors out of the box, but you should subclass your own to minimize the complexity
of your diff code.

| Selector | Usage |
| :--- | :--- |
| ListLastComponentSelector | Match the last component in the element path to a list of names. |
| ListAnyComponentSelector | Match any component in the element path to a list of names.  Good if you want to select a branch and its child elements. |
| RegExSelector | Match the element path with the RegEx. |
| NegativeSelector | Inverts the selection of the Selector it wraps. |
| EndsWithSelector | Match the end of the path. |

# ListSorters
ListSorters are used to control how lists/sets are sorted.  The are applied using Selectors
in the same as with Normalizers.  You shouldn't need anything other than 
the two provided ListSorters, but if you need to the extensibility is there.
