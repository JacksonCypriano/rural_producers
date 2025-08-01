#!/usr/bin/env bash
# Arquivo convertido para LF
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1; do
  echo "Aguardando banco de dados em $host..."
  sleep 2
done

exec $cmd
