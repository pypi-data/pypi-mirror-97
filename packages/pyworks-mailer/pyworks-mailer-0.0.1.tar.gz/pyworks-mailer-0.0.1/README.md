# Pyworks Mailer

PyWork Mailer provide fast way to use SMTP mail and the most email templates.

## Features

- Setup SMTP mail easily.
- Most popular mail templates for Register, Forgot password, Daily, Weekly news, Payment, Place Order..etc.
- Compress mail before send.

... and more

## TODO

- [x] Auto load configuration form .env file.
- [x] Auto load all templates file.
- [x] Minify mail template HTML.
- [x] Support Gmail mail.
- [ ] Support Amazon SES mail.
- [ ] Support Yandex mail.


## Requies

- Python 3.7+
- Virtualenv
- Pytest

## Development

### Create virtual environment

```shell
virtualenv -p python3.7 venv
source venv/bin/activate
```

Install Python dependencies:

```shell
pip install pytest
pip install wheel
```

### Test package locally

To run tests for project run this command:


```shell
# Use Makefile
make test

# Use pytest package in virtualenv
python -m pytest

# or
# pytest --pyargs <your_package_name>
pytest --pyargs mailer
```

Results

```
====================== test session starts ==============================
platform linux -- Python 3.7.9, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: *********/pyworks-mailer, configfile: pytest.ini
collected 2 items          

tests/test_config.py .                                              [ 50%]
tests/test_send_mail.py .                                           [100%]

======================= 2 passed in 3.18s ================================
```

## Packaging project

**Create Source Distributions**

Create a source distribution for publish to PyPI:

```shell
python setup.py sdist
```

**Create Wheels**

Create a wheel for project.

```shell
python3 -m pip install wheel
```
