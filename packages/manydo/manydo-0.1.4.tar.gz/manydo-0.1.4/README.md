# manydo

Dead-simple parallel execution with a loading bar sprinkled on top.

## Installation

`pip install manydo`. Or, better for you, use [Poetry](python-poetry.org/): `poetry add manydo`.

## Usage

`manydo` is simple. All you need is `map`:

```python
from manydo import map

map(lambda x: x + 3, [1, 2, 3]) # [4, 5, 6]
map(function, iterable, num_jobs=16) # try not to burn your CPU
map(function, iterable, loading_bar=False)
map(function, iterable, desc='Passes arguments to tqdm')
```

## Related projects

[pqdm](https://github.com/niedakh/pqdm) is very similar, but didn't work for me ¯\\\_(ツ)\_/¯
