import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["estoque"]
collection = db["categorias"]

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Categorias")
        self.root.geometry("700x400")

        # Rótulo e campo de entrada para nome da categoria
        tk.Label(self.root, text="Nome da Categoria:", font=("Arial", 12)).place(x=20, y=20)
        self.category_entry = tk.Entry(self.root, font=("Arial", 12))
        self.category_entry.place(x=180, y=20, width=200)

        # Botões de ação
        self.add_button = tk.Button(self.root, text="Adicionar", command=self.add_category, bg="green", fg="white", font=("Arial", 12))
        self.add_button.place(x=400, y=15, width=100)

        self.delete_button = tk.Button(self.root, text="Deletar", command=self.delete_category, bg="red", fg="white", font=("Arial", 12))
        self.delete_button.place(x=520, y=15, width=100)

        # Tabela para exibir categorias
        self.category_table = ttk.Treeview(self.root, columns=("ID", "Nome"), show="headings")
        self.category_table.heading("ID", text="C ID")
        self.category_table.heading("Nome", text="Nome")
        self.category_table.column("ID", width=50)
        self.category_table.column("Nome", width=200)
        self.category_table.place(x=20, y=80, width=650, height=300)

        # Evento de clique na tabela
        self.category_table.bind("<ButtonRelease-1>", self.load_selected_category)

        # Carregar dados do banco de dados
        self.load_categories()

    def add_category(self):
        """Adiciona uma nova categoria ao MongoDB."""
        category_name = self.category_entry.get().strip()
        if category_name:
            collection.insert_one({"nome": category_name})
            self.category_entry.delete(0, tk.END)
            self.load_categories()
        else:
            messagebox.showwarning("Aviso", "Digite um nome válido para a categoria.")

    def load_categories(self):
        """Carrega as categorias do banco de dados na tabela."""
        for item in self.category_table.get_children():
            self.category_table.delete(item)
        for idx, category in enumerate(collection.find(), start=1):
            self.category_table.insert("", "end", values=(idx, category["nome"]))

    def load_selected_category(self, event):
        """Carrega a categoria selecionada no campo de entrada."""
        selected_item = self.category_table.selection()
        if selected_item:
            values = self.category_table.item(selected_item, "values")
            if values:
                self.category_entry.delete(0, tk.END)
                self.category_entry.insert(0, values[1])

    def delete_category(self):
        """Deleta a categoria selecionada do MongoDB."""
        selected_item = self.category_table.selection()
        if selected_item:
            values = self.category_table.item(selected_item, "values")
            if values:
                category_name = values[1]
                collection.delete_one({"nome": category_name})
                self.category_entry.delete(0, tk.END)
                self.load_categories()
        else:
            messagebox.showwarning("Aviso", "Selecione uma categoria para deletar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CategoryClass(root)
    root.mainloop()
