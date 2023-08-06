from typing import Iterable, Iterator, Optional, Tuple, TypeVar, Union

import operator

from itertools import chain
from itertools import islice
from itertools import product
from itertools import repeat
from itertools import starmap

import numpy as np

X = TypeVar("X")

Coordinate = Tuple[int, ...]
RawSlice = Union[
  Tuple[Optional[int]],
  Tuple[Optional[int], Optional[int]],
  Tuple[Optional[int], Optional[int], Optional[int]]
]
Shape = Tuple[int, ...]

def slices(xs: Iterable[RawSlice]) -> Tuple[slice, ...]:
  ys = starmap(slice, xs)
  return tuple(ys)

def create_batches(xs: Iterable[Tuple[np.ndarray, ...]], length: int = 32) -> Iterable[Tuple[np.ndarray, ...]]:
  xs = iter(xs)
  batch: Tuple[np.ndarray, ...] = next_batch(xs, length)

  while batch:
    yield batch
    batch: Tuple[np.ndarray, ...] = next_batch(xs, length)

def next_batch(xs: Iterator[Tuple[np.ndarray, ...]], length: int = 32) -> Tuple[np.ndarray, ...]:
  batch = islice(xs, length)
  stacked_batch = map(np.stack, zip(*batch))

  return tuple(stacked_batch)

def cycle_tensor(tensor: Union[np.ndarray, float], shape: Shape) -> np.ndarray:
  tensor = tensor if isinstance(tensor, np.ndarray) else np.array(tensor)
  expanded: np.ndarray = expand_tail_dimensions(tensor, len(shape))

  for axis, axis_length in enumerate(shape):
    cycled_axis: Tuple[np.ndarray, ...] = expand_tail((expanded,), axis_length, filler=expanded)
    expanded = np.concatenate(cycled_axis, axis=axis)

  return expanded

def expand_tail_dimensions(tensor: np.ndarray, length: int) -> np.ndarray:
  expanded_shape: Shape = expand_tail(tensor.shape, length, filler=1)
  return tensor.reshape(expanded_shape)

def expand_tail(xs: Tuple[X, ...], length: int, filler: X) -> Tuple[X, ...]:
  count = max(length - len(xs), 0)

  fillers = repeat(filler)
  sliced_fillers = islice(fillers, count)

  expanded = chain(xs, sliced_fillers)
  return tuple(expanded)

def gridrange(start: Coordinate, end: Optional[Coordinate] = None, step: Optional[Coordinate] = None) -> Iterable[Coordinate]:
  if end is None:
    end = start
    start = expand_tail((0,), len(end), filler=0)

  step = step or expand_tail((1,), len(start), filler=1)

  ranges = map(range, start, end, step)
  return product(*ranges)

def iteraxis(tensor: np.ndarray, axis: int = 0) -> Iterable[np.ndarray]:
  transposed = np.moveaxis(tensor, axis, -1)
  return map(lambda x: transposed[x], np.ndindex(transposed.shape[:-1]))

def move_tensor(source: np.ndarray, destination: np.ndarray, coordinate: Optional[Coordinate] = None) -> np.ndarray:
  tensor = destination.copy()
  move_tensor_inplace(source, tensor, coordinate)

  return tensor

def move_tensor_inplace(source: np.ndarray, destination: np.ndarray, coordinate: Optional[Coordinate] = None):
  coordinate = coordinate or (0,)

  start: Coordinate = expand_tail(coordinate, source.ndim, filler=0)
  end = map(operator.add, start, source.shape)

  raw_subslices = zip(start, end)
  subslices = slices(raw_subslices)

  destination[subslices] = source
