import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os

class FidelidadeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Fidelidade")
        self.root.geometry("1200x800")
        self.root.config(bg="#f0f0f0")
        
        # Conexão com MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["estoque"]
        self.clientes = self.db["clientes"]
        self.vendas = self.db["vendas"]
        
        # Criar índices
        self.clientes.create_index([("cpf", 1)], unique=True)
        
        # Configurar interface
        self.setup_ui()
        
    def setup_ui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = tk.Label(main_frame, text="Gestão de Fidelidade", 
                        font=("Arial", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=10)
        
        # Frame para Cadastro/Edição
        cadastro_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        cadastro_frame.pack(fill=tk.X, pady=10)
        
        # Campos do formulário
        self.campos = {
            "Nome": tk.StringVar(),
            "CPF": tk.StringVar(),
            "Email": tk.StringVar(),
            "Telefone": tk.StringVar(),
            "Endereço": tk.StringVar()
        }
        
        row = 0
        for label, var in self.campos.items():
            tk.Label(cadastro_frame, text=label + ":", font=("Arial", 12), 
                    bg="white").grid(row=row, column=0, padx=5, pady=5)
            tk.Entry(cadastro_frame, textvariable=var, 
                    font=("Arial", 12)).grid(row=row, column=1, padx=5, pady=5)
            row += 1
        
        # Botões
        buttons_frame = tk.Frame(cadastro_frame, bg="white")
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        tk.Button(buttons_frame, text="Cadastrar", command=self.cadastrar_cliente,
                 bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Atualizar", command=self.atualizar_cliente,
                 bg="#2196F3", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Limpar", command=self.limpar_campos,
                 bg="#FFC107", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # Frame para Lista de Clientes
        list_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para clientes
        columns = ("CPF", "Nome", "Pontos", "Nível", "Última Compra")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_cliente)
        
        # Frame para Histórico
        historico_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        historico_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(historico_frame, text="Histórico de Compras", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        
        # Treeview para histórico
        columns = ("Data", "Nota Fiscal", "Valor", "Pontos")
        self.historico_tree = ttk.Treeview(historico_frame, columns=columns, show="headings")
        
        for col in columns:
            self.historico_tree.heading(col, text=col)
            self.historico_tree.column(col, width=100)
        
        self.historico_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Carregar dados
        self.carregar_clientes()
    
    def cadastrar_cliente(self):
        try:
            cliente = {
                "nome": self.campos["Nome"].get(),
                "cpf": self.campos["CPF"].get(),
                "email": self.campos["Email"].get(),
                "telefone": self.campos["Telefone"].get(),
                "endereco": self.campos["Endereço"].get(),
                "pontos": 0,
                "nivel": "Bronze",
                "data_cadastro": datetime.now(),
                "ultima_compra": None
            }
            
            if not all([cliente["nome"], cliente["cpf"]]):
                messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios!")
                return
            
            self.clientes.insert_one(cliente)
            self.limpar_campos()
            self.carregar_clientes()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {str(e)}")
    
    def atualizar_cliente(self):
        try:
            cpf = self.campos["CPF"].get()
            if not cpf:
                messagebox.showwarning("Atenção", "Selecione um cliente para atualizar!")
                return
            
            update_data = {
                "nome": self.campos["Nome"].get(),
                "email": self.campos["Email"].get(),
                "telefone": self.campos["Telefone"].get(),
                "endereco": self.campos["Endereço"].get(),
            }
            
            self.clientes.update_one(
                {"cpf": cpf},
                {"$set": update_data}
            )
            
            self.carregar_clientes()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {str(e)}")
    
    def limpar_campos(self):
        for var in self.campos.values():
            var.set("")
    
    def carregar_clientes(self):
        self.tree.delete(*self.tree.get_children())
        for cliente in self.clientes.find():
            ultima_compra = cliente.get("ultima_compra", "Sem compras")
            if ultima_compra:
                ultima_compra = ultima_compra.strftime("%d/%m/%Y")
            
            self.tree.insert("", tk.END, values=(
                cliente["cpf"],
                cliente["nome"],
                cliente.get("pontos", 0),
                cliente.get("nivel", "Bronze"),
                ultima_compra
            ))
    
    def selecionar_cliente(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        cpf = self.tree.item(selection[0])["values"][0]
        cliente = self.clientes.find_one({"cpf": cpf})
        
        if cliente:
            self.campos["Nome"].set(cliente["nome"])
            self.campos["CPF"].set(cliente["cpf"])
            self.campos["Email"].set(cliente.get("email", ""))
            self.campos["Telefone"].set(cliente.get("telefone", ""))
            self.campos["Endereço"].set(cliente.get("endereco", ""))
            
            # Carregar histórico
            self.carregar_historico(cpf)
    
    def carregar_historico(self, cpf):
        self.historico_tree.delete(*self.historico_tree.get_children())
        vendas = self.vendas.find({"cliente_cpf": cpf}).sort("data", -1)
        
        for venda in vendas:
            self.historico_tree.insert("", tk.END, values=(
                venda["data"].strftime("%d/%m/%Y %H:%M"),
                venda["nota_fiscal"],
                f"R$ {venda['total']:.2f}",
                venda.get("pontos_ganhos", 0)
            ))
    
    def calcular_nivel(self, pontos):
        if pontos >= 1000:
            return "Ouro"
        elif pontos >= 500:
            return "Prata"
        else:
            return "Bronze"
    
    def atualizar_pontos(self, cpf, valor_compra):
        # Cada R$ 1,00 = 1 ponto
        pontos_ganhos = int(valor_compra)
        
        cliente = self.clientes.find_one({"cpf": cpf})
        if cliente:
            pontos_atuais = cliente.get("pontos", 0) + pontos_ganhos
            nivel = self.calcular_nivel(pontos_atuais)
            
            self.clientes.update_one(
                {"cpf": cpf},
                {
                    "$set": {
                        "pontos": pontos_atuais,
                        "nivel": nivel,
                        "ultima_compra": datetime.now()
                    }
                }
            )
            
            return pontos_ganhos
        return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = FidelidadeManager(root)
    root.mainloop() 