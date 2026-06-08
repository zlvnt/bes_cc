#!/usr/bin/env sh
set -e

# Tunggu Postgres siap, lalu pastikan user admin default ada, baru jalankan server.
python -c "import db; db.wait_for_db()"
python -c "import main; main.ensure_default_admin()"

exec gunicorn --bind 0.0.0.0:8000 --workers 2 main:app
