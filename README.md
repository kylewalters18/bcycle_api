## Start Postgres
> pg_ctl -D /usr/local/var/postgres -l logfile start

## Create bcycle database
> execute 'CREATE DATABASE bcycle;' in psql

## Initialize database
> python manage.py db init

## Run Migrations
> python manage.py db migrate
> python manage.py db upgrade