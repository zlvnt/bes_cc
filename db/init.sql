-- Schema + seed data.
-- Dijalankan otomatis oleh image postgres saat container pertama kali dibuat
-- (file di /docker-entrypoint-initdb.d/).

CREATE TABLE IF NOT EXISTS anggota (
    id      SERIAL PRIMARY KEY,
    nama    VARCHAR(120) NOT NULL,
    nim     VARCHAR(30)  NOT NULL,
    prodi   VARCHAR(120) NOT NULL,
    foto    VARCHAR(255),          -- nama file di app/static/foto/
    email   VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(60) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Seed data anggota (GANTI dengan data asli kelompokmu).
-- Kolom foto = nama file yang kamu taruh di app/static/foto/
INSERT INTO anggota (nama, nim, prodi, foto, email) VALUES
    ('Anggota Satu', '1010101010', 'Teknik Informatika', 'anggota1.jpg', 'satu@example.com'),
    ('Anggota Dua',  '2020202020', 'Sistem Informasi',   'anggota2.jpg', 'dua@example.com'),
    ('Anggota Tiga', '3030303030', 'Teknik Komputer',    'anggota3.jpg', 'tiga@example.com')
ON CONFLICT DO NOTHING;

-- User login dibuat otomatis oleh app saat startup (admin / admin123)
-- supaya hash password portable. Lihat ensure_default_admin() di main.py.
