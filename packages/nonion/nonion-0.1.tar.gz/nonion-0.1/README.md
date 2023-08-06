# NOnion

NOnion is a Python package that provides tools for Functional Programming. One of its aims is to eliminate nested function calls such as **z(g(f(x)))** which remind an __onion__.

# Installing

```bash
pip install nonion
```

# Tutorial

NOnion consists of two submodules:

* *nonion.tools* - contains a set of functions and types that __might__ simplify your workflow with Functional Programming in Python,
* *nonion.loader* - contains a wrapper which takes a function *Callable[[io.IOBase], X]* (such as *json.load*), and returns a function *Callable[[typing.Optional[str]], nonion.Option[X]]*.

Also NOnion provides two handful tools:

* *Function* - a wrapper of **any** Python *Callable*,
* *Pipeline* - a wrapper of **any** Python *Iterable*.

It is important to understand that *NOnion* provides tools used for FP in context of Python. Because it is impossible to fully implement some core concepts of FP in Python, *NOnion* provides tools that resemble other FP languages tools, but are not exactly the same tools.

## *nonion.tools*

### *AnyFunction*

*AnyFunction* is a type alias that describes **any** Python function. *AnyFunction* has following two assumptions:

* *Tuple[object, ...]* - is interpreted as *args*,
* *Dict[str, object]* - is interpreted as *kwargs*.

*AnyFunction* is defined as follows:

```python
AnyFunction = Callable[[Tuple[object, ...], Dict[str, object]], object]
```

### *Option*

*Option* is a type alias. *Option* resembles Haskell's *Maybe* in Python. *Option* is defined as follows:

```python
Option = Union[Tuple[X], Tuple[()]]
```

As we can see *Option* is simply some *tuple* that might contain a single value or be an empty *tuple*.
It means that in order to initialize an *Option* you can simply write:

```python
x = () # empty Option
y = (3,) # Option with value 3
```

You can easily check whether an *Option* is empty:

```python
def f(x: int) -> Option[int]:
  return (x,) if x < 3 else ()

x: Option[int] = f(5)

if not x:
  print("Option is empty") # Option is empty
```

You can also provide an alternative value if *Option* is empty and immediately try to unwrap the *Option*:

```python
x: Option[int] = f(5)
y, *_ = x or (42,)

print(y) # 42
```

```python
# alternatively

x: Option[int] = f(1)
z = x or (42,)

# notice: if you pass an empty *z to a single argument function, you will get an error
print(*z) # 1
```

If you need to apply some function to a content of the *Option*, you can use *nonion.fmap*:

```python
x: Option[int] = f(5)
z: Option[int] = fmap(lambda y: y + 1, x)

for i in z:
  print(i)
```

Because *Option* is simply a *tuple* under the hood, you can apply any Python function (that operates on *tuple*) to an instance of an *Option*.

### *Either*

*Either* is a type alias. *Either* is defined as follows:

```python
Either = Tuple[Option[X], Option[Y]]
```

*Either* can be used when you need to return either first value or a second value:

```python
def readline(path: str) -> Either[str, str]:
  buffer: Option[IOBase] = wraptry(open)(path)

  if not buffer:
    return ((), ("error occurred during open",))

  line: Option[str] = fmap(lambda x: x.readline(), buffer)
  fmap(lambda x: x.close(), buffer)

  return (line, ())

line, error = readline("requirements.txt")

if line:
  print(*line)
else:
  print(*error)
```

Because *Either* is simply a type alias, it does not checks whether only single value is passed.

### *as_function*

*as_function* is simply:

```python
def as_function(xys: Iterable[Tuple[X, Y]]) -> Callable[[X], Y]:
  return dict(xys).__getitem__
```

When using *as_function* make sure, that a first value of a tuple could be a key dictionary. Example of *as_function* usage:

```python
successor: Callable[[int], int] = Pipeline(range(10)) // zipmapr(lambda x: x + 1) >> as_function
successor(1) # 2
```

### *binary_compose*

*binary_compose* is an implementation of a ``Function composition" defined as $( f \circ g )(x) = f(g(x))$.

```python
xs = "a", "ab", "c"
yxs = enumerate(xs)

p: Callable[[Tuple[int, str]], bool] = binary_compose(lambda x: x.startswith("a"), second)
filtered: Iterable[Tuple[int, str]] = filter(p, yxs)

ys = map(first, filtered)
print(tuple(ys)) # (0, 1)
```

### *bind*

*bind* resembles Haskell's *>>=* in Python.

```python
def f(x: int) -> Option[int]:
  return (x + 1,) if x < 3 else ()

x: Option[int] = f(1)
y: Option[int] = bind(f, x)

print(*y) # 3
```

### *cache*

*cache* is a decorator which returns a function that always returns a value that was returned in the first call.

```python
def f(x: int) -> int:
  return x + 5

g = cache(f)
print(g(5)) # 10
print(g()) # 10
print(g("abc", 1, {})) # 10

h = cache(f)
print(h(7)) # 12
```

### *cachepartial*

*cachepartial* is simply:

```python
def cachepartial(f: AnyFunction, *args: object, **kwargs: object) -> AnyFunction:
  f = partial(f, *args, **kwargs)
  return cache(f)
```

Example of *cachepartial* usage:

```python
def f(x: int, y: int) -> int:
  return x + y

g = cachepartial(f, 5)
print(g(5)) # 10
```

### *call*

*call* is simply:

```python
def call(fx: Tuple[Callable[[Tuple[object, ...]], Y], Tuple[object, ...]]) -> Y:
  f, *x = fx
  return f(*x)
```

We assume, that *Tuple[object, ...]* are positional function arguments.

Example of *call* usage:

```python
def get_initials(name: str, surname: str) -> str:
  return name[:1] + surname[:1]

names = "Haskell Curry", "John Smith", "George Sand"

(
  Pipeline(explode(get_initials, names))
  / key(star)
  / value(lambda x: x.split(" "))
  / call
  & print
)

# HC
# JS
# GS
```

### *drop*

*drop* is simply:

```python
def drop(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return lambda xs: islice(xs, n, None)
```

Example of *drop* usage:

```python
xs = drop(1)(range(3))
print(tuple(xs)) # (1, 2)

xs = islice(range(3), 1, None)
print(tuple(xs)) # (1, 2)
```

### *explode*

*explode* is simply:

```python
def explode(x: X, ys: Iterable[Y]) -> Iterable[Tuple[X, Y]]:
  return zip(repeat(x), ys)
```

Example of *explode* usage:

```python
def multiply(scalar: int, vector: Iterable[int]) -> Iterable[int]:
  xs_and_ys: Iterable[Tuple[int, int]] = explode(scalar, vector)
  return starmap(operator.mul, xs_and_ys)

xs: Iterable[int] = multiply(2, (3, 4, 5))
print(tuple(xs)) # (6, 8, 10)
```

### *find*

*find* is a function which takes a predicate and some *Iterable* and returns an *Option* with value that matches the predicate if such value exists:

```python
x: Option[int] = find(lambda x: x == 3, range(5))
print(x) # (3,)

x: Option[int] = find(lambda x: x == -1, range(5))
print(x) # ()
```

### *find_and_collect*

*find_and_collect* is a function which takes a predicate, some *Iterator* and a buffer, and returns an *Option* and passed buffer.
The *Option* contains a value that matches the predicate if such value exists. The buffer contains values that were checked using the predicate:

```python
buffer = []
xs = iter(range(5))
x, filled_buffer = find_and_collect(lambda x: x == 3, xs, buffer)

print(x) # (3,)
print(filled_buffer) # [0, 1, 2, 3]

# notice: Iterator has to be passed, not Iterable

buffer = []
x, filled_buffer = find_and_collect(lambda x: x == 3, range(5), buffer)

print(x) # ()
print(filled_buffer) # []
```

### *findindex*

*findindex* is simply:

```python
def findindex(f: Callable[[X], bool], xs: Iterable[X]) -> Option[int]:
  yxs = enumerate(xs)

  g: Callable[[Tuple[int, X]], bool] = binary_compose(f, second)
  yx: Option[Tuple[int, X]] = find(g, yxs)

  return fmap(first, yx)
```

Example of *findindex* usage:

```python
x: Option[int] = findindex(lambda x: x == 8, range(5, 10))
print(x) # (3,)

x: Option[int] = findindex(lambda x: x == -1, range(5, 10))
print(x) # ()
```

### *first*

*first* is simply:

```python
def first(xy: Tuple[X, Y]) -> X:
  return xy[0]
```

### *flatten*

*flatten* is simply:

```python
def flatten(xyz: Tuple[Tuple[X, Y], Z]) -> Tuple[X, Y, Z]:
  (x, y), z = xyz
  return x, y, z
```

Example of *flatten* usage:

```python
xys = {"A": 2.5, "B": 3.14}
Pipeline(xys.items()) // zipr(count(1)) / flatten & print

# ('A', 2.5, 1)
# ('B', 3.14, 2)
```

### *flip*

*flip* is simply:

```python
def flip(f: Callable[[Y, X], Z]) -> Callable[[X, Y], Z]:
  return lambda x, y: f(y, x)
```

Example of *flip* usage:

```python
xs = "A", "B", "C"
Pipeline(enumerate(xs)) / key(lambda x: x + 1) * star(flip(repeat)) & print

# A
# B
# B
# C
# C
# C
```

### *fmap*

*fmap* resembles Haskell's *fmap* in Python. It is intended to be used with *Option*, because it transforms the result of Python's *map* function into *tuple*. *fmap* is defined as follows:

```python
def fmap(f: Callable[[X], Y], x: Iterable[X]) -> Tuple[Y, ...]:
  return binary_compose(tuple, lift(f))(x)
```

If you simply want to lift some function without composing the resulting function with a *tuple*, use a *lift* function.

```python
def f(x: int) -> Option[int]:
  return (x + 1,) if x < 3 else ()

x: Option[int] = f(1)
y: Option[int] = fmap(lambda x: x + 5, x)

print(*y) # 7
```

### *fold*

*fold* is simply:

```python
def fold(f: Callable[[Y, X], Y], acc: Y) -> Callable[[Iterable[X]], Y]:
  return lambda xs: reduce(f, xs, acc)
```

It is a convenience function which takes only swapped second and third arguments of Python's *reduce*
function. The first argument of *reduce* function has to be supplied to returned function.
It makes it easy to partially apply some function and accumulator.

Example of *fold* usage:

```python
xs = range(ord("A"), ord("Z") + 1)
alphabet = Pipeline(xs) / chr >> fold(operator.add, "")

print(alphabet)

# ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

### *iterfind*

*iterfind* is a function which takes an *Iterable* of predicates and some *Iterable* and returns an *Iterable* of *Option*. Each *Option*
contains a matched value of a corresponding predicate. *iterfind* uses *find_and_collect* under the hood.
*iterfind* firstly searches for matching value in a buffer, if it could not find one, it passes predicate along with buffer to *find_and_collect*.

```python
fs = (lambda x: x == 2), (lambda x: x == 4), (lambda x: x == 1), (lambda x: x == -1)
ys: Iterable[Option[int]] = iterfind(fs, range(5))

for y in ys:
  print(y)

# (2,)
# (4,)
# (1,)
# ()
```

### *key*

*key* is simply:

```python
def key(f: Callable[[X], Z]) -> Callable[[Tuple[X, Y]], Tuple[Z, Y]]:
  g: Callable[[Tuple[X, Y]], Z] = binary_compose(f, first)
  return lambda xy: (g(xy), second(xy))
```

Example of *key* usage:

```python
xys = {"A": [1, 2, 3], "B": [3, 4]}
zys = map(key(str.casefold), xys.items())

for zy in zys:
  print(zy)

# ('a', [1, 2, 3])
# ('b', [3, 4])
```

### *lift*

*lift* is simply:

```python
def lift(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Y]]:
  return partial(map, f)
```

### *mapexplode*

*mapexplode* is simply:

```python
def mapexplode(f: Callable[[X, Y], Z], x: X, ys: Iterable[Y]) -> Iterable[Z]:
  xs_and_ys: Iterable[Tuple[X, Y]] = explode(x, ys)
  return starmap(f, xs_and_ys)
```

Example of *mapexplode* usage:

```python
def multiply(scalar: int, vector: Iterable[int]) -> Iterable[int]:
  return mapexplode(operator.mul, scalar, vector)

xs: Iterable[int] = multiply(2, (3, 4, 5))
print(tuple(xs)) # (6, 8, 10)
```

### *maptry*

*maptry* is simply:

```python
def maptry(f: Callable[[X], Y], xs: Iterable[X]) -> Iterable[Y]:
  ys: Iterable[Option[Y]] = map(wraptry(f), xs)
  return chain.from_iterable(ys)
```

Example of *maptry* usage:

```python
possible_jsons = "{}", "", "123, 32323", "{\"a\": 1}"
jsons = maptry(json.loads, possible_jsons)

for x in jsons:
  print(x)

# {}
# {'a': 1}
```

### *second*

*second* is simply:

```python
def second(xy: Tuple[X, Y]) -> Y:
  return xy[1]
```

### *shift*

*shift* is a decorator which returns a partially applied function. The returned function takes only single argument. This argument is the first argument of the original function.

```python
take_3 = shift(islice, 3)
xs: Iterable[int] = take_3(range(5))

for x in xs:
  print(x)

# 0
# 1
# 2
```

### *slide*

*slide* is a function which takes an *Iterable*, **length** and **step** and returns *Iterable* of *tuple* after applying a sliding window. Each *tuple* has at most length equal to **length**. **step** is simply a shift of a sliding window.

```python
xs: Iterable[Tuple[int, ...]] = slide(range(10))
print(tuple(xs))
# ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9,))

xs: Iterable[Tuple[int, ...]] = slide(range(10), length=3, step=2)
print(tuple(xs))
# ((0, 1, 2), (2, 3, 4), (4, 5, 6), (6, 7, 8), (8, 9))
```

### *take*

*take* is simply:

```python
def take(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return lambda xs: islice(xs, n)
```

Example of *take* usage:

```python
xs = take(1)(range(3))
print(tuple(xs)) # (0,)

xs = islice(range(3), 1)
print(tuple(xs)) # (0,)
```

### *value*

*value* is simply:

```python
def value(f: Callable[[Y], Z]) -> Callable[[Tuple[X, Y]], Tuple[X, Z]]:
  g: Callable[[Tuple[X, Y]], Z] = binary_compose(f, second)
  return lambda xy: (first(xy), g(xy))
```

Example of *value* usage:

```python
xys = {"A": [1, 2, 3], "B": [3, 4]}
xzs = map(value(len), xys.items())

for xz in xzs:
  print(xz)

# ('A', 3)
# ('B', 2)
```

### *wrapeek*

*wrapeek* is a function which takes an *Iterable* and returns an *Option* containing a first value of the *Iterable* along with an original *Iterable* (containing first value).

```python
xs = (x for x in range(5))
x, ys = wrapeek(xs)

print(x) # (0,)

for y in ys:
  print(y)

# 0
# 1
# 2
# 3
# 4
```

### *wrapexcept*

*wrapexcept* is a decorator which returns a function that returns *Either* with some value or an *Exception* that was raised.

```python
f = wrapexcept(next)
xs = iter(range(2))

print(f(xs)) # ((0,), ())
print(f(xs)) # ((1,), ())
print(f(xs)) # ((), (StopIteration(),))
```

### *wrapnext*

*wrapnext* is simply:

```python
wrapnext: Callable[[Iterator[X]], Option[X]] = wraptry(next)
```

Example of *wrapnext* usage:

```python
xs = iter(range(2))

print(wrapnext(xs)) # (0,)
print(wrapnext(xs)) # (1,)
print(wrapnext(xs)) # ()
```

### *wraptry*

*wraptry* is a decorator which returns a function that returns *Option* with some value or an empty *Option* if an *Exception* was raised.

```python
load_json = wraptry(json.loads)

print(load_json("{}")) # ({},)
print(load_json("[1, 2, 3]")) # ([1, 2, 3],)
print(load_json("abc")) # ()
```

### *zipl*

*zipl* is simply:

```python
def zipl(xs: Iterable[X]) -> Callable[[Iterable[Y]], Iterable[Tuple[X, Y]]]:
  return lambda ys: zip(xs, ys)
```

Example of *zipl* usage:

```python
xs = "A", "B", "C"
Pipeline(xs) // zipl(count(1)) * star(flip(repeat)) & print

# A
# B
# B
# C
# C
# C
```

### *zipmapl*

*zipmapl* is simply:

```python
def zipmapl(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[Y, X]]]:
  return lambda xs: map(lambda x: (f(x), x), xs)
```

Example of *zipmapl* usage:

```python
xs = range(ord("a"), ord("z") + 1)
upper_to_lower = Pipeline(xs) / chr // zipmapl(str.upper) >> dict

Pipeline(upper_to_lower.items()) // take(5) & print

# ('A', 'a')
# ('B', 'b')
# ('C', 'c')
# ('D', 'd')
# ('E', 'e')
```

### *zipmapr*

*zipmapr* is simply:

```python
def zipmapr(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: map(lambda x: (x, f(x)), xs)
```

Example of *zipmapr* usage:

```python
xs = range(ord("a"), ord("z") + 1)
upper_to_lower = Pipeline(xs) / chr // zipmapr(str.upper) >> dict

Pipeline(upper_to_lower.items()) // take(5) & print

# ('a', 'A')
# ('b', 'B')
# ('c', 'C')
# ('d', 'D')
# ('e', 'E')
```

### *zipr*

*zipr* is simply:

```python
def zipr(ys: Iterable[Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: zip(xs, ys)
```

Example of *zipl* usage:

```python
xys = {"A": 2.5, "B": 3.14}
Pipeline(xys.items()) // zipr(count(1)) / flatten & print

# ('A', 2.5, 1)
# ('B', 3.14, 2)
```

## *nonion.loader*

### *FROM_STDIN*

*FROM_STDIN* is *None*. *FROM_STDIN* is defined for readability purposes. When you write CLI which can read users input from **stdin** by default, you can use this constant instead of using *None*.

### *as_loader*

*as_loader* is a decorator which takes a *BufferLoader* and creates a *Loader*. *BufferLoader* and *Loader* are defined as follows:

```python
BufferLoader = Callable[[IOBase, Tuple[object, ...], Dict[str, object]], X]
Loader = Callable[[Optional[str], Tuple[object, ...], Dict[str, object]], Option[X]]
```

For example, **json.load** and **pd.read_csv** are *BufferLoader*'s.

Created *Loader* will take a path as its first argument and will read the content using Python built-in *open*. If path is not provided, *Loader* reads content from **stdin**. If during read or during *BufferLoader* call exception raises, *Loader* will return an empty *Option*.

```python
# first_column_extractor.py
from typing import Callable, Optional

import pandas as pd

from nonion import Option
from nonion import as_loader
from nonion import bind
from nonion import fmap
from nonion import wraptry

load_frame = as_loader(pd.read_csv)
frame: Option[pd.DataFrame] = load_frame()

get_first_column = wraptry(lambda x: x.iloc[:, 0])
# x.iloc[:, 0] might raise an error, so use wraptry

series: Option[pd.Series] = bind(get_first_column, frame)

to_csv = lambda x: x.to_csv(header=False, index=False)
raw_series: Option[str] = fmap(to_csv, series)

if not series:
  print("something went wrong")
else:
  print(*raw_series, end="")
```

We can use script *first_column_extractor.py* in a following way in a Bash-like shells:

```bash
python first_column_extractor.py < frame.csv
```

### *load*

*load* is a function which takes an *Optional* path to a file and returns an *IOBase* buffer containing content of the file. If path does not exists *load* uses **stdin**.

```bash
with load() as buffer:
  print(buffer.read())
```

Notice: when *load* uses **stdin**, it firstly reads whole **stdin** content.

### *load_json*

*load_json* is simply:

```python
load_json: Loader[Union[Dict[str, object], Tuple[object, ...]]] = as_loader(json.load)
```

Example of *load_json* usage:

```python
x = load_json("object.json")
print(x) # ([1, 2, 3],)
```

### *wrapopen*

*wrapopen* is simply:

```python
wrapopen: Callable[[str], Option[IOBase]] = wraptry(open)
```

Example of *wrapopen* usage:

```python
x = wrapopen("missing_object.json")
print(x) # ()
```

## *Function*

In order to create a *Function*, you simply pass any *Callable*:

```python
f = Function(lambda x: x + 1)
f(5) # returns 6
```

You can also create an identity *Function*:

```python
g = Function()
```

Notice, that a *Function* takes exactly single value and returns exactly single value.

### compose

A ``Function composition" defined as $( f \circ g )(x) = f(g(x))$ could be done in the following way:

```python
z = f @ g

# alternatively

z = f.compose(g)
```

You can also use *compose* several times:

```python
z = f @ g @ f
```

Instead of wrapping each *Callable* with a *Function*, you can wrap only __first__ *Callable* and use *compose* on the rest.

```python
def f(x):
  return x + 1

g = Function() @ (lambda x: x * 2) @ f
g(5) # returns 12
```

The *@* (at) operator was used, because it reminds $\circ$ symbol.

### then

Function composition sometimes might be hard to read, because you have to read it from right-to-left.
In order to achieve better readability, you can use *then*.

```python
g = Function() / (lambda x: x * 2) / f
g(5) # returns 11

# alternatively

g = Function().then(lambda x: x * 2).then(f)
g(5) # returns 11
```

The */* (slash) operator was used, because it reminds *|* (vertical bar) used for piping.

### call

Sometimes you want to call a function ``inline'' after several compositions. In this case, you might use:

```python
(Function() / (lambda x: x * 2) / f)(5) # returns 11
```

But it might be hard to read. Especially, when you mostly pass lambdas. A better way to call a function is by using:

```python
Function() / (lambda x: x * 2) / f & 5 # returns 11
```

The *&* (ampersand) operator was used, because it looks similar to *$* (dollar), which is a Haskell operator.

### star (function)

Suppose, that you defined a function with multiple arguments such as:

```python
def f(x, y):
  return x + y * x
```

And you want to wrap that function using Function. In this case, you have to use *star*.

```python
Function() @ star(f) & (1, 2) # returns 5
```

*star* simply passes arguments to a function using Python *\** (star) operator.

### foreach

You can also call a function for each value in some *Iterable* in the following way:

```python
ys = Function() / (lambda x: x * 2) / (lambda x: x + 1) * range(5)

for y in ys:
  print(y)

# 1
# 3
# 5
# 7
# 9
#
```

The *\** (star) operator was used, because instead of passing an *Iterable* to a function, you pass its content as with Python *\** (star) operator and functions that take *\*args*.

## Pipeline

In order to create a *Pipeline*, you simply pass any *Iterable*:

```python
xs = Pipeline(range(5))

# notation abuse, do not use that:

xs = Function() / Pipeline & range(5)
```

You can also create an empty *Pipeline*:

```python
xs = Pipeline()
```

Under the hood *Pipeline* is simply uses *iter* on a passed *Iterable*. It means, that if you will pass an *Iterable*, that could be exhausted, you iterate over *Pipeline* only once.

```python
xs = Pipeline(range(2))

for x in xs:
  print(x)

# 1
# 2
#

# perfectly fine, because range(x) returns a special object
for x in xs:
  print(x)

# 1
# 2
#

xs = Pipeline(x for x in range(2))

for x in xs:
  print(x)

# 1
# 2
#

# xs already exhausted
for x in xs:
  print(x)
```

### map

*map* allows you to call a *Callable*, which takes a single value and returns a single value, on each value of the *Pipeline*.

```python
ys = Pipeline(range(3)) / (lambda x: x + 1) / (lambda x: (x, x + 1)) / star(lambda x, y: x + y * x)

for y in ys:
  print(y)

# 3
# 8
# 15
#

# alternatively

ys = Pipeline(range(3)).map(lambda x: x + 1).map(lambda x: (x, x + 1)).map(star(lambda x, y: x + y * x))
```

The */* (slash) operator was used, because it reminds *|* (vertical bar) used for piping.

### filter

*filter* allows you to filter *Pipeline* values.

```python
ys = Pipeline(range(3)) % (lambda x: x > 1)

for y in ys:
  print(y)

# 2
#

# alternatively

ys = Pipeline(range(3)).filter(lambda x: x > 1)
```

### flatmap

*flatmap* allows you to call a *Callable*, which takes a single value and returns an *Iterable*, on each value of the *Pipeline* and flatten results into single *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) * (lambda x: (x, x + 1))

for y in ys:
  print(y)

# 1
# 2
# 2
# 3
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).flatmap(lambda x: (x, x + 1))
```

The *\** (star) operator was used, because intuitively you use Python *\** (star) operator on each result.

### apply

*apply* allows you to call a *Callable*, which takes an *Iterable* and returns an *Iterable*, on whole *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) // tuple # internally Pipeline now has a tuple

for y in ys:
  print(y)

# 1
# 2
#

# now multiple itertations is possible
for y in ys:
  print(y)

# 1
# 2
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).apply(tuple)
```

### collect

*collect* allows you to call a *Callable*, which takes an *Iterable* and returns any single value, on whole *Pipeline*. The difference between *apply* and *collect* is that *collect* returns the result of a function instead of wrapping it with *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) >> tuple
print(ys)

# (1, 2)
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).collect(tuple)
```

You can also combine *collect* with any function which takes an *Iterator*:

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) >> wrapnext
print(ys) # (1,)

ys = Pipeline(range(2)) % (lambda x: x == 5) >> wrapnext
print(ys) # ()

ys = Pipeline(range(5)) >> shift(islice, 2)

for y in ys:
  print(y)

# 0
# 1

# alternatively you can use apply

ys = Pipeline(range(5)) // shift(islice, 2) & print

# 0
# 1
```

### foreach

*foreach* allows you to call a *Callable*, which takes a single value, on each value of the *Pipeline*.

```python
Pipeline(range(2)) / (lambda x: x + 1) & print

# 1
# 2
#

# alternatively

Pipeline(range(2)).map(lambda x: x + 1).foreach(print)
```

## groupon

*groupon* is a function which takes a function *Callable[[X], Y]*, some *Iterable[X]*, and returns *Iterable[X]* grouped on *Callable[[X], Y]* function. The *groupon* function uses Python *groupby* function under the hood. *groupon* adds a grouping key using passed *Callable[[X], Y]* function and sorts values by that key before applying *groupby*.

```python
for y, xs in groupon(lambda x: x > 0, (-3, 1, 0, -1, 5)):
  print(f"{y}: {tuple(xs)}")

# False: (-3, 0, -1)
# True: (1, 5)
```
