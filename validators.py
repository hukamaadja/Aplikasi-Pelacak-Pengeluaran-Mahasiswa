"""validators.py - memeriksa input pengguna dengan raise ValueError.

Aturannya: kalau input salah, lempar ValueError berisi pesan yang jelas.
Pesan itu nanti ditangkap (try/except) oleh UI dan ditampilkan ke pengguna.
"""
from datetime import datetime

KATEGORI_VALID = ["Makan", "Transport", "Kuliah", "Hiburan", "Kos", "Lainnya"]


def validasi_tanggal(teks):
    teks = str(teks).strip()
    try:
        datetime.strptime(teks, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Tanggal harus berformat YYYY-MM-DD, contoh: 2026-11-18")
    return teks


def validasi_kategori(teks):
    teks = str(teks).strip()
    if teks not in KATEGORI_VALID:
        raise ValueError("Kategori harus salah satu dari: " + ", ".join(KATEGORI_VALID))
    return teks


def validasi_deskripsi(teks):
    teks = str(teks).strip()
    if not teks:
        raise ValueError("Deskripsi tidak boleh kosong")
    if len(teks) > 50:
        raise ValueError("Deskripsi maksimal 50 karakter")
    if "," in teks:
        teks = teks.replace(",", " ")  # koma dibuang agar CSV tidak rusak
    return teks


def validasi_jumlah(teks):
    teks = str(teks).strip().replace(".", "")  # "15.000" -> "15000"
    if not teks.isdigit():
        raise ValueError("Jumlah harus berupa angka bulat positif, contoh: 15000")
    jumlah = int(teks)
    if jumlah <= 0:
        raise ValueError("Jumlah harus lebih dari 0")
    return jumlah


def validasi_transaksi(tanggal, kategori, deskripsi, jumlah):
    """Jalankan semua validasi sekaligus, kembalikan data yang sudah bersih."""
    return (
        validasi_tanggal(tanggal),
        validasi_kategori(kategori),
        validasi_deskripsi(deskripsi),
        validasi_jumlah(jumlah),
    )
