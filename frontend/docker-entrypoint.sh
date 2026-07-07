#!/bin/sh
set -e

cd /app

if [ ! -d node_modules ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
  echo "==> node_modules missing — running npm ci..."
  npm ci --no-audit
fi

exec "$@"
