# Validata UI

[![PyPI](https://img.shields.io/pypi/v/validata-ui.svg)](https://pypi.python.org/pypi/validata-ui)

Validata user interface

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

We recommend using `venv` standard package:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

PDF report generation uses:

- either [Headless Chromium](https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md) (default)

```bash
apt install -y chromium
```

- or [browserless.io](https://www.browserless.io/) pdf service
  (see [.env.example](.env.example) to configure this option)

### Configure

```bash
cp .env.example .env
```

Customize the configuration variables in `.env` file.

Do not commit `.env`.

### Serve

Start the web server...

```bash
./serve.sh
```

... then open http://localhost:5601/

## Test

UI tests can be launched using [Cypress tool](https://www.cypress.io/)
