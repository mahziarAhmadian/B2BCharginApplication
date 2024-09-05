#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
#python manage.py migrate
echo "Migrate the Database at startup of project"

# Wait for few minute and run db migraiton
while ! python manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 3
done
#echo "Applying users..."
#python manage.py insert_user
#python manage.py insert_seller
#python manage.py insert_superuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn core.wsgi --bind 0.0.0.0:8000
