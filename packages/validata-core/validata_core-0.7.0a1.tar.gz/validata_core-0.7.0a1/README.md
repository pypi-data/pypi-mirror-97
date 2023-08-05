# Validata validation core

[![PyPI](https://img.shields.io/pypi/v/validata-core.svg)](https://pypi.python.org/pypi/validata-core)

Validata validation library built over [frictionless-py](https://github.com/frictionlessdata/frictionless-py) `3.*` provides tabular data validation with:

- french error messages
- custom checks to handle french specifics (SIREN, SIRET, ...)

See [ERRORS.md](ERRORS.md) for more information

Validata core is used by [validata-ui](https://git.opendatafrance.net/validata/validata-ui/) and [validata-api](https://git.opendatafrance.net/validata/validata-api/) projects.

## Try

Create a virtualenv, run the script against fixtures:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
validata --schema /path/to/schema.json table.csv
```

A complete list of error messages can found in [ERRORS.md](ERRORS.md)

## Testing

```bash
pip install pytest
pytest --doctest-modules
```
