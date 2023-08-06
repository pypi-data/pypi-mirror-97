
FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # nginx and supervisor
  && apt-get install -y nginx supervisor \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system --gid 1001 django \
    && adduser --system --uid 1001 --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt
RUN pip install --no-cache-dir -r /requirements/extra.txt \
    && find /requirements -name '*.tar.gz' -exec pip install {} \; \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# maintenance
RUN mkdir /backups
COPY ./compose/production/django/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

# nginx
ADD ./compose/production/nginx/nginx.conf /etc/nginx/sites-enabled/default
# nginx log
# https://medium.com/@ecaradec/redirecting-nginx-output-on-docker-compose-up-when-embedded-in-supervisor-cbc461723326
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# supervisor
COPY ./compose/production/supervisor/start-supervisor /start-supervisor
RUN sed -i 's/\r$//g' /start-supervisor
RUN chmod +x /start-supervisor
ADD ./compose/production/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf


COPY --chown=django:django ./src/ /app/

# USER django  # supervisor

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
