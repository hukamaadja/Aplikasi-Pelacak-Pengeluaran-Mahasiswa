"""models.py - Class 1: model objek Transaksi.

Satu objek Transaksi = satu baris pengeluaran (satu "catatan belanja").
"""


class Transaksi:
    def __init__(self, id_transaksi, tanggal, kategori, deskripsi, jumlah):
        self.id = id_transaksi        # nomor unik, mis. 1, 2, 3
        self.tanggal = tanggal        # teks "YYYY-MM-DD"
        self.kategori = kategori      # mis. "Makan"
        self.deskripsi = deskripsi    # mis. "Nasi goreng"
        self.jumlah = jumlah          # bilangan bulat (rupiah)

    def ke_baris(self):
        """Ubah objek menjadi list, siap ditulis ke baris CSV."""
        return [self.id, self.tanggal, self.kategori, self.deskripsi, self.jumlah]

    @classmethod
    def dari_baris(cls, baris):
        """Kebalikan ke_baris(): bangun objek dari satu baris CSV."""
        return cls(int(baris[0]), baris[1], baris[2], baris[3], int(baris[4]))

    def __str__(self):
        return f"[{self.id}] {self.tanggal} | {self.kategori} | {self.deskripsi} | Rp {self.jumlah:,}".replace(",", ".")
