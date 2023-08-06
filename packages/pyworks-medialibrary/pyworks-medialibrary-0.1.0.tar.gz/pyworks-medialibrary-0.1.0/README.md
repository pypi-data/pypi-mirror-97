# PyWorks Medialibrary

Pyworks Medialibrary provide awsome tools for manage image and document files.

## Pre-Requisites

- Python 3+
- Poetry 1.1.4+

Setup environment

```shell
poetry init
```

## Test package locally

To run tests for project run this command:

```
make test
make test-cov
```

Results

====================== test session starts ==============================
platform linux -- Python 3.7.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: *********/pyworks-medialibrary, configfile: pytest.ini
collected 10 items          

tests/test_config.py .                                              [ 50%]
tests/test_send_mail.py .                                           [100%]

======================= 2 passed in 3.18s ================================