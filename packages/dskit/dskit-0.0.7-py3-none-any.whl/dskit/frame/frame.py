from typing import Callable, Dict, Iterable, Tuple, TypeVar, Union

import operator

from functools import partial
from itertools import count

import numpy as np
import pandas as pd

from nonion import Option
from nonion import Pipeline
from nonion import as_function
from nonion import first
from nonion import key
from nonion import mapexplode
from nonion import second
from nonion import star
from nonion import value
from nonion import zipl
from nonion import zipr

Y = TypeVar("Y")

Encoder = Callable[[Tuple[object, ...]], pd.DataFrame]
FrameFunction = Callable[[pd.DataFrame], Y]
SeriesFunction = Callable[[pd.Series], Y]

COLUMNS_AXIS = 1

COLUMNS_SORT_PARAMETERS = {
  "axis": COLUMNS_AXIS,
  "kind": "stable"
}

def unique(frame: pd.DataFrame) -> Dict[str, Tuple[object, ...]]:
  return (
    Pipeline(frame.iteritems())
    / value(lambda y: y.unique())
    / value(lambda y: y.astype(object))
    / value(tuple)
    >> dict
  )

def create_dummifier(
    xys: Dict[str, Tuple[object, ...]],
    separator: str = "_",
    sort_columns: bool = True
  ) -> FrameFunction[pd.DataFrame]:

  create: Callable[[str, Tuple[object, ...]], Encoder] = partial(create_encoder, separator=separator)

  name_to_encoder: Dict[str, Encoder] = (
    Pipeline(xys.items())
    / star(lambda x, y: (x, create(x, y)))
    >> dict
  )

  sort = (lambda x: x.sort_index(**COLUMNS_SORT_PARAMETERS)) if sort_columns else (lambda x: x)

  def dummify(frame: pd.DataFrame) -> pd.DataFrame:
    sorted_frame: pd.DataFrame = sort(frame)

    return (
      Pipeline(sorted_frame.iteritems())
      / key(lambda x: name_to_encoder.get(x, pd.DataFrame))
      / star(lambda f, x: f(x))
      >> partial(pd.concat, axis=COLUMNS_AXIS)
    )

  return dummify

def create_encoder(x: str, ys: Tuple[object, ...], separator: str = "_") -> Encoder:
  encode: Callable[[Tuple[object, ...]], np.ndarray] = create_numpy_encoder(ys)

  columns: Iterable[str] = mapexplode(operator.add, x + separator, map(str, ys))
  columns = tuple(columns)

  def wrapped(zs: Tuple[object, ...]) -> pd.DataFrame:
    frame = encode(zs)
    return pd.DataFrame(frame, columns=columns)

  return wrapped

def create_numpy_encoder(xs: Tuple[object, ...]) -> Callable[[Tuple[object, ...]], np.ndarray]:
  to_index: Callable[[object], Option[int]] = Pipeline(xs) // zipr(count(0)) >> as_function

  def encode(ys: Tuple[object, ...]) -> np.ndarray:
    matrix = np.zeros((len(ys), len(xs)), dtype=np.int)

    row_to_column = (
      Pipeline(ys)
      / to_index
      // zipl(count(0))
      % second
      / value(first)
    )

    for i, j in row_to_column:
      matrix[i, j] = 1

    return matrix

  return encode

def astype(t: Union[Union[str, type], Dict[str, Union[str, type]]]) -> Callable[[Union[pd.DataFrame, pd.Series]], Union[pd.DataFrame, pd.Series]]:
  return lambda xs: xs.astype(t)

def transformrows(
    f: SeriesFunction[pd.Series],
    xs: pd.DataFrame,
    concatenate: Callable[[Iterable[pd.Series]], pd.DataFrame] = partial(pd.concat, axis="columns")
    ) -> pd.DataFrame:

  ys: Iterable[pd.Series] = maprows(f, xs)

  return (
    Pipeline(ys)
    >> concatenate
  ).transpose()

def maprows(f: SeriesFunction[Y], xs: pd.DataFrame) -> Iterable[Y]:
  return (
    Pipeline(xs.iterrows())
    / second
    / f
  )

def name(x: Union[pd.Series, str]) -> str:
  return x if isinstance(x, str) else (x.name or "")
