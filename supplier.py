import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
from tkinter import ttk
from pymongo import MongoClient
from bson.objectid import ObjectId  # Para lidar com _id do MongoDB

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["estoque"]
collection = db["fornecedores"]

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Fornecedores")
        self.root.geometry("700x450")

        # Variável para armazenar o ID selecionado
        self.selected_supplier_id = None  

        # Campos de entrada
        tk.Label(root, text="Invoice No.").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.invoice_entry = tk.Entry(root)
        self.invoice_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Nome Fornecedor").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Contato").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.contact_entry = tk.Entry(root)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Descrição").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=3, column=1, padx=10, pady=5)

        # Botões
        tk.Button(root, text="Salvar", bg="blue", fg="white", command=self.save_supplier).grid(row=4, column=0, padx=5, pady=10)
        tk.Button(root, text="Atualizar", bg="green", fg="white", command=self.update_supplier).grid(row=4, column=1, padx=5, pady=10)
        tk.Button(root, text="Deletar", bg="red", fg="white", command=self.delete_supplier).grid(row=4, column=2, padx=5, pady=10)
        tk.Button(root, text="Limpar", bg="gray", fg="white", command=self.clear_fields).grid(row=4, column=3, padx=5, pady=10)

        # Campo de pesquisa
        tk.Label(root, text="Invoice No").grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=0, column=4, padx=10, pady=5)
        tk.Button(root, text="Buscar", bg="lightblue", command=self.search_supplier).grid(row=0, column=5, padx=5, pady=5)

        # Treeview com coluna para descrição
        self.tree = ttk.Treeview(root, columns=("ID", "Invoice", "Name", "Contact", "Descrição"), show="headings")
        self.tree.heading("ID", text="Sup ID")
        self.tree.heading("Invoice", text="Invoice No.")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Descrição", text="Descrição")
        
        # Configura largura e alinhamento das colunas
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Invoice", width=100, anchor="center")
        self.tree.column("Name", width=120, anchor="center")
        self.tree.column("Contact", width=100, anchor="center")
        self.tree.column("Descrição", width=200, anchor="w")
        
        self.tree.grid(row=5, column=0, columnspan=6, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        # Carregar dados na tabela ao iniciar
        self.load_data()

    def save_supplier(self):
        """Salva um novo fornecedor no MongoDB"""
        data = {
            "invoice_no": self.invoice_entry.get(),
            "name": self.name_entry.get(),
            "contact": self.contact_entry.get(),
            "description": self.desc_entry.get()
        }
        collection.insert_one(data)
        messagebox.showinfo("Sucesso", "Fornecedor salvo com sucesso!")
        self.load_data()
        self.clear_fields()

    def update_supplier(self):
        """Atualiza um fornecedor existente"""
        if not self.selected_supplier_id:
            messagebox.showerror("Erro", "Selecione um fornecedor para atualizar")
            return

        collection.update_one(
            {"_id": ObjectId(self.selected_supplier_id)},
            {"$set": {
                "invoice_no": self.invoice_entry.get(),
                "name": self.name_entry.get(),
                "contact": self.contact_entry.get(),
                "description": self.desc_entry.get()
            }}
        )
        messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
        self.load_data()
        self.clear_fields()

    def delete_supplier(self):
        """Deleta um fornecedor"""
        if not self.selected_supplier_id:
            messagebox.showerror("Erro", "Selecione um fornecedor para deletar")
            return

        collection.delete_one({"_id": ObjectId(self.selected_supplier_id)})
        messagebox.showinfo("Sucesso", "Fornecedor deletado com sucesso!")
        self.load_data()
        self.clear_fields()

    def search_supplier(self):
        """Busca um fornecedor pelo número da fatura"""
        invoice_no = self.search_entry.get()
        supplier = collection.find_one({"invoice_no": invoice_no})

        self.tree.delete(*self.tree.get_children())  # Limpar tabela
        if supplier:
            self.tree.insert("", "end", values=(
                supplier["_id"],
                supplier["invoice_no"],
                supplier["name"],
                supplier["contact"],
                supplier.get("description", "")
            ))
        else:
            messagebox.showerror("Erro", "Fornecedor não encontrado")

    def load_data(self):
        """Carrega todos os fornecedores na tabela"""
        self.tree.delete(*self.tree.get_children())  # Limpar tabela
        for supplier in collection.find():
            self.tree.insert("", "end", values=(
                supplier["_id"],
                supplier["invoice_no"],
                supplier["name"],
                supplier["contact"],
                supplier.get("description", "")
            ))

    def on_tree_select(self, event):
        """Ao clicar na tabela, preenche os campos"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        # Agora, os valores incluem a descrição
        supplier_id, invoice_no, name, contact, description = item["values"]

        self.selected_supplier_id = supplier_id
        self.invoice_entry.delete(0, tk.END)
        self.invoice_entry.insert(0, invoice_no)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.contact_entry.delete(0, tk.END)
        self.contact_entry.insert(0, contact)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, description)

    def clear_fields(self):
        """Limpa os campos de entrada"""
        self.selected_supplier_id = None
        self.invoice_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SupplierClass(root)
    root.mainloop()
