# Validata API

[![PyPI](https://img.shields.io/pypi/v/validata-api.svg)](https://pypi.python.org/pypi/validata-api)

Web API for Validata

## Usage

You can use the online instance of Validata:

- user interface: https://go.validata.fr/
- API: https://go.validata.fr/api/v1/
- API docs: https://go.validata.fr/api/v1/apidocs

Several software services compose the Validata stack. The recommended way to run it on your computer is to use Docker. Otherwise you can install each component of this stack manually, for example if you want to contribute by developing a new feature or fixing a bug.

## Run with Docker

Read instructions at https://git.opendatafrance.net/validata/validata-docker

## Develop

### Install

We recommend using `venv` python standard package:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

### Configure

```bash
cp .env.example .env
```

Customize the configuration variables in `.env` file.

Do not commit `.env`.

See also: https://github.com/theskumar/python-dotenv

### Serve

Start the web server...

```bash
./serve.sh
```

... then open http://localhost:5600/
