#!/usr/bin/env bash

set -x

create_user() {
  if [[ -n ${POSTGRES_USER} ]]; then
    if [[ -z ${POSTGRES_PASSWORD} ]]; then
      echo "ERROR! Please specify a password for POSTGRES_USER in POSTGRES_PASSWORD. Exiting..."
      exit 1
    fi

    echo "Creating project database user: $POSTGRES_APP_USER"

    if [[ -z $(psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -Atc "SELECT 1 FROM pg_catalog.pg_user WHERE usename = '$POSTGRES_APP_USER'";) ]]; then
      psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "CREATE ROLE \"$POSTGRES_APP_USER\" with LOGIN CREATEDB NOSUPERUSER NOCREATEROLE PASSWORD '$POSTGRES_APP_PASSWORD';" >/dev/null
    fi
  fi
}

create_user
