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
python -m unittest discover 
```
