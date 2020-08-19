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

OBJ_1 = {"a": 1.0, "b": 2.0}
OBJ_2 = {"a": 1.01, "b": 2.01}


def float_mismatch():
    differ = Differ()
    result = differ.diff(OBJ_1, OBJ_2)
    assert not result
    print(result.support)
```
<img src="https://github.com/nathan5280/ndl-tools/blob/develop/images/float-precision-fail.png"a/>

