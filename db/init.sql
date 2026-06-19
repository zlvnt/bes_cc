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

-- Seed data anggota kelompok.
INSERT INTO anggota (nama, nim, prodi, foto, email) VALUES
    ('Zelvin Apri Thady',        '102022330294', '', 'zelvin.jpg',   NULL),
    ('Dendi Prawira',            '102022330454', '', 'dendi.jpeg',   NULL),
    ('Fauzi Achmad Koesnaedi',   '102022300352', '', 'fauzi.jpeg',   NULL),
    ('Faadhil Al Ghifari',       '102022300425', '', 'faadhil.png',  NULL)
ON CONFLICT DO NOTHING;

-- User login dibuat otomatis oleh app saat startup (admin / admin123)
-- supaya hash password portable. Lihat ensure_default_admin() di main.py.
