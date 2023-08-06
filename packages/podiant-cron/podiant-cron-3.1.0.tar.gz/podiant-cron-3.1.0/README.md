Podiant cron
============

![Build](https://git.steadman.io/podiant/cron/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/cron/badges/master/coverage.svg)

A tiny wrapper around APScheduler and Django RQ, for defining cron jobs

## Quickstart

Install cron:

```sh
pip install podiant-cron
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'cron',
    ...
)
```

## Running tests

Does the code actually work?

```
coverage run --source cron runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
