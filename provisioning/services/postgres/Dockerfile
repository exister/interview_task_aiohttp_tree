FROM postgres:9.6

COPY docker-healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-healthcheck.sh
HEALTHCHECK CMD ["docker-healthcheck.sh"]

COPY 01_create_db.sh /docker-entrypoint-initdb.d/01_create_db.sh
