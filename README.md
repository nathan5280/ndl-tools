# ndl-tools
Tools for sorting and diffing nested dictionaries and lists.  

The focus of the package is to support API testing.  Hashing two object trees or nested dictionaries to compare them works great when they are 
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
obj1 = {"start_date": datetime.date(1999, 1, 1)}
obj2 = {"start_date": datetime.date(2020, 8, 19)}
```

The dictionary isn't to bad to get sorted to compare correctly.  But gets messy when one 
of the values is another dictionary, list or set.  The list case needs to be sorted or not
depends on the context of the object and if it is a list or a set.  And finally the date one
is hard to keep up to date in your test case because the dates keep shifting if the result
comes from an external service that you can feezegun today to some standard day in the past.

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
<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-precision-fail.png"/>

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
    result = differ.diff(OBJ_1, OBJ_2, normalizer=float_round_normalizer)
    assert result
    print(result.support)
```

<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-precision-pass.png"/>


#### Selector to Apply Different Nomalizers
```python
from ndl_tools import Differ, FloatRoundNormalizer, ListLastComponentSelector

OBJ_1 = {"a": 1.0, "b": 2.01}
OBJ_2 = {"a": 1.01, "b": 2.011}


def float_two_precision_match():
    differ = Differ()
    # Normalize the 'a' element to 1 decimal place.
    a_selector = ListLastComponentSelector(component_names=["a"])
    one_float_round_normalizer = FloatRoundNormalizer(places=1, selector=a_selector)

    # Normalize the 'b' element to 2 decimal places.
    b_selector = ListLastComponentSelector(component_names=["b"])
    two_float_round_normalizer = FloatRoundNormalizer(
        places=2, selector=b_selector, parent_normalizer=one_float_round_normalizer
    )

    result = differ.diff(OBJ_1, OBJ_2, normalizer=two_float_round_normalizer)
    assert result
    print(result.support)
```

<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-two-precision-pass.png"/>

Each of the Normalizers can have a different selector or use the default which is to apply it to
all elements.  The Normalizers are just chained together and called successively until one of them
normalizes the node.  There is an art to figuring out how to minimize the number of Normalizers and
Selectors you need to get two NDLs to match.   If you start getting to the point where you have many
of them it might be time to think about doing some prework on the NDL before comparing them.

# Normalizers
Normalizers are designed to be easily extensible.  Checkout the existing [Normalizers](https://github.com/nathan5280/ndl-tools/blob/develop/src/ndl_tools/normalizer.py)
You can easily see ways to extend these to support exponential numbers, dates, ...

>[!WARNING]
>If a normalizer was applied to an element, but doesn't actually normalize it, the normalizer should raise NotNormalizedError()