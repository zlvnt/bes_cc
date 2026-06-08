"""Koneksi PostgreSQL sederhana pakai psycopg2.

Kredensial dibaca dari environment (lihat .env / docker-compose.yml).
"""
import os
import time

import psycopg2
import psycopg2.extras


def _config():
    return dict(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "tubes"),
        user=os.environ.get("DB_USER", "tubes"),
        password=os.environ.get("DB_PASSWORD", "tubes"),
    )


def get_connection():
    """Buka koneksi baru ke Postgres."""
    conn = psycopg2.connect(**_config())
    conn.autocommit = True
    return conn


def query(sql, params=None, *, one=False):
    """Jalankan SELECT, kembalikan list[dict] (atau dict tunggal kalau one=True)."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall()
    finally:
        conn.close()
    if one:
        return rows[0] if rows else None
    return rows


def execute(sql, params=None):
    """Jalankan INSERT/UPDATE/DELETE."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
    finally:
        conn.close()


def wait_for_db(retries=30, delay=1.0):
    """Tunggu Postgres siap (berguna saat container app start sebelum DB ready)."""
    last_err = None
    for _ in range(retries):
        try:
            conn = get_connection()
            conn.close()
            return
        except psycopg2.OperationalError as err:  # DB belum siap
            last_err = err
            time.sleep(delay)
    raise RuntimeError(f"Database tidak siap setelah {retries} percobaan: {last_err}")
