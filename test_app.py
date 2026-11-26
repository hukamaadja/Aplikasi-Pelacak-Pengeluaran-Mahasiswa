"""test_app.py - unit test. Jalankan:  python -m unittest test_app -v"""
import os
import tempfile
import unittest

from service import ExpenseService, format_rupiah
from storage import muat_transaksi, simpan_transaksi
from validators import validasi_jumlah, validasi_tanggal


class TestValidator(unittest.TestCase):
    def test_jumlah_valid_dengan_titik(self):
        self.assertEqual(validasi_jumlah("15.000"), 15000)

    def test_jumlah_negatif_ditolak(self):
        with self.assertRaises(ValueError):
            validasi_jumlah("-500")

    def test_tanggal_format_salah_ditolak(self):
        with self.assertRaises(ValueError):
            validasi_tanggal("18-11-2026")


class TestService(unittest.TestCase):
    def setUp(self):
        self.s = ExpenseService()
        self.s.tambah("2026-11-01", "Makan", "Nasi goreng", "15000")
        self.s.tambah("2026-11-02", "Transport", "Ojek online", "22000")
        self.s.tambah("2026-11-03", "Makan", "Ayam geprek", "18000")

    def test_tambah_memberi_id_berurutan(self):
        self.assertEqual([t.id for t in self.s.daftar], [1, 2, 3])

    def test_urutkan_jumlah_menurun(self):
        hasil = self.s.urutkan(berdasarkan="jumlah", menurun=True)
        self.assertEqual([t.jumlah for t in hasil], [22000, 18000, 15000])

    def test_cari_kata_kunci(self):
        hasil = self.s.cari("ayam")
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0].deskripsi, "Ayam geprek")

    def test_hitung_total_dengan_args(self):
        self.assertEqual(self.s.hitung_total(), 55000)
        self.assertEqual(self.s.hitung_total("Makan"), 33000)

    def test_saring_dengan_kwargs(self):
        hasil = self.s.saring(kategori="Makan", min_jumlah=16000)
        self.assertEqual(len(hasil), 1)

    def test_hapus_id_tidak_ada(self):
        with self.assertRaises(ValueError):
            self.s.hapus(99)

    def test_format_rupiah(self):
        self.assertEqual(format_rupiah(1500000), "Rp 1.500.000")


class TestStorage(unittest.TestCase):
    def test_simpan_lalu_muat(self):
        s = ExpenseService()
        s.tambah("2026-11-05", "Kuliah", "Fotokopi modul", "5000")
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "data", "uji.csv")
            simpan_transaksi(path, s.daftar)
            hasil = muat_transaksi(path)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0].deskripsi, "Fotokopi modul")
        self.assertEqual(hasil[0].jumlah, 5000)

    def test_muat_file_tidak_ada_kembali_kosong(self):
        self.assertEqual(muat_transaksi("/tidak/ada/file.csv"), [])


if __name__ == "__main__":
    unittest.main()