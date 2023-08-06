# json_repository
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal&style=flat-square)](https://www.paypal.me/mandrewcito/1)&nbsp;
![travis build](https://img.shields.io/travis/mandrewcito/json_repository.svg)
![Pypi](https://img.shields.io/pypi/v/json-repository.svg)
[![Downloads](https://pepy.tech/badge/json-repository)](https://pepy.tech/project/json-repository)
[![Downloads](https://pepy.tech/badge/json-repository/month)](https://pepy.tech/project/json-repository/month)
![codecov.io](https://codecov.io/github/mandrewcito/json_repository/coverage.svg?branch=master)

# Install

[https://pypi.org/project/json-repository/](Pypi)
pip install json-repository

# Examples

You can also go to [tests](test/sample/foobar_test.py) to check a good how-to!

## Creating custom repository

```python
class Foo(object):
    foo = None
    bar = None
    id = None

class FoobarRepository(BaseJsonRepository):
  def __init__(self):
    super(FoobarRepository, self).__init__(Foo)
```

## using created repository

```python
  with FoobarRepository() as repo:
    for entity in repo.get_all():
      repo.delete(entity)
    repo.context.commit()
```
