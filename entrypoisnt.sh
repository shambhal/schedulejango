#!/bin/sh

# Run migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "Running preset SQL..."
mysql $DATABASE_URL -f /app/appoint.sql
# Create superuser automatically (if not exists)
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SU_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SU_USERNAME', '$DJANGO_SU_EMAIL', '$DJANGO_SU_PASSWORD')
" | python manage.py shell

# Start server
gunicorn your_project.wsgi:application --bind 0.0.0.0:8000