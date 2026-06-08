# Tubes — Web App Anggota Kelompok

Flask + PostgreSQL, server-rendered (Jinja2). Punya halaman login, menu utama,
dan daftar anggota dari DB. Tiap halaman menampilkan **INSTANCE_ID** di footer
(buat membuktikan request dilayani instance yang mana).

## Struktur
```
app/
  main.py            # routing: /login, /, /anggota, /healthz
  db.py              # koneksi postgres
  templates/         # base, login, menu, anggota
  static/foto/       # foto anggota (+ placeholder.png)
db/
  init.sql           # schema + seed data anggota
Dockerfile
docker-compose.yml   # app + postgres (lokal)
.env                 # INSTANCE_ID, DB credentials
```

## Jalankan lokal (Docker)
```bash
docker compose up --build
```
Buka http://localhost:8000 — login default: **admin / admin123**

## Yang perlu kamu siapkan manual
1. **Foto anggota**: taruh di `app/static/foto/`, resize seragam (mis. 400×400).
2. **Data anggota**: edit seed di `db/init.sql` (nama, NIM, prodi, email, nama file foto).
   - Kolom `foto` = nama file di `app/static/foto/`. Kalau file tidak ada,
     otomatis fallback ke `placeholder.png`.

> Catatan: kalau mengubah `init.sql` setelah DB sudah pernah dibuat, jalankan
> `docker compose down -v` dulu (hapus volume) supaya seed di-load ulang.

## Deploy ke AWS (2 instance, 1 DB bersama)
Set env per instance: `INSTANCE_ID=1` dan `INSTANCE_ID=2`, arahkan `DB_HOST`
ke Postgres bersama. Footer akan menunjukkan instance mana yang melayani.
