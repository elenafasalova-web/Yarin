git init
echo "*.pyc" > .gitignore
echo "__pycache__/" >> .gitignore
import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data_file = "expenses.json"
        self.expenses = self.load_data()

        # Поля ввода
        tk.Label(root, text="Сумма:").grid(row=0, column=0)
        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=0, column=1)

        tk.Label(root, text="Категория:").grid(row=1, column=0)
        self.combo_category = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.combo_category.grid(row=1, column=1)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0)
        self.entry_date = tk.Entry(root)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=2, column=1)

        # Кнопки
        tk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Таблица
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=3)

        # Фильтры
        tk.Label(root, text="Фильтр по категории:").grid(row=5, column=0)
        self.filter_cat = tk.Entry(root)
        self.filter_cat.grid(row=5, column=1)
        tk.Button(root, text="Применить", command=self.refresh_table).grid(row=5, column=2)

        self.label_total = tk.Label(root, text="Итого: 0", font=('Arial', 10, 'bold'))
        self.label_total.grid(row=6, column=0, columnspan=2)

        self.refresh_table()

    def add_expense(self):
        try:
            amount = float(self.entry_amount.get())
            if amount <= 0: raise ValueError
            date_str = self.entry_date.get()
            datetime.strptime(date_str, "%Y-%m-%d") # Валидация формата
            
            new_item = {
                "amount": amount,
                "category": self.combo_category.get() or "Другое",
                "date": date_str
            }
            self.expenses.append(new_item)
            self.save_data()
            self.refresh_table()
            self.entry_amount.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму и дату (ГГГГ-ММ-ДД)")

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        category_filter = self.filter_cat.get().lower()
        total = 0
        
        for item in self.expenses:
            if category_filter in item['category'].lower():
                self.tree.insert("", tk.END, values=(item['amount'], item['category'], item['date']))
                total += item['amount']
        
        self.label_total.config(text=f"Итого за выбранный период/фильтр: {total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
