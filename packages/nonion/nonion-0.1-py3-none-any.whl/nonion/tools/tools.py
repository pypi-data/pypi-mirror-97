from typing import Callable, Dict, Iterable, Iterator, List, Tuple, TypeVar, Union

from functools import partial
from functools import reduce
from itertools import chain
from itertools import islice
from itertools import repeat
from itertools import starmap

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

Option = Union[Tuple[X], Tuple[()]]
Either = Tuple[Option[X], Option[Y]]

AnyFunction = Callable[[Tuple[object, ...], Dict[str, object]], object]
OptionFunction = Callable[[Tuple[object, ...], Dict[str, object]], Option[object]]
EitherFunction = Callable[[Tuple[object, ...], Dict[str, object]], Either[object, Exception]]

def binary_compose(f: Callable[[Y], Z], g: Callable[[X], Y]) -> Callable[[X], Z]:
  return lambda x: f(g(x))

def lift(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Y]]:
  return partial(map, f)

def fmap(f: Callable[[X], Y], x: Iterable[X]) -> Tuple[Y, ...]:
  return binary_compose(tuple, lift(f))(x)

def bind(f: Callable[[X], Iterable[Y]], x: Iterable[X]) -> Tuple[Y, ...]:
  ys: Iterable[Iterable[Y]] = map(f, x)
  y: Iterable[Y] = chain.from_iterable(ys)

  return tuple(y)

def wraptry(f: AnyFunction) -> OptionFunction:
  def wrapped(*args: object, **kwargs: object) -> Option[object]:
    try:
      return (f(*args, **kwargs),)
    except:
      return ()

  return wrapped

def wrapexcept(f: AnyFunction) -> EitherFunction:
  def wrapped(*args: object, **kwargs: object) -> Option[object]:
    try:
      y = f(*args, **kwargs)
      return ((y,), ())
    except Exception as e:
      return ((), (e,))

  return wrapped

def maptry(f: Callable[[X], Y], xs: Iterable[X]) -> Iterable[Y]:
  ys: Iterable[Option[Y]] = map(wraptry(f), xs)
  return chain.from_iterable(ys)

wrapnext: Callable[[Iterator[X]], Option[X]] = wraptry(next)

def wrapeek(xs: Iterable[X]) -> Tuple[Option[X], Iterable[X]]:
  xs = iter(xs)
  x = wrapnext(xs)

  return x, chain(x, xs)

def iterfind(fs: Iterable[Callable[[X], bool]], xs: Iterable[X]) -> Iterable[Option[X]]:
  xs = iter(xs)
  buffer = []

  for f in fs:
    x = find(f, buffer)

    if not x:
      x, buffer = find_and_collect(f, xs, buffer)

    yield x

def find(f: Callable[[X], bool], xs: Iterable[X]) -> Option[X]:
  xs = filter(f, xs)
  return wrapnext(xs)

def find_and_collect(
    f: Callable[[X], bool],
    xs: Iterator[X],
    buffer: List[X]
    ) -> Tuple[Option[X], List[X]]:

  x = wrapnext(xs)

  while x:
    buffer.extend(x)

    if f(*x):
      return x, buffer

    x = wrapnext(xs)

  return (), buffer

def findindex(f: Callable[[X], bool], xs: Iterable[X]) -> Option[int]:
  yxs = enumerate(xs)

  g: Callable[[Tuple[int, X]], bool] = binary_compose(f, second)
  yx: Option[Tuple[int, X]] = find(g, yxs)

  return fmap(first, yx)

def first(xy: Tuple[X, Y]) -> X:
  return xy[0]

def second(xy: Tuple[X, Y]) -> Y:
  return xy[1]

def mapexplode(f: Callable[[X, Y], Z], x: X, ys: Iterable[Y]) -> Iterable[Z]:
  xs_and_ys: Iterable[Tuple[X, Y]] = explode(x, ys)
  return starmap(f, xs_and_ys)

def explode(x: X, ys: Iterable[Y]) -> Iterable[Tuple[X, Y]]:
  return zip(repeat(x), ys)

def slide(xs: Iterable[X], length: int = 2, step: int = 1) -> Iterable[Tuple[X, ...]]:
  xs = iter(xs)

  window = islice(xs, length)
  window = tuple(window)

  while len(window) > 0:
    yield window

    window = chain(window[step:], islice(xs, step))
    window = tuple(window)

def take(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return lambda xs: islice(xs, n)

def drop(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return lambda xs: islice(xs, n, None)

def cachepartial(f: AnyFunction, *args: object, **kwargs: object) -> AnyFunction:
  f = partial(f, *args, **kwargs)
  return cache(f)

def cache(f: AnyFunction) -> AnyFunction:
  def cached() -> Iterable[object]:
    args, kwargs = yield
    y = f(*args, **kwargs)

    while True:
      yield y

  cached = cached()
  next(cached)

  def wrapped(*args: object, **kwargs: object) -> object:
    return cached.send((args, kwargs))

  return wrapped

def shift(f: AnyFunction, *args: object, **kwargs: object) -> Callable[[object], object]:
  def wrapped(x: object) -> object:
    return f(x, *args, **kwargs)

  return wrapped

def key(f: Callable[[X], Z]) -> Callable[[Tuple[X, Y]], Tuple[Z, Y]]:
  g: Callable[[Tuple[X, Y]], Z] = binary_compose(f, first)
  return lambda xy: (g(xy), second(xy))

def value(f: Callable[[Y], Z]) -> Callable[[Tuple[X, Y]], Tuple[X, Z]]:
  g: Callable[[Tuple[X, Y]], Z] = binary_compose(f, second)
  return lambda xy: (first(xy), g(xy))

def flip(f: Callable[[Y, X], Z]) -> Callable[[X, Y], Z]:
  return lambda x, y: f(y, x)

def fold(f: Callable[[Y, X], Y], acc: Y) -> Callable[[Iterable[X]], Y]:
  return lambda xs: reduce(f, xs, acc)

def zipl(xs: Iterable[X]) -> Callable[[Iterable[Y]], Iterable[Tuple[X, Y]]]:
  return lambda ys: zip(xs, ys)

def zipr(ys: Iterable[Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: zip(xs, ys)

def flatten(xyz: Tuple[Tuple[X, Y], Z]) -> Tuple[X, Y, Z]:
  (x, y), z = xyz
  return x, y, z

def zipmapl(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[Y, X]]]:
  return lambda xs: map(lambda x: (f(x), x), xs)

def zipmapr(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: map(lambda x: (x, f(x)), xs)

def call(fx: Tuple[Callable[[Tuple[object, ...]], Y], Tuple[object, ...]]) -> Y:
  f, *x = fx
  return f(*x)

def as_function(xys: Iterable[Tuple[X, Y]]) -> Callable[[X], Y]:
  return dict(xys).__getitem__
