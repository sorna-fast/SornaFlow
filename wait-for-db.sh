#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for MySQL at $host ..."

until mysqladmin ping -h "$host" --silent; do
  echo "MySQL is unavailable - sleeping"
  sleep 2
done

echo "MySQL is up - executing command"
exec $cmd
