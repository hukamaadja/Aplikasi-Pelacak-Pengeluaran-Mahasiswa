"""storage.py - baca/tulis file CSV memakai with open() dan try/except."""
import csv
import os

from models import Transaksi

HEADER = ["id", "tanggal", "kategori", "deskripsi", "jumlah"]


def muat_transaksi(path):
    """Baca CSV -> list objek Transaksi. File belum ada = daftar kosong."""
    if not os.path.exists(path):
        return []
    hasil = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            pembaca = csv.reader(f)
            next(pembaca, None)  # lewati baris header
            for baris in pembaca:
                if baris:  # abaikan baris kosong
                    hasil.append(Transaksi.dari_baris(baris))
    except (OSError, ValueError, IndexError) as e:
        raise RuntimeError(f"Gagal membaca file data: {e}") from e
    return hasil


def simpan_transaksi(path, daftar):
    """Tulis seluruh list Transaksi ke CSV (menimpa isi lama)."""
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            penulis = csv.writer(f)
            penulis.writerow(HEADER)
            for t in daftar:
                penulis.writerow(t.ke_baris())
    except OSError as e:
        raise RuntimeError(f"Gagal menyimpan file data: {e}") from e
