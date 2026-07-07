#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Installing backend dependencies..."
PYTHON=${PYTHON:-python3.12}
if ! command -v "$PYTHON" &>/dev/null; then
  PYTHON=python3
  echo "Warning: python3.12 not found, using $PYTHON. Docker is recommended for backend."
fi
"$PYTHON" -m venv backend/.venv
source backend/.venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> Installing frontend dependencies..."
cd frontend
npm install
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env from .env.example"
fi

echo "==> Install complete. Run ./scripts/dev.sh to start development."
