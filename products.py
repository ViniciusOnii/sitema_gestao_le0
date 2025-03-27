import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu, ttk
from pymongo import MongoClient
from datetime import datetime

class ProductManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Produtos")
        self.root.geometry("1000x700")
        self.root.config(bg="#f0f0f0")
        
        # Conecta ao MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["estoque"]
        self.collection = self.db["produtos"]
        self.categoria_collection = self.db["categorias"]
        self.fornecedor_collection = self.db["fornecedores"]

        # Variáveis
        self.var_id = StringVar()
        self.var_categoria = StringVar()
        self.var_fornecedor = StringVar()
        self.var_nome = StringVar()
        self.var_preco = StringVar()
        self.var_quantidade = StringVar()
        self.var_status = StringVar(value="ativo")
        self.var_busca = StringVar()

        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title = tk.Label(main_frame, text="Gerenciamento de Produtos", 
                        font=("Arial", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Frame de Busca
        search_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        search_frame.pack(fill=tk.X, pady=(0,10))

        tk.Label(search_frame, text="Buscar:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, textvariable=self.var_busca, font=("Arial", 12), width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Buscar", command=self.search_products,
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        # Frame de Dados
        data_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        # Campos de Entrada
        fields_frame = tk.Frame(data_frame, bg="white")
        fields_frame.pack(fill=tk.X, pady=10)

        # Grid de campos
        fields = [
            ("Categoria:", self.var_categoria, True),
            ("Fornecedor:", self.var_fornecedor, True),
            ("Nome:", self.var_nome, False),
            ("Preço:", self.var_preco, False),
            ("Quantidade:", self.var_quantidade, False),
            ("Status:", self.var_status, True)
        ]

        for i, (label, var, is_combo) in enumerate(fields):
            tk.Label(fields_frame, text=label, font=("Arial", 12), bg="white").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            if is_combo:
                if label == "Categoria:":
                    values = self.get_category_options()
                elif label == "Fornecedor:":
                    values = self.get_supplier_options()
                else:
                    values = ["ativo", "inativo"]
                
                ttk.Combobox(fields_frame, textvariable=var, values=values, 
                            state="readonly", font=("Arial", 12)).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            else:
                tk.Entry(fields_frame, textvariable=var, font=("Arial", 12)).grid(row=i, column=1, padx=5, pady=5, sticky="w")

        # Botões
        buttons_frame = tk.Frame(data_frame, bg="white")
        buttons_frame.pack(fill=tk.X, pady=10)

        buttons = [
            ("Adicionar", self.add_product, "#4CAF50"),
            ("Atualizar", self.update_product, "#2196F3"),
            ("Excluir", self.delete_product, "#F44336"),
            ("Limpar", self.clear_fields, "#FFC107")
        ]

        for text, command, color in buttons:
            tk.Button(buttons_frame, text=text, command=command,
                     font=("Arial", 12), bg=color, fg="white").pack(side=tk.LEFT, padx=5)

        # Tabela de Produtos
        table_frame = tk.Frame(data_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview
        columns = ("ID", "Categoria", "Fornecedor", "Nome", "Preço", "Quantidade", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Configurar grid weights
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def get_category_options(self):
        return [cat["nome"] for cat in self.categoria_collection.find()]

    def get_supplier_options(self):
        return [sup["name"] for sup in self.fornecedor_collection.find()]

    def search_products(self):
        search_term = self.var_busca.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        query = {
            "$or": [
                {"nome": {"$regex": search_term, "$options": "i"}},
                {"categoria": {"$regex": search_term, "$options": "i"}},
                {"fornecedor": {"$regex": search_term, "$options": "i"}}
            ]
        }
        
        for product in self.collection.find(query):
            self.tree.insert("", tk.END, values=(
                str(product["_id"]),
                product.get("categoria", ""),
                product.get("fornecedor", ""),
                product.get("nome", ""),
                f"R$ {product.get('preco', 0):.2f}",
                product.get("quantidade", 0),
                product.get("status", "ativo")
            ))

    def load_products(self):
        self.tree.delete(*self.tree.get_children())
        for product in self.collection.find():
            self.tree.insert("", tk.END, values=(
                str(product["_id"]),
                product.get("categoria", ""),
                product.get("fornecedor", ""),
                product.get("nome", ""),
                f"R$ {product.get('preco', 0):.2f}",
                product.get("quantidade", 0),
                product.get("status", "ativo")
            ))

    def add_product(self):
        try:
            product = {
                "categoria": self.var_categoria.get(),
                "fornecedor": self.var_fornecedor.get(),
                "nome": self.var_nome.get(),
                "preco": float(self.var_preco.get()),
                "quantidade": int(self.var_quantidade.get()),
                "status": self.var_status.get(),
                "data_cadastro": datetime.now()
            }

            if not all([product["categoria"], product["fornecedor"], product["nome"]]):
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
                return

            self.collection.insert_one(product)
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores de preço e quantidade!")

    def update_product(self):
        try:
            if not self.var_id.get():
                messagebox.showwarning("Atenção", "Selecione um produto para atualizar!")
                return

            product = {
                "categoria": self.var_categoria.get(),
                "fornecedor": self.var_fornecedor.get(),
                "nome": self.var_nome.get(),
                "preco": float(self.var_preco.get()),
                "quantidade": int(self.var_quantidade.get()),
                "status": self.var_status.get(),
                "data_atualizacao": datetime.now()
            }

            if not all([product["categoria"], product["fornecedor"], product["nome"]]):
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
                return

            self.collection.update_one(
                {"_id": self.var_id.get()},
                {"$set": product}
            )
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores de preço e quantidade!")

    def delete_product(self):
        if not self.var_id.get():
            messagebox.showwarning("Atenção", "Selecione um produto para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este produto?"):
            self.collection.delete_one({"_id": self.var_id.get()})
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        self.var_id.set(values[0])
        self.var_categoria.set(values[1])
        self.var_fornecedor.set(values[2])
        self.var_nome.set(values[3])
        self.var_preco.set(values[4].replace("R$ ", ""))
        self.var_quantidade.set(values[5])
        self.var_status.set(values[6])

    def clear_fields(self):
        self.var_id.set("")
        self.var_categoria.set("")
        self.var_fornecedor.set("")
        self.var_nome.set("")
        self.var_preco.set("")
        self.var_quantidade.set("")
        self.var_status.set("ativo")
        self.var_busca.set("")
        self.tree.selection_remove(*self.tree.selection())

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManager(root)
    root.mainloop()
