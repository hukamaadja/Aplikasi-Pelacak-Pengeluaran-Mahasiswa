"""services.py - Class 2: logika bisnis (tambah, hapus, sorting, searching, ringkasan)."""
from models import Transaksi
from validators import validasi_transaksi


def format_rupiah(angka):
    """15000 -> 'Rp 15.000'"""
    return "Rp " + f"{angka:,}".replace(",", ".")


class ExpenseService:
    def __init__(self, daftar=None):
        self.daftar = daftar if daftar is not None else []

    # ---------- CRUD ----------
    def _id_baru(self):
        return max((t.id for t in self.daftar), default=0) + 1

    def tambah(self, tanggal, kategori, deskripsi, jumlah):
        tanggal, kategori, deskripsi, jumlah = validasi_transaksi(
            tanggal, kategori, deskripsi, jumlah
        )
        transaksi = Transaksi(self._id_baru(), tanggal, kategori, deskripsi, jumlah)
        self.daftar.append(transaksi)
        return transaksi

    def hapus(self, id_transaksi):
        for t in self.daftar:
            if t.id == id_transaksi:
                self.daftar.remove(t)
                return
        raise ValueError(f"Transaksi dengan id {id_transaksi} tidak ditemukan")

    # ---------- SORTING (memakai lambda) ----------
    def urutkan(self, data=None, berdasarkan="tanggal", menurun=False):
        data = self.daftar if data is None else data
        kunci = {
            "tanggal": lambda t: t.tanggal,
            "kategori": lambda t: t.kategori.lower(),
            "jumlah": lambda t: t.jumlah,
        }
        assert berdasarkan in kunci, f"Kolom urut tidak dikenal: {berdasarkan}"
        return sorted(data, key=kunci[berdasarkan], reverse=menurun)

    # ---------- SEARCHING ----------
    def cari(self, kata_kunci, data=None):
        """Pencarian linear: cek satu per satu apakah kata kunci ada di
        deskripsi atau kategori (tidak peduli huruf besar/kecil)."""
        data = self.daftar if data is None else data
        kata_kunci = kata_kunci.strip().lower()
        if not kata_kunci:
            return list(data)
        hasil = []
        for t in data:
            if kata_kunci in t.deskripsi.lower() or kata_kunci in t.kategori.lower():
                hasil.append(t)
        return hasil

    # ---------- **kwargs: filter fleksibel ----------
    def saring(self, **kriteria):
        """Contoh: saring(kategori="Makan", min_jumlah=10000, bulan="2026-11").
        Kriteria yang tidak diberikan diabaikan."""
        hasil = list(self.daftar)
        if "kategori" in kriteria:
            hasil = [t for t in hasil if t.kategori == kriteria["kategori"]]
        if "min_jumlah" in kriteria:
            hasil = [t for t in hasil if t.jumlah >= kriteria["min_jumlah"]]
        if "maks_jumlah" in kriteria:
            hasil = [t for t in hasil if t.jumlah <= kriteria["maks_jumlah"]]
        if "bulan" in kriteria:
            hasil = [t for t in hasil if t.tanggal.startswith(kriteria["bulan"])]
        return hasil

    # ---------- *args: jumlah kategori bebas ----------
    def hitung_total(self, *kategori):
        """hitung_total() = semua; hitung_total("Makan") atau
        hitung_total("Makan", "Kos") = hanya kategori yang disebut."""
        return sum(t.jumlah for t in self.daftar if not kategori or t.kategori in kategori)

    # ---------- Ringkasan untuk analisis ----------
    def ringkasan_per_kategori(self, data=None):
        data = self.daftar if data is None else data
        total = {}
        for t in data:
            total[t.kategori] = total.get(t.kategori, 0) + t.jumlah
        return total
