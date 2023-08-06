# DSKit

DSKit (Data Science Kit) is a Python package that provides tools for solving simple Data Science tasks.

# Installing

```bash
pip install dskit
```

# Tutorial

DSKit consists of three submodules:

* *dskit.frame* - contains a set of functions for *pandas.DataFrame* and *pandas.Series* manipulation.
* *dskit.pipeline* - contains a *PipelineFrame* wrapper of *pandas.DataFrame*.
* *dskit.tensor* - contains a set of functions for *numpy.ndarray* manipulation.

## *dskit.frame*

### *astype*

*astype* is a convenience function, which partially applies passed parameter to *pd.DataFrame.astype* or *pd.Series.astype* function.

```python
xs = pd.Series([1, 2, 3])
print(astype(float)(xs))

# 0    1.0
# 1    2.0
# 2    3.0
# dtype: float64

ys = pd.DataFrame({"A": [1, 2], "B": ["01-01-2020", "02-01-2020"]})
print(astype({"A": float, "B": "datetime64[D]"})(ys))

#      A          B
# 0  1.0 2020-01-01
# 1  2.0 2020-02-01
```

### *create_dummifier*

*create_dummifier* is less harmful alternative to *pd.get_dummies*. This function takes a *Dict[str, Tuple[object, ...]]* and returns *Callable[[pd.DataFrame], pd.DataFrame]*. Key of the dictionary is treated as a name of a column and value of the dictionary is treated as unique values of that column.
Each key and value of the dictionary are passed to *create_encoder* function. Bases on created encoders a new function is created which takes *pd.DataFrame* and returns *pd.DataFrame*. The returned function is a "dummify" function.

```python
frame = pd.DataFrame({"A": (1, 2, 2, 5, 5), "B": ("a", "a", "b", "c", "d")})
uniques: Dict[str, Tuple[object, ...]] = unique(frame)

dummify: Callable[[pd.DataFrame], pd.DataFrame] = create_dummifier(uniques)
print(dummify(frame))

#    A_1  A_2  A_5  B_a  B_b  B_c  B_d
# 0  1.0  0.0  0.0  1.0  0.0  0.0  0.0
# 1  0.0  1.0  0.0  1.0  0.0  0.0  0.0
# 2  0.0  1.0  0.0  0.0  1.0  0.0  0.0
# 3  0.0  0.0  1.0  0.0  0.0  1.0  0.0
# 4  0.0  0.0  1.0  0.0  0.0  0.0  1.0

other_frame = pd.DataFrame({"C": (True, True, False, True), "A": (1, 2, 3, 4)})
print(dummify(other_frame))

#    A_1  A_2  A_5      C
# 0  1.0  0.0  0.0   True
# 1  0.0  1.0  0.0   True
# 2  0.0  0.0  0.0  False
# 3  0.0  0.0  0.0   True

# notice, that columns are sorted alphabetically (C comes after A)
# you can pass sort_columns=False if you want to omit sorting
```

One of the reasons why *create_dummifier* is less harmful than *pd.get_dummies* is that it will not dummify new values. Thanks to that Machine Learning models will operate on data with the same number of dimensions regardless of new values presence in new portion of data.

```python
old_frame = pd.DataFrame({"B": ("a", "a", "b")})
new_frame = pd.DataFrame({"B": ("a", "b", "c")})

uniques: Dict[str, Tuple[object, ...]] = unique(old_frame)
dummify: Callable[[pd.DataFrame], pd.DataFrame] = create_dummifier(uniques)

print(dummify(new_frame))

#    B_a  B_b
# 0  1.0  0.0
# 1  0.0  1.0
# 2  0.0  0.0

print(pd.get_dummies(new_frame))

#    B_a  B_b  B_c
# 0    1    0    0
# 1    0    1    0
# 2    0    0    1
```

### *create_encoder*

*create_encoder* is a function used by *create_dummifier*. *create_encoder* takes a column name with a set of values and returns *Callable[[Tuple[object, ...]], pd.DataFrame]*. The returned function one-hot-encodes passed values.

```python
encoded: pd.DataFrame = create_encoder("A", (1, 2, 3))((1, 2, 3, 4, np.nan))
print(encoded)

#    A_1  A_2  A_3
# 0    1    0    0
# 1    0    1    0
# 2    0    0    1
# 3    0    0    0
# 4    0    0    0
```

### *create_numpy_encoder*

*create_numpy_encoder* is a similar function to *create_encoder*. The only difference is that it operates on *numpy.ndarray* instead of *pd.DataFrame*.

```python
encoded: np.ndarray = create_numpy_encoder((1, 2, 3))((1, 2, 3, 4, np.nan))
print(encoded)

# [[1 0 0]
#  [0 1 0]
#  [0 0 1]
#  [0 0 0]
#  [0 0 0]]
```

### *maprows*

*maprows* is a function that applies some function to each row of the *pd.DataFrame*.

```python
xs = pd.DataFrame({"A": [1, 2], "B": ["01-01-2020", "02-01-2020"]})

for x in maprows(lambda x: x.A, xs):
  print(x)

# 1
# 2
```

It is a wrapper of *pd.DataFrame.iterrows* which simply removes unnecessary row indices.

### *name*

*name* is simply:

```python
def name(x: Union[pd.Series, str]) -> str:
  return x if isinstance(x, str) else (x.name or "")
```

Example of *name* usage:

```python
print(name(pd.Series([1, 2, 3])) == "") # True
print(name(pd.Series([1, 2, 3], name="ABC"))) # ABC
```

Notice that, default name of any *pd.Series* is None.

### *transformrows*

*transformrows* is a function similar to *maprows*. The difference between *transformrows* and *maprows* is that *transformrows* takes a function *Callable[[pd.Series], pd.Series]* instead of *Callable[[pd.Series], Y]*. After applying passed function to each row, *transformrows* will concatenate resulting rows into a new frame. The concatenation is done by using *concatenate* function which is passed as third parameter. By default *partial(pd.concat, axis="columns")* function is used.

```python
xs = pd.DataFrame({"A": [1, 2], "B": ["01-01-2020", "02-01-2020"]})
ys: pd.DataFrame = transformrows(lambda x: 2 * x, xs)

print(ys)

#    A                     B
# 0  2  01-01-202001-01-2020
# 1  4  02-01-202002-01-2020
```

### *unique*

*unique* is a function which takes *pd.DataFrame* and returns *Dict[str, Tuple[object, ...]]*. Key of the dictionary is a name of a column of the passed frame and value of the dictionary is unique values of that column.

```python
frame = pd.DataFrame({"A": (1, 2, 2, 5, 5), "B": ("a", "a", "b", "c", "d")})
uniques: Dict[str, Tuple[object, ...]] = unique(frame)

print(uniques)

# {'A': (1, 2, 5), 'B': ('a', 'b', 'c', 'd')}
```

## *dskit.pipeline*

### *PipelineFrame*

You can create a *PipelineFrame* by passing some *pd.DataFrame*:

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})
pipeline = PipelineFrame(xs)
```

Additionally, you can pass some concatenation function along with *pd.DataFrame*:

```python
pipeline = PipelineFrame(xs, concatenate_columns=inner)
# inner is simply: partial(pd.concat, axis="columns", join="inner")
```

You will see later how passing custom concatenation function might benefit. For now you can stick with a default concatenation function *partial(pd.concat, axis="columns")*.

Under the hood *PipelineFrame* stores passed *pd.DataFrame* as *Iterable[pd.DataFrame]*. Thanks to that, some functions applied to underlining *pd.DataFrame* are **lazily evaluated**. Following *PipelineFrame* methods are lazy:

* *map*
* *apply*
* *filter*
* *select*

Those methods also return *PipelineFrame* (the same object you operate on). I call those methods **non-terminal** methods.

The rest of the *PipelineFrame* methods are not lazy:

* *aggregate*
* *foreach*
* *get*

I call those methods **terminal** methods, because they do not return a *PipelineFrame*, so you can not apply other *PipelineFrame* methods to the result.

#### *map*

*map* allows you to map the underlining *pd.DataFrame* using some function. *map* can take different types of parameters. Based on parameter's type *map* behaves differently. Supported types and behaviours include:

* *Callable[[pd.DataFrame], pd.DataFrame]* - apply passed function to underlining *pd.DataFrame*.
* *Tuple[Callable[[pd.DataFrame], pd.DataFrame], ...]* - apply each function to underlining *pd.DataFrame* and concatenate resulting frames using passed *concatenate_columns* function.
* *List[Callable[[pd.Series], pd.Series]]* - apply each function to each row of underlining *pd.DataFrame* and concatenate resulting frames using passed *concatenate_columns* function.

The last type is slightly more complicated. It has following definition: *Iterable[Tuple[Union[pd.Series, str], Union[Callable[[pd.DataFrame], pd.Series], Callable[[pd.Series], pd.Series]]]]*. It is an *Iterable* of pairs. The first value of a pair is either a *pd.Series* or a *str*. If it is a *pd.Series*, it will be mapped to a *str* using a *name* function. If the first value of the pair is a name of the underlining *pd.DataFrame* column, *map* will assume, that the second value is a *Callable[[pd.Series], pd.Series]*. If the first value of the pair is any other string, *map* will assume, that the second value is a *Callable[[pd.DataFrame], pd.Series]*. So in the first case *map* will take an existing column from the underlining *pd.DataFrame* and apply passed function to that column, and in the second case *map* will take the whole underlining *pd.DataFrame* and apply passed function to it. The result of that function will be stored in the underlining *pd.DataFrame* with a name passed as the first value of the pair.

Let's take a look at some examples:

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})

# the first behaviour
PipelineFrame(xs).map(lambda ys: 2 * ys).foreach(print)

# sidenote: foreach is a terminal method which applies a function

#    A   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB

# the second behaviour
PipelineFrame(xs).map((lambda ys: 2 * ys, lambda ys: ys)).foreach(print)

#    A   B  A  B
# 0  2  AA  1  A
# 1  2  BB  1  B
# 2  4  AA  2  A
# 3  6  BB  3  B
# 4  6  BB  3  B

# the third behaviour
PipelineFrame(xs).map([lambda ys: 2 * ys, lambda ys: ys]).foreach(print)

#    A   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB
# 0  1   A
# 1  1   B
# 2  2   A
# 3  3   B
# 4  3   B

# the fourth behaviour
PipelineFrame(xs).map(
  (
    ("A", lambda ys: ys + 1),
    (xs.B, lambda ys: 2 * ys),
    ("C", lambda ys: ys.A.astype(str) + ys.B)
  )
).foreach(print)

#    A   B   C
# 0  2  AA  1A
# 1  2  BB  1B
# 2  3  AA  2A
# 3  4  BB  3B
# 4  4  BB  3B
```

You can see, that by using the fourth behaviour of the *map* you can add new columns to a *pd.DataFrame*. You might also want to use operators instead of calling methods explicitly:

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})

# the first behaviour
PipelineFrame(xs) / (lambda ys: 2 * ys) & print

#    A   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB

# the second behaviour
PipelineFrame(xs) / (lambda ys: 2 * ys, lambda ys: ys) & print

#    A   B  A  B
# 0  2  AA  1  A
# 1  2  BB  1  B
# 2  4  AA  2  A
# 3  6  BB  3  B
# 4  6  BB  3  B

# the third behaviour
PipelineFrame(xs) / [lambda ys: 2 * ys, lambda ys: ys] & print

#    A   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB
# 0  1   A
# 1  1   B
# 2  2   A
# 3  3   B
# 4  3   B

# the fourth behaviour
(
  PipelineFrame(xs)
  / (
      ("A", lambda ys: ys + 1),
      (xs.B, lambda ys: 2 * ys),
      ("C", lambda ys: ys.A.astype(str) + ys.B)
    )
  & print
)

#    A   B   C
# 0  2  AA  1A
# 1  2  BB  1B
# 2  3  AA  2A
# 3  4  BB  3B
# 4  4  BB  3B
```

Notice that, evaluation happens only after using a terminal method (in this case *foreach*):

```python
def f(ys: pd.DataFrame) -> pd.DataFrame:
  print("A")
  return ys

pipeline = PipelineFrame(xs) / f

print("B")
pipeline & print

# B
# A
#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B
```

#### *apply*

*apply* behaves nearly the same way as *map*, but with single minor difference. *map* guarantees that, the passed *pd.DataFrame* remains unmodified (unless passed function modifies it), and *apply* does not. *apply* will modify the passed *pd.DataFrame* only in the context of the fourth behaviour of the *map* function, and only when you pass exclusively existing column names.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})
PipelineFrame(xs).apply((("A", lambda x: x + 1),)).foreach(print)

#    A  B
# 0  2  A
# 1  2  B
# 2  3  A
# 3  4  B
# 4  4  B

print(xs)

#    A  B
# 0  2  A
# 1  2  B
# 2  3  A
# 3  4  B
# 4  4  B

# alternatively

xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})
PipelineFrame(xs) // (("A", lambda x: x + 1),) & print

#    A  B
# 0  2  A
# 1  2  B
# 2  3  A
# 3  4  B
# 4  4  B
```

In any other case *apply* will behave exactly the same way *map* does. Use it only if you know what you are doing.

#### *filter*

*filter* allows you to filter the underlining *pd.DataFrame*. Similar to *map* method, *filter* also behaves differently based on a type of the passed parameter:

* *Callable[[pd.DataFrame], np.ndarray]* - apply passed function to the underlining *pd.DataFrame* and filter columns based on the resulting *np.ndarray*. Under the hood, simple *xs.iloc[:, fs(xs)]* is done, where *fs* is a passed function and *xs* is the underlining *pd.DataFrame*.
* *Tuple[Callable[[pd.DataFrame], np.ndarray], ...]* - apply passed functions to the underlining *pd.DataFrame*, fold the results using *partial(np.all, axis=0)* function and filter columns based on the resulting *np.ndarray*. Under the hood, simple *xs.iloc[:, ys]* is done, where *ys* is the result of a *partial(np.all, axis=0)* function and *xs* is the underlining *pd.DataFrame*.
* *List[Callable[[pd.Series], bool]]* - create a function *lambda x: all(map(lambda f: f(x), fs))*, where *fs* is the list of passed functions, apply that function to each row and filter rows based on the result.

As with *map* method, the last behaviour has a slightly more complex associated parameter type: *Iterable[Tuple[Union[pd.Series, str], Callable[[pd.Series], np.ndarray]]]*. It is an *Iterable* of pairs. The first value of a pair is either a *pd.Series* or a *str*. If it is a *pd.Series*, it will be mapped to a *str* using a *name* function. The second value is a function which is applied to a column of the underlining *pd.DataFrame*. The names of that column is the first value of a pair. After each function of an *Iterable* of pairs is applied, the results are folded using *partial(np.all, axis=0)* function. Based on the result *zs* of that function application, the underlining *pd.DataFrame* is filtered using expression *xs.iloc[zs]*, where *xs* is the underlining *pd.DataFrame*.

Let's take a look at some examples:

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"], "dates": ["2020-02-02", "2020-01-01", "2020-02-01", "2020-02-01", "2020-01-02"]})

# the first behaviour
PipelineFrame(xs).filter(lambda ys: ys.columns == "B").foreach(print)

#    B
# 0  A
# 1  B
# 2  A
# 3  B
# 4  B

# the second behaviour
PipelineFrame(xs).filter((lambda ys: ys.columns.str.isupper(), lambda ys: ys.dtypes == object)).foreach(print)

#    B
# 0  A
# 1  B
# 2  A
# 3  B
# 4  B

# the third behaviour
PipelineFrame(xs).filter([lambda ys: ys.A == 1, lambda ys: ys.B == "B"]).foreach(print)

#    A  B       dates
# 1  1  B  2020-01-01

# the fourth behaviour
PipelineFrame(xs).filter(
  (
    ("A", lambda ys: ys > 1),
    (xs.B, lambda ys: ys == "B"),
    ("dates", lambda ys: ys == "2020-01-02")
  )
).foreach(print)

#    A  B       dates
# 4  3  B  2020-01-02

# alternatively

# the first behaviour
PipelineFrame(xs) % (lambda ys: ys.columns == "B") & print

#    B
# 0  A
# 1  B
# 2  A
# 3  B
# 4  B

# the second behaviour
PipelineFrame(xs) % (lambda ys: ys.columns.str.isupper(), lambda ys: ys.dtypes == object) & print

#    B
# 0  A
# 1  B
# 2  A
# 3  B
# 4  B

# the third behaviour
PipelineFrame(xs) % [lambda ys: ys.A == 1, lambda ys: ys.B == "B"] & print

#    A  B       dates
# 1  1  B  2020-01-01

# the fourth behaviour
(
  PipelineFrame(xs)
  % (
      ("A", lambda ys: ys > 1),
      (xs.B, lambda ys: ys == "B"),
      ("dates", lambda ys: ys == "2020-01-02")
    )
  & print
)

#    A  B       dates
# 4  3  B  2020-01-02
```

#### *select*

*select* allows you to select columns from the underlining *pd.DataFrame*. *select* takes either an *Iterable[Union[pd.Series, str]]* or a *ColumnFilter*. If an *Iterable[Union[pd.Series, str]]* is passed, *select* at first will map each *pd.Series* in the *Iterable* using a *name* function, and then it will pass resulting *Iterable[str]* to *column* function to construct a *ColumnFilter*. The resulting *fs* of type *ColumnFilter* will be used for selecting like so *xs.loc[:, fs(xs)]*, where *xs* is the underlining *pd.DataFrame*. If a *ColumnFilter* is passed, *select* will immediately use it for selecting like so *xs.loc[:, fs(xs)]*, where *fs* is the passed *ColumnFilter* and *xs* is the underlining *pd.DataFrame*.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"], "dates": ["2020-02-02", "2020-01-01", "2020-02-01", "2020-02-01", "2020-01-02"]})

PipelineFrame(xs).select(("A", "B")).foreach(print)

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

PipelineFrame(xs).select(column("A", "B")).foreach(print)

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

PipelineFrame(xs).select(~column("A")).foreach(print)

#    B       dates
# 0  A  2020-02-02
# 1  B  2020-01-01
# 2  A  2020-02-01
# 3  B  2020-02-01
# 4  B  2020-01-02

# alternatively

PipelineFrame(xs) * ("A", "B") & print

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

PipelineFrame(xs) * column("A", "B") & print

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

PipelineFrame(xs) * ~column("A") & print

#    B       dates
# 0  A  2020-02-02
# 1  B  2020-01-01
# 2  A  2020-02-01
# 3  B  2020-02-01
# 4  B  2020-01-02
```

#### *aggregate*

*aggregate* allows you to map columns from the underlining *pd.DataFrame* to anything. Similar to *map* method, *aggregate* also behaves differently based on a type of the passed parameter:

* *Callable[[pd.Series], object]* - apply passed function to each column of the underlining *pd.DataFrame*.
* *Tuple[Callable[[pd.Series], object], ...]* - apply passed functions to each column of the underlining *pd.DataFrame*.

As with *map* method, the last behaviour has a slightly more complex associated parameter type: *Iterable[Tuple[Union[pd.Series, str], Union[Callable[[pd.Series], object], Iterable[Callable[[pd.Series], object]]]]]*. It is an *Iterable* of pairs. The first value of a pair is either a *pd.Series* or a *str*. If it is a *pd.Series*, it will be mapped to a *str* using a *name* function. The second value is either a single function which is applied to a column of the underlining *pd.DataFrame* or multiple functions which are applied to a column of the underlining *pd.DataFrame*. The names of that column is the first value of a pair.

*aggregate* will always store results of passed functions in a dictionary. A key in that dictionary is a column name. A value in that dictionary is a functions results.

Let's take a look at some examples:

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})

# the first behaviour
print(PipelineFrame(xs).aggregate(np.unique))

# {'A': array([1, 2, 3]), 'B': array(['A', 'B'], dtype=object)}

# the second behaviour
for column, ys in PipelineFrame(xs).aggregate((np.unique, pd.Series.sum)).items():
  print(f"{column}: {tuple(ys)}")

# A: (array([1, 2, 3]), 10)
# B: (array(['A', 'B'], dtype=object), 'ABABB')

# notice, that we had to create tuple(ys), because ys is an Iterable

# the third behaviour
print(
  PipelineFrame(xs)
  .aggregate(
    (
      ("A", sum),
      (xs.B, np.unique),
    )
  )
)

# {'A': 10, 'B': array(['A', 'B'], dtype=object)}

# alternatively

# the first behaviour
print(PipelineFrame(xs) << np.unique)

# {'A': array([1, 2, 3]), 'B': array(['A', 'B'], dtype=object)}

# the second behaviour
for column, ys in (PipelineFrame(xs) << (np.unique, pd.Series.sum)).items():
  print(f"{column}: {tuple(ys)}")

# A: (array([1, 2, 3]), 10)
# B: (array(['A', 'B'], dtype=object), 'ABABB')

# the third behaviour
print(
  PipelineFrame(xs)
  << (
      ("A", sum),
      (xs.B, np.unique),
    )
)

# {'A': 10, 'B': array(['A', 'B'], dtype=object)}
```

#### *foreach*

*foreach* allows you to apply some function to the underlining *pd.DataFrame*. The result of the function will not be used anyhow.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})

PipelineFrame(xs).map(lambda ys: 2 * ys).foreach(print)

#    A   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB

# alternatively

PipelineFrame(xs) / (lambda ys: 2 * ys) & print

#    A   B
# 0  4  AA
# 1  4  BB
# 2  6  AA
# 3  8  BB
# 4  8  BB
```

#### *get*

*get* allows you to get the underlining *pd.DataFrame*.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})
ys = (PipelineFrame(xs).map(lambda ys: 2 * ys)).get()

print(ys)

#    A   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB

# get method does not has an operator form
```

### *append*

*append* allows you to append new columns or rows to a *PipelineFrame* created by functions instead of substituting an original frame wrapped by *PipelineFrame* with the result of concatenation of those columns or rows. *append* can take different types of parameters. Based on parameter's type *append* provides different outputs. Supported types and outputs are following:


* *Callable[[pd.DataFrame], pd.DataFrame]* - returns the same output as *append((fs,))*, where *fs* is a passed parameter.
* *Tuple[Callable[[pd.DataFrame], pd.DataFrame], ...]* - returns a *Tuple[Callable[[pd.DataFrame], pd.DataFrame], ...]* which has an identity function as a first function. Other functions are simply functions of a passed *Tuple* parameter.
* *List[Callable[[pd.Series], pd.Series]]* - returns a *List[Callable[[pd.Series], pd.Series]]* which has an identity function as a first function. Other functions are simply functions of a passed *List* parameter.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})

(
  PipelineFrame(xs)
  / select("A")(lambda ys: ys * 2)
  & print
)

#    A
# 0  2
# 1  2
# 2  4
# 3  6
# 4  6

# notice that, original "A" and "B" columns are not present in the resulting frame

# the first type of the parameter
(
  PipelineFrame(xs)
  / append(select("A")(lambda ys: ys * 2))
  & print
)

#    A  B  A
# 0  1  A  2
# 1  1  B  2
# 2  2  A  4
# 3  3  B  6
# 4  3  B  6

# this time we have another column "A" appended
# if you want to change the name of that column, you could use rename, prefix or sufix functions

(
  PipelineFrame(xs)
  / append(rename(lambda x: "test_" + x)(select("A")(lambda ys: ys * 2)))
  & print
)

#    A  B  test_A
# 0  1  A       2
# 1  1  B       2
# 2  2  A       4
# 3  3  B       6
# 4  3  B       6

# or you can write

(
  PipelineFrame(xs)
  / append(prefix("test_")(select("A")(lambda ys: ys * 2)))
  & print
)

#    A  B  test_A
# 0  1  A       2
# 1  1  B       2
# 2  2  A       4
# 3  3  B       6
# 4  3  B       6

# the second type of the parameter
(
  PipelineFrame(xs)
  / append(
      prefix("new_")(
        (
          select("A")(lambda ys: ys * 2),
          select("B")(lambda ys: "A" + ys)
        )
      )
    )
  & print
)

#    A  B  new_A new_B
# 0  1  A      2    AA
# 1  1  B      2    AB
# 2  2  A      4    AA
# 3  3  B      6    AB
# 4  3  B      6    AB

# the third type of the parameter
(
  PipelineFrame(xs)
  / append([lambda ys: 2 * ys])
  & print
)

#    A   B
# 0  1   A
# 1  1   B
# 2  2   A
# 3  3   B
# 4  3   B
# 0  2  AA
# 1  2  BB
# 2  4  AA
# 3  6  BB
# 4  6  BB
```

### *column*

*column* allows you to specify what columns you want to select. *column* is basically a convenient way to create a value of type *ColumnFilter*. A *ColumnFilter* is a type, that supports *+* (*__add__*) and *~* (*__invert__*) operators.

* When you use *x + y* on two *ColumnFilter* values, you get another *ColumnFilter* value that has columns from *x* and then columns from *y* value.
* When you use *~x* on single *ColumnFilter* value, you get another *ColumnFilter* value that has all columns except columns in *x* value.

A value of type *ColumnFilter* also behaves as a function (supports *__call__*) of type *Callable[[pd.DataFrame], List[str]]*. This function takes a *pd.DataFrame* and returns a list of column names.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"], "dates": ["2020-02-02", "2020-01-01", "2020-02-01", "2020-02-01", "2020-01-02"]})

print(column("A")(xs))
# ['A']

print(column("A", "B")(xs))
# ['A', 'B', 'dates']

print((column("A") + column("B") + column("dates"))(xs))
# ['A', 'B', 'dates']

print((~column("A"))(xs))
# ['B', 'dates']

print((~column("A") + column("B") + column("A"))(xs))
# ['B', 'dates', 'B', 'A']

(
  PipelineFrame(xs)
  * (column("A") + ~column("A", "B"))
  & print
)

#    A       dates
# 0  1  2020-02-02
# 1  1  2020-01-01
# 2  2  2020-02-01
# 3  3  2020-02-01
# 4  3  2020-01-02
```

### *inner*

*inner* is simply:

```python
inner: Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame] = partial(pd.concat, axis="columns", join="inner")
```

### *prefix*

*prefix* is simply:

```python
def prefix(x: str) -> Callable[
    [Union[FrameFunction[pd.DataFrame], Tuple[FrameFunction[pd.DataFrame], ...]]],
    Tuple[FrameFunction[pd.DataFrame], ...]
    ]:

  return rename(lambda y: x + y)
```

### *removecolumns*

*removecolumns* allows you to separate some columns from the rest of frame's columns. *removecolumns* takes column sets to be separated and returns a function which takes a *pd.DataFrame* and returns a *Tuple[pd.DataFrame, ...]*. Number of resulting frames depends on number of column sets to be separated. The resulting *Tuple[pd.DataFrame, ...]* always has the rest of frame's columns as the last element.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"], "C": ["2020-02-02", "2020-01-01", "2020-02-01", "2020-02-01", "2020-01-02"]})

ys, rest = removecolumns(("A",))(xs)

print(ys)

#    A
# 0  1
# 1  1
# 2  2
# 3  3
# 4  3

print(rest)

#    B           C
# 0  A  2020-02-02
# 1  B  2020-01-01
# 2  A  2020-02-01
# 3  B  2020-02-01
# 4  B  2020-01-02

ys, zs, rest = removecolumns(column("A", "B"), ("C",))(xs)

print(ys)

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

print(zs)

#             C
# 0  2020-02-02
# 1  2020-01-01
# 2  2020-02-01
# 3  2020-02-01
# 4  2020-01-02

print(rest)

# Empty DataFrame
# Columns: []
# Index: [0, 1, 2, 3, 4]
```

### *rename*

*rename* allows you to apply some function *Callable[[str], str]* to each column name. *rename* returns a function which takes a *Tuple* of functions (or a single function) of type *Callable[[pd.DataFrame], pd.DataFrame]* and returns a *Tuple* of functions of the same type. That function will apply *Callable[[str], str]* to each column name of each function's *pd.DataFrame* output.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})

# a single function as a parameter
(
  PipelineFrame(xs)
  / rename(lambda x: "_" + x)(lambda xs: xs.loc[:, ["B"]])
  & print
)

#   _B
# 0  A
# 1  B
# 2  A
# 3  B
# 4  B

# a tuple of functions as a parameter
(
  PipelineFrame(xs)
  / rename(lambda x: "_" + x)((
      select("A")(),
      select("B")(lambda ys: 2 * ys)
    ))
  & print
)

#    _A  _B
# 0   1  AA
# 1   1  BB
# 2   2  AA
# 3   3  BB
# 4   3  BB

# if you will not pass any function as a parameter, an identity function will be used
(
  PipelineFrame(xs)
  / rename(lambda x: "_" + x)()
  & print
)

#   _A _B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B
```

### *sufix*

*sufix* is simply:

```python
def sufix(x: str) -> Callable[
    [Union[FrameFunction[pd.DataFrame], Tuple[FrameFunction[pd.DataFrame], ...]]],
    Tuple[FrameFunction[pd.DataFrame], ...]
    ]:

  return rename(lambda y: y + x)
```

### *select*

*select* allows you to map some subset of columns. *select* is basically a convenient way to create a value of type *Selector*. A value of type *Selector*, behaves like a function of type *Callable[[Callable[[pd.DataFrame], pd.DataFrame]], Callable[[pd.DataFrame], pd.DataFrame]]* (*__call__*) or like a function of type *Callable[[Callable[[np.ndarray], np.ndarray]], Callable[[pd.DataFrame], pd.DataFrame]]* (*numpy*).

*select* function takes a list (varargs) of *Union[str, ColumnFilter]* values and returns a value of type *Selector*. Each value of type *str* is converted to *ColumnFilter* by using *column* function and then a list of *ColumnFilter* values is folded into single *ColumnFilter* by using *+* as an operator and value of *ColumnFilter* type, which returns no columns, as an accumulator. That *ColumnFilter* value will be used by *Selector* value to get a subset of some frame columns.

* When you use *Selector* value as a *Callable[[Callable[[pd.DataFrame], pd.DataFrame]], Callable[[pd.DataFrame], pd.DataFrame]]* function (by using *__call__*), your passed function to it will be decorated in a way that the subset of columns will be passed to your function (instead of the whole frame).
* When you use *Selector* value as a *Callable[[Callable[[np.ndarray], np.ndarray]], Callable[[pd.DataFrame], pd.DataFrame]]* function (by using *numpy*), your passed function to it will be decorated in a way that subset of columns will first be converted to *np.ndarray* and then passed to your function. The resulting *np.ndarray* of your function will be wrapped into *pd.DataFrame*. If the result of your function will have the same number of columns as the subset of columns, your *np.ndarray* after wrapping into *pd.DataFrame* will have column names of those columns in the subset. The same behaviour applies to indices. You can turn off indices copying by setting *copy_index=False*.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"], "C": ["2020-02-02", "2020-01-01", "2020-02-01", "2020-02-01", "2020-01-02"]})

# by default, if you do not pass any function, an identity function is used
print(select("A")()(xs))

#    A
# 0  1
# 1  1
# 2  2
# 3  3
# 4  3

def f(xs: pd.DataFrame) -> pd.DataFrame:
  print(xs.columns)
  print(xs.shape)

  return xs.B

print(select("B", "C")(f)(xs))

# Index(['B', 'C'], dtype='object')
# (5, 2)
# 0    A
# 1    B
# 2    A
# 3    B
# 4    B
# Name: B, dtype: object

(
  PipelineFrame(xs)
  / select("A", "B")()
  & print
)

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

# same could be achieved with

(
  PipelineFrame(xs)
  * column("A", "B")
  & print
)

#    A  B
# 0  1  A
# 1  1  B
# 2  2  A
# 3  3  B
# 4  3  B

(
  PipelineFrame(xs)
  / select(~column("A"))(lambda ys: 2 * ys)
  / (select("B")(lambda ys: 3 * ys), select("C")(lambda ys: 2 * ys))
  & print
)

#         B                                         C
# 0  AAAAAA  2020-02-022020-02-022020-02-022020-02-02
# 1  BBBBBB  2020-01-012020-01-012020-01-012020-01-01
# 2  AAAAAA  2020-02-012020-02-012020-02-012020-02-01
# 3  BBBBBB  2020-02-012020-02-012020-02-012020-02-01
# 4  BBBBBB  2020-01-022020-01-022020-01-022020-01-02

# now let's try to use numpy
# it is especially useful when combined with some sklearn.preprocessing estimators

scaler = StandardScaler()
encoder = OneHotEncoder(sparse=False)

(
  PipelineFrame(xs)
  / (
      select("A").numpy(scaler.fit_transform),
      *prefix("encoded_")(select("B").numpy(encoder.fit_transform)),
      select("C")()
    )
  / astype({"C": "datetime64[D]"})
  & print
)

#           A  encoded_0  encoded_1          C
# 0 -1.118034        1.0        0.0 2020-02-02
# 1 -1.118034        0.0        1.0 2020-01-01
# 2  0.000000        1.0        0.0 2020-02-01
# 3  1.118034        0.0        1.0 2020-02-01
# 4  1.118034        0.0        1.0 2020-01-02

# we used select("C")() on the end to include "C" column
# notice that, we used * before prefix("encoded_")(select("B").numpy(encoder.fit_transform))

# if you want to append columns, you can write

scaler = StandardScaler()
encoder = OneHotEncoder(sparse=False)

(
  PipelineFrame(xs)
  / append((
      *prefix("scaled_")(select("A").numpy(scaler.fit_transform)),
      *prefix("encoded_")(select("B").numpy(encoder.fit_transform))
    ))
  / astype({"C": "datetime64[D]"})
  & print
)

#    A  B          C  scaled_A  encoded_0  encoded_1
# 0  1  A 2020-02-02 -1.118034        1.0        0.0
# 1  1  B 2020-01-01 -1.118034        0.0        1.0
# 2  2  A 2020-02-01  0.000000        1.0        0.0
# 3  3  B 2020-02-01  1.118034        0.0        1.0
# 4  3  B 2020-01-02  1.118034        0.0        1.0
```

### *zipframe*

*zipframe* is a convenience function, which allows you to concatenate columns using some *concatenate_columns* function. The difference between *pd.concat* and *zipframe* is that *pd.concat* takes some *Iterable* of columns and returns the result of concatenation immediately, whereas *zipframe* takes some *Iterable* of columns and returns a function which takes another set of columns and concatenates passed earlier *Iterable* of columns with that set.

```python
xs = pd.DataFrame({"A": [1, 1, 2, 3, 3], "B": ["A", "B", "A", "B", "B"]})
ys = pd.DataFrame({"C": ["2020-02-02", "2020-01-01", "2020-02-01", "2020-02-01", "2020-01-02"]})

(
  PipelineFrame(xs)
  / zipframe(ys)
  & print
)

#    A  B           C
# 0  1  A  2020-02-02
# 1  1  B  2020-01-01
# 2  2  A  2020-02-01
# 3  3  B  2020-02-01
# 4  3  B  2020-01-02
```

## *dskit.tensor*

### *create_batches*

*create_batches* is a function which takes *Iterable[Tuple[np.ndarray, ...]]* with length of batches and returns an *Iterable[Tuple[np.ndarray, ...]]* of created batches.

```python
xs = np.arange(15).reshape(-1, 3)
ys = np.arange(10).reshape(-1, 2)

print(xs)

# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]

print(ys)

# [[0 1]
#  [2 3]
#  [4 5]
#  [6 7]
#  [8 9]]

for sub_xs, sub_ys in create_batches(zip(xs, ys), length=3):
  print(sub_xs)
  print(sub_ys)

  print()

# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
# [[0 1]
#  [2 3]
#  [4 5]]
#
# [[ 9 10 11]
#  [12 13 14]]
# [[6 7]
#  [8 9]]
```

### *cycle_tensor*

*cycle_tensor* is a "cycle" function used for tensors. This function takes a *np.ndarray* with *Tuple[int, ...]* and returns "cycled" *np.ndarray*.

```python
xs = np.arange(4).reshape(-1, 2)
print(xs)

# [[0 1]
#  [2 3]]

cycled_xs = cycle_tensor(xs, (3, 3))
print(cycled_xs)

# [[0 1 0 1 0 1]
#  [2 3 2 3 2 3]
#  [0 1 0 1 0 1]
#  [2 3 2 3 2 3]
#  [0 1 0 1 0 1]
#  [2 3 2 3 2 3]]

zeros = cycle_tensor(0, (2, 2, 3))
print(zeros)

# [[[0 0 0]
#   [0 0 0]]
#
#  [[0 0 0]
#   [0 0 0]]]
```

### *expand_tail*

*expand_tail* is simply:

```python
def expand_tail(xs: Tuple[X, ...], length: int, filler: X) -> Tuple[X, ...]:
  count = max(length - len(xs), 0)

  fillers = repeat(filler)
  sliced_fillers = islice(fillers, count)

  expanded = chain(xs, sliced_fillers)
  return tuple(expanded)
```

Example of *expand_tail* usage:

```python
xs = expand_tail((1, 2), length=5, filler=3)
print(xs) # (1, 2, 3, 3, 3)
```

### *expand_tail_dimensions*

*expand_tail_dimensions* is simply:

```python
def expand_tail_dimensions(tensor: np.ndarray, length: int) -> np.ndarray:
  expanded_shape: Shape = expand_tail(tensor.shape, length, filler=1)
  return tensor.reshape(expanded_shape)
```

Example of *expand_tail_dimensions* usage:

```python
xs = np.arange(27).reshape(-1, 3, 3)
ys = expand_tail_dimensions(xs, 5)

print(ys.shape) # (3, 3, 3, 1, 1)
```

### *gridrange*

*gridrange* is a function similar to Python's *range* function. The difference between *gridrange* and *range* is that *gridrange* operates on *Tuple[int, ...]* instead of *int*.

```python
for x in gridrange((2, 3)):
  print(x)

# (0, 0)
# (0, 1)
# (0, 2)
# (1, 0)
# (1, 1)
# (1, 2)

for x in gridrange((1, 1), (3, 4)):
  print(x)

# (1, 1)
# (1, 2)
# (1, 3)
# (2, 1)
# (2, 2)
# (2, 3)

for x in gridrange((1, 1), (10, 20), (5, 5)):
  print(x)

# (1, 1)
# (1, 6)
# (1, 11)
# (1, 16)
# (6, 1)
# (6, 6)
# (6, 11)
# (6, 16)
```

### *iteraxis*

*iteraxis* is a function which takes *np.ndarray* and returns *Iterable[np.ndarray]* along passed axis. This function is similar to *np.apply_along_axis*. The difference between *iteraxis* and *np.apply_along_axis* is that *np.apply_along_axis* applies some function to arrays and *iteraxis* returns those arrays.

```python
xs = np.arange(27).reshape(-1, 3, 3)

for x in iteraxis(xs, axis=-1):
  print(x)

# [0 1 2]
# [3 4 5]
# [6 7 8]
# [ 9 10 11]
# [12 13 14]
# [15 16 17]
# [18 19 20]
# [21 22 23]
# [24 25 26]
```

### *move_tensor*

*move_tensor* is simply:

```python
def move_tensor(source: np.ndarray, destination: np.ndarray, coordinate: Optional[Coordinate] = None) -> np.ndarray:
  tensor = destination.copy()
  move_tensor_inplace(source, tensor, coordinate)

  return tensor
```
Example of *move_tensor* usage:

```python
xs = np.arange(4).reshape(-1, 2)
ys = np.zeros((3, 3), dtype=np.uint)

moved = move_tensor(xs, ys, coordinate=(1, 1))
print(moved)

# [[0 0 0]
#  [0 0 1]
#  [0 2 3]]
```

### *move_tensor_inplace*

*move_tensor_inplace* is a procedure which moves source *np.ndarray* to destination *np.ndarray* at coordinate *Tuple[int, ...]*. Only destination *np.ndarray* is modified. The coordinate is optional.

```python
xs = np.arange(4).reshape(-1, 2)
ys = np.zeros((3, 3), dtype=np.uint)

move_tensor_inplace(xs, ys)
print(ys)

# [[0 1 0]
#  [2 3 0]
#  [0 0 0]]
```

### *next_batch*

*next_batch* is a function used by *create_batches*. *next_batch* takes an *Iterable[Tuple[np.ndarray, ...]]* with length of batch and returns a next batch. The next batch might have smaller length than the passed one.

```python
xs = np.arange(15).reshape(-1, 3)
ys = np.arange(10).reshape(-1, 2)

print(xs)

# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]

print(ys)

# [[0 1]
#  [2 3]
#  [4 5]
#  [6 7]
#  [8 9]]

sub_xs, sub_ys = next_batch(zip(xs, ys), length=3)

print(sub_xs)
print(sub_ys)

# [[0 1 2]
#  [3 4 5]
#  [6 7 8]]
# [[0 1]
#  [2 3]
#  [4 5]]
```

### *slices*

*slices* is simply:

```python
RawSlice = Union[
  Tuple[Optional[int]],
  Tuple[Optional[int], Optional[int]],
  Tuple[Optional[int], Optional[int], Optional[int]]
]

def slices(xs: Iterable[RawSlice]) -> Tuple[slice, ...]:
  ys = starmap(slice, xs)
  return tuple(ys)
```

Example of *slices* usage:

```python
xs = np.arange(9).reshape(-1, 3)
ys = (1, None), (0, 1)

print(xs[slices(ys)])

# [[3]
#  [6]]
```
