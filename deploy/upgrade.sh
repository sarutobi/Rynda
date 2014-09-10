#!/bin/bash

cur_dir=`pwd`
cd ..
# Fetch latest from repo
echo "Upgrading code..."
git pull

#Activating virtualenv
source $VENV
echo "Upgrading dependencies..."
pip install -r requirements/stage.txt

# Generating static assets (css, javascripts)
echo "Generating some assets..."
grunt less:development
cd rynda # ROOT DIR
echo "Cleaning files..."
find . -name "*.pyc" -delete
export vk_app_id='' # Fake vk_app_id
echo "Migrating database..."
python manage.py migrate --settings=Rynda.settings.stage
echo "Collect all statics..."
python manage.py collectstatic --noinput -c --settings=Rynda.settings.stage
