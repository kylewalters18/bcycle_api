[![Build Status](https://travis-ci.org/kylewalters18/bcycle_api.svg?branch=master)](https://travis-ci.org/kylewalters18/bcycle_api)
[![Coverage Status](https://coveralls.io/repos/github/kylewalters18/bcycle_api/badge.svg?branch=master)](https://coveralls.io/github/kylewalters18/bcycle_api?branch=master)

# Denver Bcycle API
This is a REST API that exposes the publicaly available Denver Bcycle rider trip data.
Below are instructions on how to set up your development environment.


## Running locally

Install B-Cycle requirements
```bash
pip install -r requirements.txt
```

Start Postgres and create bcycle database
```bash
pg_ctl -D /usr/local/var/postgres -l logfile start
execute 'CREATE DATABASE bcycle;' in psql
```

Run migrations
```bash
python manage.py db migrate
python manage.py db upgrade
```

Run tests
```bash
coverage run --source bcycle -m unittest discover -s tests -v
coverage report
```
