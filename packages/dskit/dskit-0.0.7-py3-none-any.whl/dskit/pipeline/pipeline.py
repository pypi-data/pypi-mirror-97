from typing import Callable, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar, Union

import operator

from functools import partial
from itertools import chain

import numpy as np
import pandas as pd

from nonion import Function
from nonion import Pipeline
from nonion import first
from nonion import fold
from nonion import groupon
from nonion import key
from nonion import lift
from nonion import second
from nonion import star
from nonion import value

from dskit.frame import FrameFunction
from dskit.frame import SeriesFunction
from dskit.frame import maprows
from dskit.frame import name
from dskit.frame import transformrows

from dskit.pipeline.column import ColumnFilter
from dskit.pipeline.column import column

X = TypeVar("X")
Y = TypeVar("Y")

class PipelineFrame:
  pass

class PipelineFrame:
  _xs: Iterable[pd.DataFrame]
  _concatenate: Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame]

  def __init__(self,
      xs: pd.DataFrame,
      concatenate_columns: Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame] = partial(pd.concat, axis="columns")
      ):

    self._xs = (xs,)
    self._concatenate = concatenate_columns

  def __truediv__(self,
      fs: Union[
          FrameFunction[pd.DataFrame],
          Tuple[FrameFunction[pd.DataFrame], ...],
          List[SeriesFunction[pd.Series]],
          Iterable[Tuple[Union[pd.Series, str], Union[FrameFunction[pd.Series], SeriesFunction[pd.Series]]]]
        ]
      ) -> PipelineFrame:

    return self.map(fs)

  def map(self,
      fs: Union[
          FrameFunction[pd.DataFrame],
          Tuple[FrameFunction[pd.DataFrame], ...],
          List[SeriesFunction[pd.Series]],
          Iterable[Tuple[Union[pd.Series, str], Union[FrameFunction[pd.Series], SeriesFunction[pd.Series]]]]
        ]
      ) -> PipelineFrame:

    if isfunction(fs) or (isinstance(fs, tuple) and len(fs) > 0 and isfunction(first(fs))) or isinstance(fs, list):
      return self.apply(fs)

    fs = Pipeline(fs) / key(name)

    def g(xs: pd.DataFrame) -> pd.DataFrame:
      group_to_functions = groupon_presence(first, fs, xs.columns)

      if False not in group_to_functions and True in group_to_functions:
        xs = xs.copy()

      gs = (
        Pipeline(group_to_functions.items())
        * second
      )

      return self._get_apply(gs)(xs)

    self._xs = map(g, self._xs)
    return self

  def __floordiv__(self,
      fs: Union[
          FrameFunction[pd.DataFrame],
          Tuple[FrameFunction[pd.DataFrame], ...],
          List[SeriesFunction[pd.Series]],
          Iterable[Tuple[Union[pd.Series, str], Union[FrameFunction[pd.Series], SeriesFunction[pd.Series]]]]
        ]
      ) -> PipelineFrame:

    return self.apply(fs)

  def apply(self,
      fs: Union[
          FrameFunction[pd.DataFrame],
          Tuple[FrameFunction[pd.DataFrame], ...],
          List[SeriesFunction[pd.Series]],
          Iterable[Tuple[Union[pd.Series, str], Union[FrameFunction[pd.Series], SeriesFunction[pd.Series]]]]
        ]
      ) -> PipelineFrame:

    self._xs = map(self._get_apply(fs), self._xs)
    return self

  def _get_apply(self,
      fs: Union[
          FrameFunction[pd.DataFrame],
          Tuple[FrameFunction[pd.DataFrame], ...],
          List[SeriesFunction[pd.Series]],
          Iterable[Tuple[Union[pd.Series, str], Union[FrameFunction[pd.Series], SeriesFunction[pd.Series]]]]
        ]
      ) -> FrameFunction[pd.DataFrame]:

    if isfunction(fs):
      return fs

    if isinstance(fs, tuple) and len(fs) > 0 and isfunction(first(fs)):
      z: FrameFunction[Iterable[pd.DataFrame]] = lambda xs: map(lambda f: f(xs), fs)
      return Function() / z / self._concatenate

    if isinstance(fs, list):
      z = partial(transformrows, concatenate=self._concatenate)
      gs: Iterable[FrameFunction[pd.DataFrame]] = map(lambda f: partial(z, f), fs)

      return lambda xs: (Pipeline(gs) / (lambda f: f(xs)) / pd.DataFrame.transpose >> self._concatenate).transpose()

    fs = Pipeline(fs) / key(name)

    def g(xs: pd.DataFrame) -> pd.DataFrame:
      group_to_functions = groupon_presence(first, fs, xs.columns)

      new_columns_functions: Tuple[Tuple[str, FrameFunction[pd.Series]], ...] = group_to_functions.get(False, ())
      old_columns_functions: Tuple[Tuple[str, SeriesFunction[pd.Series]], ...] = group_to_functions.get(True, ())

      new_columns: Tuple[pd.Series, ...] = (
        Pipeline(new_columns_functions)
        / value(lambda f: f(xs))
        / star(lambda n, ys: ys.rename(n, inplace=True))
        >> tuple
      )

      ys = self._concatenate((xs, *new_columns)) if new_columns else xs

      for n, f in old_columns_functions:
        ys.loc[:, n] = f(ys.loc[:, n])

      return ys

    return g

  def __mod__(self,
      fs: Union[
          FrameFunction[np.ndarray],
          Tuple[FrameFunction[np.ndarray], ...],
          List[SeriesFunction[bool]],
          Iterable[Tuple[Union[pd.Series, str], SeriesFunction[np.ndarray]]]
        ]
      ) -> PipelineFrame:

    return self.filter(fs)

  def filter(self,
      fs: Union[
          FrameFunction[np.ndarray],
          Tuple[FrameFunction[np.ndarray], ...],
          List[SeriesFunction[bool]],
          Iterable[Tuple[Union[pd.Series, str], SeriesFunction[np.ndarray]]]
        ]
      ) -> PipelineFrame:

    self._xs = map(self._get_filter(fs), self._xs)
    return self

  def _get_filter(self,
      fs: Union[
          FrameFunction[np.ndarray],
          Tuple[FrameFunction[np.ndarray], ...],
          List[SeriesFunction[bool]],
          Iterable[Tuple[Union[pd.Series, str], SeriesFunction[np.ndarray]]]
        ]
      ) -> FrameFunction[pd.DataFrame]:

    if isfunction(fs):
      return lambda xs: xs.iloc[:, fs(xs)]

    if isinstance(fs, tuple) and len(fs) > 0 and isfunction(first(fs)):
      z: FrameFunction[Iterable[np.ndarray]] = lambda xs: map(lambda f: f(xs), fs)
      g: FrameFunction[np.ndarray] = Function() / z / tuple / partial(np.all, axis=0)

      return self._get_filter(g)

    if isinstance(fs, list):
      z = lambda x: all(map(lambda f: f(x), fs))
      g = Function() / partial(maprows, z) / list

      return lambda xs: xs.iloc[g(xs)]

    fs = Pipeline(fs) / key(name)

    def g(xs: pd.DataFrame) -> pd.DataFrame:
      ys: Tuple[np.ndarray, ...] = (
        Pipeline(fs)
        % star(lambda n, _: n in xs.columns)
        / star(lambda n, f: f(xs.loc[:, n]))
        >> tuple
      )

      if not ys:
        return xs

      zs = np.all(ys, axis=0)
      return xs.iloc[zs]

    return g

  def __lshift__(self,
      fs: Union[
          SeriesFunction[object],
          Tuple[SeriesFunction[object], ...],
          Iterable[Tuple[Union[pd.Series, str], Union[SeriesFunction[object], Iterable[SeriesFunction[object]]]]]
        ]
      ) -> Union[Dict[str, object], Dict[str, Iterable[object]]]:

    return self.aggregate(fs)

  def aggregate(self,
      fs: Union[
          SeriesFunction[object],
          Tuple[SeriesFunction[object], ...],
          Iterable[Tuple[Union[pd.Series, str], Union[SeriesFunction[object], Iterable[SeriesFunction[object]]]]]
        ]
      ) -> Union[Dict[str, object], Dict[str, Iterable[object]]]:

    if isfunction(fs):
      xs, *_ = self._xs

      return (
        Pipeline(xs.items())
        / value(fs)
        >> dict
      )

    if isinstance(fs, tuple) and len(fs) > 0 and isfunction(first(fs)):
      xs, *_ = self._xs

      return (
        Pipeline(xs.items())
        / value(lambda x: map(lambda f: f(x), fs))
        >> dict
      )

    fs = Pipeline(fs) / key(name)

    xs, *_ = self._xs

    return (
      Pipeline(fs)
      % star(lambda n, _: n in xs.columns)
      / star(lambda n, gs: (n, gs(xs.loc[:, n]) if isfunction(gs) else map(lambda g: g(xs.loc[:, n]), gs)))
      >> dict
    )

  def __mul__(self,
      fs: Union[
          Iterable[Union[pd.Series, str]],
          ColumnFilter
        ]
      ) -> PipelineFrame:

    return self.select(fs)

  def select(self,
      fs: Union[
          Iterable[Union[pd.Series, str]],
          ColumnFilter
        ]
      ) -> PipelineFrame:

    self._xs = map(self._get_select(fs), self._xs)
    return self

  def _get_select(self,
      fs: Union[
          Iterable[Union[pd.Series, str]],
          ColumnFilter
        ]
      ) -> FrameFunction[pd.DataFrame]:

    if not isinstance(fs, ColumnFilter):
      fs = Pipeline(fs) / name >> tuple
      fs: ColumnFilter = column(*fs)

    return lambda xs: xs.loc[:, fs(xs)]

  def __rshift__(self, f: FrameFunction[X]) -> X:
    return self.collect(f)

  def collect(self, f: FrameFunction[X]) -> X:
    xs, *_ = self._xs
    return f(xs)

  def __and__(self, consumer: FrameFunction[None]):
    return self.foreach(consumer)

  def foreach(self, consumer: FrameFunction[None]):
    xs, *_ = self._xs
    consumer(xs)

  def __iter__(self) -> Iterator[pd.Series]:
    xs, *_ = self._xs
    return iter(maprows(lambda x: x, xs))

  def get(self) -> pd.DataFrame:
    xs, *_ = self._xs
    return xs

  def __or__(self, y: PipelineFrame) -> PipelineFrame:
    return self.zipr(y)

  def zipr(self,
      y: PipelineFrame,
      concatenate: Optional[Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame]] = None
      ) -> PipelineFrame:

    concatenate = concatenate or self._concatenate

    z = PipelineFrame((), concatenate_columns=concatenate)
    z._xs = map(concatenate, zip(self._xs, y._xs))

    return z

  def zipl(self,
      y: PipelineFrame,
      concatenate: Optional[Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame]] = None
      ) -> PipelineFrame:

    return y.zipr(self, concatenate or self._concatenate)

def isfunction(f: object) -> bool:
  return "__call__" in dir(f)

def groupon_presence(f: Callable[[X], Y], xs: Iterable[X], ys: Tuple[Y, ...]) -> Dict[bool, Tuple[X, ...]]:
  return (
    Pipeline(xs)
    // groupon(lambda x: f(x) in ys)
    / value(tuple)
    >> dict
  )

def zipframe(
    *args: Union[pd.Series, pd.DataFrame],
    concatenate_columns: Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame] = partial(pd.concat, axis="columns")
    ) -> FrameFunction[pd.DataFrame]:

  return lambda xs: concatenate_columns(chain((xs,), args))

inner: Callable[[Iterable[Union[pd.Series, pd.DataFrame]]], pd.DataFrame] = partial(pd.concat, axis="columns", join="inner")

def append(
    fs: Union[
        FrameFunction[pd.DataFrame],
        Tuple[FrameFunction[pd.DataFrame], ...],
        List[SeriesFunction[pd.Series]]
      ]
    ) -> Union[Tuple[FrameFunction[pd.DataFrame], ...], List[SeriesFunction[pd.Series]]]:

  if isfunction(fs):
    return append((fs,))

  if isinstance(fs, tuple):
    return (lambda xs: xs, *fs)

  return [lambda xs: xs, *fs]

def rename(g: Callable[[str], str]) -> Callable[
    [Union[FrameFunction[pd.DataFrame], Tuple[FrameFunction[pd.DataFrame], ...]]],
    Tuple[FrameFunction[pd.DataFrame], ...]
    ]:

  return partial(rename_core, g)

def rename_core(
    g: Callable[[str], str],
    fs: Union[
        FrameFunction[pd.DataFrame],
        Tuple[FrameFunction[pd.DataFrame], ...]
      ] = lambda xs: xs
    ) -> Tuple[FrameFunction[pd.DataFrame], ...]:

  if isfunction(fs):
    return rename_core(g, (fs,))

  rename_columns = lambda ys: Pipeline(ys) / str / g >> pd.Series

  def rename_frame(xs: pd.DataFrame) -> pd.DataFrame:
    ys = rename_columns(xs.columns)
    return pd.DataFrame(xs.to_numpy(), index=xs.index, columns=ys)

  gs = map(lambda f: Function() / f / rename_frame, fs)
  return tuple(gs)

def prefix(x: str) -> Callable[
    [Union[FrameFunction[pd.DataFrame], Tuple[FrameFunction[pd.DataFrame], ...]]],
    Tuple[FrameFunction[pd.DataFrame], ...]
    ]:

  return rename(lambda y: x + y)

def sufix(x: str) -> Callable[
    [Union[FrameFunction[pd.DataFrame], Tuple[FrameFunction[pd.DataFrame], ...]]],
    Tuple[FrameFunction[pd.DataFrame], ...]
    ]:

  return rename(lambda y: y + x)

def removecolumns(
    *args: Union[
        Iterable[Union[pd.Series, str]],
        ColumnFilter
      ]
    ) -> FrameFunction[Tuple[pd.DataFrame, ...]]:

  to_column_filter = Function() / lift(name) / star(column)

  columns = (
    Pipeline(args)
    / (lambda x: x if isinstance(x, ColumnFilter) else to_column_filter(x))
    >> tuple
  )

  all_columns: ColumnFilter = fold(operator.add, column())(columns)
  rest_columns = ~all_columns

  def g(xs: pd.DataFrame) -> Tuple[pd.DataFrame, ...]:
    get = lambda f: xs.loc[:, f(xs)]

    removed = Pipeline(columns) / get >> tuple
    return removed + (get(rest_columns),)

  return g
