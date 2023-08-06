from typing import Callable, Dict, Iterable, Tuple, TypeVar, Union

import operator

from functools import partial

import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder

from nonion import Pipeline
from nonion import key
from nonion import mapexplode
from nonion import second
from nonion import star
from nonion import value

Y = TypeVar("Y")

Encoder = Callable[[Tuple[object, ...]], pd.DataFrame]
FrameFunction = Callable[[pd.DataFrame], Y]
SeriesFunction = Callable[[pd.Series], Y]

COLUMNS_AXIS = 1

COLUMNS_SORT_PARAMETERS = {
  "axis": COLUMNS_AXIS,
  "kind": "stable"
}

ENCODER_PARAMETERS = {
  "sparse": False,
  "handle_unknown": "ignore"
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
  encoder = OneHotEncoder(**ENCODER_PARAMETERS)

  expanded_ys = np.expand_dims(ys, axis=-1)
  encoder.fit(expanded_ys)

  columns: Iterable[str] = mapexplode(operator.add, x + separator, map(str, ys))
  columns = tuple(columns)

  def encode(zs: Tuple[object, ...]) -> pd.DataFrame:
    expanded_zs = np.expand_dims(zs, axis=-1)
    frame = encoder.transform(expanded_zs)

    return pd.DataFrame(frame, columns=columns)

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
