"""ui.py - Class 3: antarmuka GUI (Tkinter + Treeview).

UI hanya mengurus tampilan & tombol. Semua logika dipanggil dari
ExpenseService, dan penyimpanan dari storage.
"""
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from service import format_rupiah
from storage import simpan_transaksi
from validators import KATEGORI_VALID


class ExpenseApp:
    def __init__(self, root, service, path_csv):
        self.root = root
        self.service = service
        self.path_csv = path_csv

        self.root.title("Pelacak Pengeluaran Mahasiswa")
        self.root.geometry("860x580")

        self._buat_form()
        self._buat_kontrol()
        self._buat_tabel()
        self._buat_ringkasan()
        self.refresh_tabel()

    # ---------- Bagian tampilan ----------
    def _buat_form(self):
        bingkai = ttk.LabelFrame(self.root, text="Tambah Pengeluaran")
        bingkai.pack(fill="x", padx=10, pady=(10, 5))

        self.var_tanggal = tk.StringVar(value=date.today().isoformat())
        self.var_kategori = tk.StringVar(value=KATEGORI_VALID[0])
        self.var_deskripsi = tk.StringVar()
        self.var_jumlah = tk.StringVar()

        ttk.Label(bingkai, text="Tanggal (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(bingkai, textvariable=self.var_tanggal, width=18).grid(row=1, column=0, padx=5, pady=2)

        ttk.Label(bingkai, text="Kategori").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Combobox(bingkai, textvariable=self.var_kategori, values=KATEGORI_VALID,
                     state="readonly", width=14).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(bingkai, text="Deskripsi").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        ttk.Entry(bingkai, textvariable=self.var_deskripsi, width=28).grid(row=1, column=2, padx=5, pady=2)

        ttk.Label(bingkai, text="Jumlah (Rp)").grid(row=0, column=3, padx=5, pady=2, sticky="w")
        ttk.Entry(bingkai, textvariable=self.var_jumlah, width=14).grid(row=1, column=3, padx=5, pady=2)

        ttk.Button(bingkai, text="Tambah", command=self.aksi_tambah).grid(row=1, column=4, padx=8, pady=2)

    def _buat_kontrol(self):
        bingkai = ttk.Frame(self.root)
        bingkai.pack(fill="x", padx=10, pady=5)

        ttk.Label(bingkai, text="Cari:").pack(side="left")
        self.var_cari = tk.StringVar()
        # Setiap kali isi kotak cari berubah, tabel langsung diperbarui
        self.var_cari.trace_add("write", lambda *args: self.refresh_tabel())
        ttk.Entry(bingkai, textvariable=self.var_cari, width=24).pack(side="left", padx=5)

        ttk.Label(bingkai, text="Urutkan:").pack(side="left", padx=(15, 0))
        self.var_urut = tk.StringVar(value="tanggal")
        kotak_urut = ttk.Combobox(bingkai, textvariable=self.var_urut,
                                  values=["tanggal", "kategori", "jumlah"],
                                  state="readonly", width=10)
        kotak_urut.pack(side="left", padx=5)
        kotak_urut.bind("<<ComboboxSelected>>", lambda e: self.refresh_tabel())

        self.var_menurun = tk.BooleanVar(value=True)
        ttk.Checkbutton(bingkai, text="Menurun", variable=self.var_menurun,
                        command=self.refresh_tabel).pack(side="left")

        ttk.Button(bingkai, text="Hapus Terpilih", command=self.aksi_hapus).pack(side="right")

    def _buat_tabel(self):
        bingkai = ttk.Frame(self.root)
        bingkai.pack(fill="both", expand=True, padx=10, pady=5)

        kolom = ("id", "tanggal", "kategori", "deskripsi", "jumlah")
        self.tabel = ttk.Treeview(bingkai, columns=kolom, show="headings", height=12)
        judul = {"id": "ID", "tanggal": "Tanggal", "kategori": "Kategori",
                 "deskripsi": "Deskripsi", "jumlah": "Jumlah"}
        lebar = {"id": 40, "tanggal": 100, "kategori": 100, "deskripsi": 340, "jumlah": 120}
        for k in kolom:
            self.tabel.heading(k, text=judul[k])
            self.tabel.column(k, width=lebar[k], anchor="e" if k == "jumlah" else "w")

        scroll = ttk.Scrollbar(bingkai, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scroll.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _buat_ringkasan(self):
        self.label_total = ttk.Label(self.root, font=("Segoe UI", 10, "bold"))
        self.label_total.pack(fill="x", padx=10)
        self.label_kategori = ttk.Label(self.root, wraplength=820, justify="left")
        self.label_kategori.pack(fill="x", padx=10, pady=(0, 10))

    # ---------- Memperbarui tampilan ----------
    def refresh_tabel(self):
        data = self.service.cari(self.var_cari.get())
        data = self.service.urutkan(data, self.var_urut.get(), self.var_menurun.get())

        self.tabel.delete(*self.tabel.get_children())
        for t in data:
            self.tabel.insert("", tk.END,
                              values=(t.id, t.tanggal, t.kategori, t.deskripsi, format_rupiah(t.jumlah)))

        total_tampil = sum(t.jumlah for t in data)
        self.label_total.config(
            text=f"Total ditampilkan: {format_rupiah(total_tampil)}   |   "
                 f"Total seluruh: {format_rupiah(self.service.hitung_total())}")
        per_kategori = self.service.ringkasan_per_kategori(data)
        teks = "  |  ".join(f"{k}: {format_rupiah(v)}" for k, v in sorted(per_kategori.items()))
        self.label_kategori.config(text="Per kategori -> " + (teks if teks else "(belum ada data)"))

    # ---------- Aksi tombol ----------
    def aksi_tambah(self):
        try:
            self.service.tambah(self.var_tanggal.get(), self.var_kategori.get(),
                                self.var_deskripsi.get(), self.var_jumlah.get())
            self._simpan()
        except ValueError as e:
            messagebox.showerror("Input tidak valid", str(e))
            return
        except RuntimeError as e:
            messagebox.showerror("Gagal menyimpan", str(e))
            return
        self.var_deskripsi.set("")
        self.var_jumlah.set("")
        self.refresh_tabel()

    def aksi_hapus(self):
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Pilih data", "Klik satu baris di tabel dulu.")
            return
        id_transaksi = int(self.tabel.item(terpilih[0])["values"][0])
        if not messagebox.askyesno("Konfirmasi", f"Hapus transaksi ID {id_transaksi}?"):
            return
        try:
            self.service.hapus(id_transaksi)
            self._simpan()
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Gagal", str(e))
            return
        self.refresh_tabel()

    def _simpan(self):
        simpan_transaksi(self.path_csv, self.service.daftar)
