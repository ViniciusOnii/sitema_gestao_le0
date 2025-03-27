import pymongo
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os
from fidelidade import FidelidadeManager

class POS:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema POS")
        self.root.geometry("1200x800")
        self.root.config(bg="#f0f0f0")

        # Conectar ao MongoDB
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["estoque"]
            self.collection = self.db["produtos"]
            self.vendas = self.db["vendas"]
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao MongoDB.\n{e}")
            return

        # Criar índice para busca otimizada
        self.collection.create_index([("nome", pymongo.TEXT)])

        # Variáveis
        self.var_produto = StringVar()
        self.var_preco = StringVar()
        self.var_quantidade = StringVar(value="1")
        self.var_desconto = StringVar(value="0")
        self.var_cliente = StringVar()
        self.var_telefone = StringVar()
        self.var_cpf = StringVar()
        self.var_pontos = StringVar(value="0")
        self.total_valor = DoubleVar(value=0.0)
        self.carrinho = []

        # Frame Principal
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Frame de Busca
        frame_busca = Frame(main_frame, bd=2, relief=RIDGE, bg="white", padx=10, pady=10)
        frame_busca.pack(fill=X, pady=(0,10))

        Label(frame_busca, text="Buscar Produto:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        self.entry_busca = Entry(frame_busca, textvariable=self.var_produto, font=("Arial", 12), width=30)
        self.entry_busca.pack(side=LEFT, padx=5)
        Button(frame_busca, text="Buscar", command=self.buscar_produto, 
               font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=LEFT, padx=5)

        # Frame de Informações do Cliente
        frame_cliente = Frame(main_frame, bd=2, relief=RIDGE, bg="white", padx=10, pady=10)
        frame_cliente.pack(fill=X, pady=(0,10))

        Label(frame_cliente, text="Nome do Cliente:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        Entry(frame_cliente, textvariable=self.var_cliente, font=("Arial", 12), width=30).pack(side=LEFT, padx=5)
        
        Label(frame_cliente, text="CPF:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        Entry(frame_cliente, textvariable=self.var_cpf, font=("Arial", 12), width=15).pack(side=LEFT, padx=5)
        
        Label(frame_cliente, text="Telefone:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        Entry(frame_cliente, textvariable=self.var_telefone, font=("Arial", 12), width=15).pack(side=LEFT, padx=5)

        Label(frame_cliente, text="Pontos:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        Label(frame_cliente, textvariable=self.var_pontos, font=("Arial", 12, "bold"), fg="green").pack(side=LEFT, padx=5)

        Button(frame_cliente, text="Buscar Cliente", command=self.buscar_cliente,
               font=("Arial", 12), bg="#2196F3", fg="white").pack(side=LEFT, padx=5)

        # Lista de Produtos
        frame_produtos = Frame(main_frame, bd=2, relief=RIDGE, bg="white")
        frame_produtos.pack(fill=BOTH, expand=True, pady=(0,10))

        # Treeview para produtos
        self.tree = ttk.Treeview(frame_produtos, columns=("nome", "preco", "estoque"), show='headings', height=5)
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("estoque", text="Estoque")
        self.tree.column("nome", width=300)
        self.tree.column("preco", width=100)
        self.tree.column("estoque", width=100)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.tree.bind("<Double-1>", self.selecionar_produto)

        # Scrollbar para a lista de produtos
        scrollbar = ttk.Scrollbar(frame_produtos, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Frame do Carrinho
        frame_carrinho = Frame(main_frame, bd=2, relief=RIDGE, bg="white", padx=10, pady=10)
        frame_carrinho.pack(fill=BOTH, expand=True)

        # Campos do Carrinho
        Label(frame_carrinho, text="Produto:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        Entry(frame_carrinho, textvariable=self.var_produto, state="readonly", 
              font=("Arial", 12), width=30).grid(row=0, column=1, padx=5, pady=5)

        Label(frame_carrinho, text="Preço:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
        Entry(frame_carrinho, textvariable=self.var_preco, state="readonly", 
              font=("Arial", 12), width=10).grid(row=0, column=3, padx=5, pady=5)

        Label(frame_carrinho, text="Quantidade:", font=("Arial", 12)).grid(row=0, column=4, padx=5, pady=5)
        Entry(frame_carrinho, textvariable=self.var_quantidade, 
              font=("Arial", 12), width=5).grid(row=0, column=5, padx=5, pady=5)

        Label(frame_carrinho, text="Desconto (%):", font=("Arial", 12)).grid(row=0, column=6, padx=5, pady=5)
        Entry(frame_carrinho, textvariable=self.var_desconto, 
              font=("Arial", 12), width=5).grid(row=0, column=7, padx=5, pady=5)

        Button(frame_carrinho, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho,
               font=("Arial", 12), bg="#2196F3", fg="white").grid(row=0, column=8, padx=10, pady=5)

        # Tabela do Carrinho
        self.cart_table = ttk.Treeview(frame_carrinho, columns=("nome", "preco", "quantidade", "subtotal"), 
                                      show='headings', height=8)
        self.cart_table.heading("nome", text="Nome")
        self.cart_table.heading("preco", text="Preço")
        self.cart_table.heading("quantidade", text="Quantidade")
        self.cart_table.heading("subtotal", text="Subtotal")
        self.cart_table.column("nome", width=300)
        self.cart_table.column("preco", width=100)
        self.cart_table.column("quantidade", width=100)
        self.cart_table.column("subtotal", width=100)
        self.cart_table.grid(row=1, column=0, columnspan=9, sticky="nsew", pady=10)

        # Configurar grid weights
        frame_carrinho.grid_columnconfigure(0, weight=1)
        frame_carrinho.grid_rowconfigure(1, weight=1)

        # Frame de Total e Botões
        frame_total = Frame(main_frame, bd=2, relief=RIDGE, bg="white", padx=10, pady=10)
        frame_total.pack(fill=X)

        Label(frame_total, text="Total: R$", font=("Arial", 14, "bold")).pack(side=LEFT, padx=10)
        Label(frame_total, textvariable=self.total_valor, 
              font=("Arial", 14, "bold"), fg="green").pack(side=LEFT)

        Button(frame_total, text="Limpar Carrinho", command=self.limpar_carrinho,
               font=("Arial", 12), bg="#FFC107", fg="black").pack(side=LEFT, padx=10)
        Button(frame_total, text="Finalizar Compra", command=self.finalizar_compra,
               font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=LEFT, padx=10)

    def buscar_produto(self):
        self.tree.delete(*self.tree.get_children())
        nome_produto = self.var_produto.get()
        resultados = self.collection.find({"nome": {"$regex": nome_produto, "$options": "i"}})
        for produto in resultados:
            self.tree.insert("", END, values=(produto["nome"], produto["preco"], produto["quantidade"]))

    def selecionar_produto(self, event):
        item = self.tree.focus()
        valores = self.tree.item(item, "values")
        if valores:
            self.var_produto.set(valores[0])
            self.var_preco.set(valores[1])

    def adicionar_ao_carrinho(self):
        try:
            nome = self.var_produto.get()
            preco = float(self.var_preco.get())
            quantidade = int(self.var_quantidade.get())
            desconto = float(self.var_desconto.get() or 0)
            
            if nome and quantidade > 0:
                subtotal = preco * quantidade * (1 - desconto/100)
                self.carrinho.append((nome, preco, quantidade, subtotal))
                self.atualizar_carrinho()
                
                # Limpar campos
                self.var_produto.set("")
                self.var_preco.set("")
                self.var_quantidade.set("1")
                self.var_desconto.set("0")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos")

    def atualizar_carrinho(self):
        self.cart_table.delete(*self.cart_table.get_children())
        total = sum(item[3] for item in self.carrinho)
        self.total_valor.set(f"{total:.2f}")
        
        for item in self.carrinho:
            self.cart_table.insert("", END, values=item)

    def limpar_carrinho(self):
        self.carrinho.clear()
        self.atualizar_carrinho()

    def buscar_cliente(self):
        cpf = self.var_cpf.get()
        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF do cliente!")
            return
            
        cliente = self.db["clientes"].find_one({"cpf": cpf})
        if cliente:
            self.var_cliente.set(cliente["nome"])
            self.var_telefone.set(cliente.get("telefone", ""))
            self.var_pontos.set(str(cliente.get("pontos", 0)))
        else:
            messagebox.showinfo("Cliente não encontrado", 
                              "Cliente não cadastrado. Deseja cadastrar?")
            self.abrir_cadastro_cliente()

    def abrir_cadastro_cliente(self):
        cadastro_window = Toplevel(self.root)
        FidelidadeManager(cadastro_window)

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showwarning("Aviso", "O carrinho está vazio!")
            return
            
        if not self.var_cliente.get():
            messagebox.showwarning("Aviso", "Por favor, informe o nome do cliente!")
            return

        # Gerar número da nota fiscal
        nota_fiscal = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Calcular total
        total = float(self.total_valor.get())
        
        # Atualizar pontos do cliente se tiver CPF
        pontos_ganhos = 0
        if self.var_cpf.get():
            try:
                # Calcular pontos (1 ponto por real gasto)
                pontos_ganhos = int(total)
                
                # Atualizar pontos no banco de dados
                cliente = self.db["clientes"].find_one({"cpf": self.var_cpf.get()})
                if cliente:
                    pontos_atuais = cliente.get("pontos", 0)
                    novos_pontos = pontos_atuais + pontos_ganhos
                    
                    # Atualizar pontos do cliente
                    self.db["clientes"].update_one(
                        {"cpf": self.var_cpf.get()},
                        {"$set": {"pontos": novos_pontos}}
                    )
                    
                    # Atualizar nível do cliente
                    nivel = "Bronze"
                    if novos_pontos >= 1000:
                        nivel = "Ouro"
                    elif novos_pontos >= 500:
                        nivel = "Prata"
                    
                    self.db["clientes"].update_one(
                        {"cpf": self.var_cpf.get()},
                        {"$set": {"nivel": nivel}}
                    )
            except Exception as e:
                print(f"Erro ao atualizar pontos: {e}")
                messagebox.showwarning("Aviso", "Erro ao atualizar pontos do cliente")
        
        # Salvar venda no MongoDB
        venda = {
            "nota_fiscal": nota_fiscal,
            "cliente": self.var_cliente.get(),
            "cliente_cpf": self.var_cpf.get(),
            "telefone": self.var_telefone.get(),
            "data": datetime.now(),
            "itens": self.carrinho,
            "total": total,
            "pontos_ganhos": pontos_ganhos
        }
        self.vendas.insert_one(venda)
        
        # Atualizar estoque
        for item in self.carrinho:
            self.collection.update_one(
                {"nome": item[0]},
                {"$inc": {"quantidade": -item[2]}}
            )
        
        # Emitir nota fiscal
        self.emitir_nota(
            self.var_cliente.get(),
            self.var_telefone.get(),
            nota_fiscal,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.carrinho,
            total,
            pontos_ganhos
        )
        
        # Limpar carrinho
        self.limpar_carrinho()
        self.var_cliente.set("")
        self.var_telefone.set("")
        self.var_cpf.set("")
        self.var_pontos.set("0")
        
        messagebox.showinfo("Sucesso", f"Venda finalizada com sucesso!\nPontos ganhos: {pontos_ganhos}")

    def emitir_nota(self, cliente, telefone, nota_fiscal, data, itens, total, pontos_ganhos):
        if not os.path.exists('bill'):
            os.makedirs('bill')
            
        nota = f"""
        ============================================
                      XYZ-Inventory
        Phone No. 98725***** , Delhi-125001
        ============================================
        Cliente: {cliente}
        CPF: {self.var_cpf.get()}
        Telefone: {telefone}
        Nota Fiscal: {nota_fiscal}      Data: {data}
        --------------------------------------------
        Produto       QTD       Preço       Subtotal
        --------------------------------------------
        """
        
        for item in itens:
            nota += f"{item[0]:<15} {item[2]:<10} R$ {item[1]:<10.2f} R$ {item[3]:.2f}\n"
            
        nota += f"""
        --------------------------------------------
        Total: R$ {total:.2f}
        Pontos ganhos: {pontos_ganhos}
        ============================================
        """
        
        with open(f'bill/nota_{nota_fiscal}.txt', 'w', encoding='utf-8') as file:
            file.write(nota)
            
        messagebox.showinfo("Nota Fiscal", nota)

if __name__ == "__main__":
    root = Tk()
    app = POS(root)
    root.mainloop()
