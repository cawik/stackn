#!/bin/sh
sleep 5
cd modules
echo "installing modules..."
for d in */ ; do
    echo "installing $d"
    python3 -m pip install -e $d
done
cd ..
echo "deleting all existing migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
echo "done!"
echo "Installing all migrations"
python3 manage.py makemigrations
python3 manage.py makemigrations ingress datasets deployments experiments files labs models projects reports workflows
python3 manage.py migrate
python3 manage.py makemigrations ingress datasets deployments experiments files labs models projects reports workflows
python3 manage.py migrate
echo "loading seed data..."
python3 manage.py loaddata projects/fixtures/fixtures.json
python3 manage.py loaddata projects/fixtures/data.json
echo "starting serving..."
python3 manage.py runserver 0.0.0.0:8080