"""main.py - titik masuk aplikasi. Jalankan dengan:  python main.py"""
import os
import tkinter as tk

from services import ExpenseService
from storage import muat_transaksi
from ui import ExpenseApp

PATH_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "transaksi.csv")


def main():
    try:
        daftar = muat_transaksi(PATH_CSV)
    except RuntimeError as e:
        print(e)
        daftar = []
    root = tk.Tk()
    ExpenseApp(root, ExpenseService(daftar), PATH_CSV)
    root.mainloop()


if __name__ == "__main__":
    main()
