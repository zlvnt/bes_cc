"""Web app Flask + Postgres, server-rendered (Jinja2).

Halaman:
  /login    -> form login
  /         -> menu utama (butuh login)
  /anggota  -> daftar anggota dari DB (butuh login)

Indikator instance: env var INSTANCE_ID di-inject ke footer tiap halaman,
jadi kelihatan instance mana yang nge-serve request.
"""
import functools
import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ganti-secret-ini-di-produksi")

INSTANCE_ID = os.environ.get("INSTANCE_ID", "local")


@app.context_processor
def inject_instance():
    """Sediakan instance_id ke semua template (dipakai di footer)."""
    return {"instance_id": INSTANCE_ID}


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def ensure_default_admin():
    """Buat user admin default kalau belum ada. Default: admin / admin123.

    Idempotent & aman dari race condition: 2 instance app bisa jalan
    entrypoint barengan terhadap 1 DB yang sama, jadi pakai
    INSERT ... ON CONFLICT DO NOTHING (mengandalkan UNIQUE pada users.username)
    biar tidak duplikat / tidak error saat startup bersamaan.

    Hashing password ada di sisi app (bukan di init.sql) supaya hash portable.
    """
    db.execute(
        """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
        ON CONFLICT (username) DO NOTHING
        """,
        ("admin", generate_password_hash("admin123")),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = db.query(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,),
            one=True,
        )
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("menu"))
        error = "Username atau password salah."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def menu():
    return render_template("menu.html", username=session.get("username"))


@app.route("/anggota")
@login_required
def anggota():
    rows = db.query(
        """
        SELECT id, nama, nim, prodi, foto, email
        FROM anggota
        ORDER BY id
        """
    )
    return render_template("anggota.html", anggota=rows)


@app.route("/healthz")
def healthz():
    """Health check ringan buat load balancer / docker."""
    return {"status": "ok", "instance": INSTANCE_ID}


if __name__ == "__main__":
    db.wait_for_db()
    ensure_default_admin()
    app.run(host="0.0.0.0", port=8000)
