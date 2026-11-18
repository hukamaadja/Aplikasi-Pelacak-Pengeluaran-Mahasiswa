"""Modul models berisi definisi struktur data transaksi pengeluaran."""


class Expense:
    """Merepresentasikan satu entitas catatan pengeluaran mahasiswa."""

    def __init__(self, expense_id: str, date: str, description: str, category: str, amount: float):
        """Inisialisasi atribut objek pengeluaran."""
        self.expense_id = expense_id
        self.date = date
        self.description = description
        self.category = category
        self.amount = float(amount)

    def to_dict(self) -> dict:
        """Mengubah objek Expense menjadi dictionary untuk penyimpanan CSV."""
        return {
            "id": self.expense_id,
            "date": self.date,
            "description": self.description,
            "category": self.category,
            "amount": self.amount,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Membuat objek Expense dari dictionary hasil pembacaan file."""
        return cls(
            expense_id=data["id"],
            date=data["date"],
            description=data["description"],
            category=data["category"],
            amount=float(data["amount"]),
        )