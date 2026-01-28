FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR C:/djangoapps/appoint

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

#RUN python manage.py collectstatic --noinput
COPY cron/expire_orders.cron /etc/cron.d/expire_orders
RUN chmod 0644 /etc/cron.d/expire_orders \
    && crontab /etc/cron.d/expire_orders

# Create log file
RUN touch /var/log/cron.log

CMD ["sh", "-c", "cron && gunicorn appoint.wsgi:application --bind 0.0.0.0:8000"]

