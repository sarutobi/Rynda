#!/bin/sh
spatialite rynda.db "select InitSpatialMetaData();"
python manage.py migrate
python manage.py loaddata rynda/core/fixtures/initial_data.json
python manage.py createsuperuser --username=admin --email=admin@rynda.org
