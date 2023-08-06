# Time to submit while mobile working ヽ(´▽`)/
[![Python application](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml/badge.svg)](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml)
## Setup (currently)

```bash
python3 -m pip install poetry
poetry install
poetry shell
poetry run python timrr/timrr.py calc
```

## Short Docu

### calculate work time

```bash
Usage: timr.py calc [OPTIONS]

Options:
  -s, --start-time TEXT
  -e, --end-time TEXT
  -b, --break-time TEXT
  -ch, --contract-hours-per-day TEXT
  --local-config / --no-local-config
  --help
```

### configure defaults

```bash
Usage: timrr.py configure [OPTIONS]

Options:
  --start-time TEXT              [required]
  --end-time TEXT                [required]
  --break-time TEXT              [required]
  --contract-hours-per-day TEXT  [required]
  --help                         Show this message and exit.
```
