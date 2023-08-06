from typing import Callable, List, Union

import operator

from functools import partial

import numpy as np
import pandas as pd

from nonion import Function
from nonion import Pipeline
from nonion import fold

from dskit.frame import FrameFunction

from dskit.tensor import expand_tail_dimensions

class ColumnFilter:
  pass

class ColumnFilter:
  get: FrameFunction[List[str]]

  def __init__(self, get: FrameFunction[List[str]] = lambda xs: list(xs.columns)):
    self.get = get

  def __invert__(self) -> ColumnFilter:
    return self.invert()

  def invert(self) -> ColumnFilter:
    def inverse(xs: pd.DataFrame) -> List[str]:
      ys: List[str] = self(xs)
      g: FrameFunction[List[str]] = create_column_filter(lambda x: x not in ys)

      return g(xs)

    return ColumnFilter(inverse)

  def __add__(self, y: ColumnFilter) -> ColumnFilter:
    return self.combine(y)

  def combine(self, y: ColumnFilter) -> ColumnFilter:
    return ColumnFilter(lambda xs: self(xs) + y(xs))

  def __call__(self, xs: pd.DataFrame) -> List[str]:
    return self.get(xs)

def column(*args: str) -> ColumnFilter:
  get: FrameFunction[List[str]] = create_column_filter(lambda x: x in args)
  return ColumnFilter(get)

def create_column_filter(p: Callable[[str], bool]) -> FrameFunction[List[str]]:
  return lambda xs: Pipeline(xs.columns) % p >> list

class Selector:
  get: FrameFunction[pd.DataFrame]

  def __init__(self, get: FrameFunction[List[str]] = lambda xs: xs.columns):
    self.get = lambda xs: xs.loc[:, get(xs)]

  def __call__(self, f: FrameFunction[pd.DataFrame] = lambda x: x) -> FrameFunction[pd.DataFrame]:
    return Function() / self.get / f

  def numpy(self, f: Callable[[np.ndarray], np.ndarray], copy_index: bool = True) -> FrameFunction[pd.DataFrame]:
    def g(xs: pd.DataFrame) -> pd.DataFrame:
      ys: pd.DataFrame = self()(xs)
      z = Function() / pd.DataFrame.to_numpy / f / get_frame_wrapper(ys, copy_index=copy_index)

      return z(ys)

    return g

def get_frame_wrapper(xs: pd.DataFrame, copy_index: bool = True) -> Callable[[np.ndarray], pd.DataFrame]:
  def wrap(ys: np.ndarray) -> pd.DataFrame:
    create_frame = pd.DataFrame

    if ys.shape[0] == len(xs) and copy_index:
      create_frame = partial(create_frame, index=xs.index)

    if ys.ndim < 2:
      ys = expand_tail_dimensions(ys, 2)

    if ys.shape[1] == len(xs.columns):
      create_frame = partial(create_frame, columns=xs.columns)

    return create_frame(ys)

  return wrap

def select(*args: Union[str, ColumnFilter]) -> Selector:
  y = (
    Pipeline(args)
    / (lambda x: column(x) if isinstance(x, str) else x)
    >> fold(operator.add, ColumnFilter(lambda _: []))
  )

  return Selector(y)
