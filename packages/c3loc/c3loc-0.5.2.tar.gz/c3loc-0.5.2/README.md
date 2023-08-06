# C3 Location Engine

## Prerequisites

- Python 3.7+
- Postgresql
- [Optional] Docker for Postgresql Test Setup
## Postgresql Testing Setup
``` sh
docker run -it -p5432:5432 -ePOSTGRES_USER=c3loc -ePOSTGRES_PASSWORD=c3letmein -d postgres
```

## Installation
``` sh
git clone https://gitlab.com/c3wireless/c3loc.git
cd c3loc
python -m venv venv
. venv/bin/activate
pip install wheel
pip install -e .
cp src/c3loc/alembic.ini.local ./alembic.ini
alembic upgrade head # Migrate the database
c3loc_ingest -p 9999
```
