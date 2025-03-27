import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

class FinanceiroManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão Financeira e Relatórios")
        self.root.geometry("1200x800")
        self.root.config(bg="#f0f0f0")
        
        # Conexão com MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["estoque"]
        self.produtos = self.db["produtos"]
        self.vendas = self.db["vendas"]
        self.financeiro = self.db["financeiro"]
        
        # Criar coleção financeiro se não existir
        if "financeiro" not in self.db.list_collection_names():
            self.financeiro.insert_one({
                "tipo": "inicial",
                "data": datetime.now(),
                "valor": 0,
                "descricao": "Saldo inicial"
            })
        
        self.setup_ui()
        self.atualizar_dashboard()

    def setup_ui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title = tk.Label(main_frame, text="Gestão Financeira e Relatórios", 
                        font=("Arial", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Frame para Dashboard
        dashboard_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        dashboard_frame.pack(fill=tk.X, pady=(0,10))

        # Cards de Informação
        self.lbl_saldo = tk.Label(dashboard_frame, text="Saldo Atual\nR$ 0,00", 
                                 font=("Arial", 14, "bold"), bg="#4CAF50", fg="white")
        self.lbl_saldo.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.lbl_produtos_baixos = tk.Label(dashboard_frame, text="Produtos com Estoque Baixo\n0", 
                                          font=("Arial", 14, "bold"), bg="#FFC107", fg="black")
        self.lbl_produtos_baixos.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.lbl_vendas_mes = tk.Label(dashboard_frame, text="Vendas do Mês\nR$ 0,00", 
                                     font=("Arial", 14, "bold"), bg="#2196F3", fg="white")
        self.lbl_vendas_mes.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        # Frame para Gráficos
        graphs_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        graphs_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        # Gráfico de Vendas
        self.fig_vendas = plt.Figure(figsize=(6, 4))
        self.canvas_vendas = FigureCanvasTkAgg(self.fig_vendas, master=graphs_frame)
        self.canvas_vendas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Gráfico de Produtos
        self.fig_produtos = plt.Figure(figsize=(6, 4))
        self.canvas_produtos = FigureCanvasTkAgg(self.fig_produtos, master=graphs_frame)
        self.canvas_produtos.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Frame para Relatórios
        reports_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        reports_frame.pack(fill=tk.X, pady=(0,10))

        # Botões de Relatório
        tk.Button(reports_frame, text="Exportar Relatório de Vendas", 
                 command=self.exportar_relatorio_vendas,
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(reports_frame, text="Exportar Relatório de Estoque", 
                 command=self.exportar_relatorio_estoque,
                 font=("Arial", 12), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(reports_frame, text="Exportar Relatório Financeiro", 
                 command=self.exportar_relatorio_financeiro,
                 font=("Arial", 12), bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)

        # Frame para Alertas
        alerts_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        alerts_frame.pack(fill=tk.X)

        # Lista de Alertas
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=("Data", "Tipo", "Mensagem"), show="headings")
        self.alerts_tree.heading("Data", text="Data")
        self.alerts_tree.heading("Tipo", text="Tipo")
        self.alerts_tree.heading("Mensagem", text="Mensagem")
        self.alerts_tree.pack(fill=tk.X, pady=5)

    def atualizar_dashboard(self):
        # Atualizar saldo
        saldo = self.calcular_saldo()
        self.lbl_saldo.config(text=f"Saldo Atual\nR$ {saldo:.2f}")

        # Atualizar produtos com estoque baixo
        produtos_baixos = self.verificar_estoque_baixo()
        self.lbl_produtos_baixos.config(text=f"Produtos com Estoque Baixo\n{len(produtos_baixos)}")

        # Atualizar vendas do mês
        vendas_mes = self.calcular_vendas_mes()
        self.lbl_vendas_mes.config(text=f"Vendas do Mês\nR$ {vendas_mes:.2f}")

        # Atualizar gráficos
        self.atualizar_grafico_vendas()
        self.atualizar_grafico_produtos()

        # Atualizar alertas
        self.atualizar_alertas()

    def calcular_saldo(self):
        saldo = 0
        for mov in self.financeiro.find():
            if mov["tipo"] == "entrada":
                saldo += mov["valor"]
            else:
                saldo -= mov["valor"]
        return saldo

    def verificar_estoque_baixo(self):
        produtos_baixos = []
        for produto in self.produtos.find():
            # Verifica se existe o campo quantidade ou qtde
            quantidade = produto.get("quantidade", produto.get("qtde", 0))
            if quantidade < 10:  # Considera baixo menos de 10 unidades
                produtos_baixos.append(produto)
        return produtos_baixos

    def calcular_vendas_mes(self):
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        vendas = self.vendas.find({"data": {"$gte": inicio_mes}})
        return sum(venda["total"] for venda in vendas)

    def atualizar_grafico_vendas(self):
        self.fig_vendas.clear()
        ax = self.fig_vendas.add_subplot(111)
        
        # Buscar vendas dos últimos 7 dias
        datas = []
        valores = []
        for i in range(7):
            data = datetime.now() - timedelta(days=i)
            inicio_dia = data.replace(hour=0, minute=0, second=0, microsecond=0)
            fim_dia = data.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            vendas = self.vendas.find({"data": {"$gte": inicio_dia, "$lte": fim_dia}})
            total = sum(venda["total"] for venda in vendas)
            
            datas.append(data.strftime("%d/%m"))
            valores.append(total)
        
        ax.bar(datas[::-1], valores[::-1])
        ax.set_title("Vendas dos Últimos 7 Dias")
        ax.set_xlabel("Data")
        ax.set_ylabel("Valor (R$)")
        
        self.canvas_vendas.draw()

    def atualizar_grafico_produtos(self):
        try:
            self.fig_produtos.clear()
            ax = self.fig_produtos.add_subplot(111)
            
            # Buscar produtos mais vendidos
            produtos = {}
            for venda in self.vendas.find():
                try:
                    for item in venda.get("itens", []):
                        try:
                            # Verifica se item é uma lista/tupla com pelo menos 3 elementos
                            if isinstance(item, (list, tuple)) and len(item) >= 3:
                                nome_produto = str(item[0])
                                # Tenta converter a quantidade para inteiro, se falhar usa 0
                                try:
                                    quantidade = int(item[2])
                                except (ValueError, TypeError):
                                    quantidade = 0
                                
                                if nome_produto not in produtos:
                                    produtos[nome_produto] = 0
                                produtos[nome_produto] += quantidade
                        except Exception as e:
                            print(f"Erro ao processar item: {e}")
                            continue
                except Exception as e:
                    print(f"Erro ao processar venda: {e}")
                    continue
            
            if produtos:
                # Ordenar por quantidade vendida
                produtos_ordenados = dict(sorted(produtos.items(), key=lambda x: x[1], reverse=True)[:5])
                
                ax.bar(produtos_ordenados.keys(), produtos_ordenados.values())
                ax.set_title("Top 5 Produtos Mais Vendidos")
                ax.set_xlabel("Produto")
                ax.set_ylabel("Quantidade")
                
                # Ajusta o layout para melhor visualização
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
                self.fig_produtos.tight_layout()
            else:
                ax.text(0.5, 0.5, "Sem dados de vendas", 
                       horizontalalignment='center', verticalalignment='center')
            
            self.canvas_produtos.draw()
        except Exception as e:
            print(f"Erro ao atualizar gráfico de produtos: {e}")
            messagebox.showerror("Erro", "Não foi possível atualizar o gráfico de produtos")

    def atualizar_alertas(self):
        self.alerts_tree.delete(*self.alerts_tree.get_children())
        
        # Verificar produtos com estoque baixo
        produtos_baixos = self.verificar_estoque_baixo()
        for produto in produtos_baixos:
            quantidade = produto.get("quantidade", produto.get("qtde", 0))
            self.alerts_tree.insert("", "end", values=(
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Estoque Baixo",
                f"{produto.get('nome', 'Sem nome')} - Quantidade: {quantidade}"
            ))

    def exportar_relatorio_vendas(self):
        try:
            # Buscar todas as vendas
            vendas = list(self.vendas.find())
            
            # Criar DataFrame
            dados = []
            for venda in vendas:
                for item in venda["itens"]:
                    dados.append({
                        "Data": venda["data"].strftime("%d/%m/%Y %H:%M"),
                        "Nota Fiscal": venda["nota_fiscal"],
                        "Cliente": venda["cliente"],
                        "Produto": item[0],
                        "Quantidade": item[2],
                        "Preço Unitário": item[1],
                        "Subtotal": item[3],
                        "Total": venda["total"]
                    })
            
            df = pd.DataFrame(dados)
            
            # Exportar para Excel
            if not os.path.exists("relatorios"):
                os.makedirs("relatorios")
            df.to_excel("relatorios/relatorio_vendas.xlsx", index=False)
            
            messagebox.showinfo("Sucesso", "Relatório de vendas exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")

    def exportar_relatorio_estoque(self):
        try:
            # Buscar todos os produtos
            produtos = list(self.produtos.find())
            
            # Criar DataFrame
            dados = []
            for produto in produtos:
                dados.append({
                    "Nome": produto["nome"],
                    "Categoria": produto["categoria"],
                    "Fornecedor": produto["fornecedor"],
                    "Preço": produto["preco"],
                    "Quantidade": produto["quantidade"],
                    "Status": produto["status"]
                })
            
            df = pd.DataFrame(dados)
            
            # Exportar para Excel
            if not os.path.exists("relatorios"):
                os.makedirs("relatorios")
            df.to_excel("relatorios/relatorio_estoque.xlsx", index=False)
            
            messagebox.showinfo("Sucesso", "Relatório de estoque exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")

    def exportar_relatorio_financeiro(self):
        try:
            # Buscar todas as movimentações financeiras
            movimentacoes = list(self.financeiro.find())
            
            # Criar DataFrame
            dados = []
            for mov in movimentacoes:
                dados.append({
                    "Data": mov["data"].strftime("%d/%m/%Y %H:%M"),
                    "Tipo": mov["tipo"],
                    "Valor": mov["valor"],
                    "Descrição": mov["descricao"]
                })
            
            df = pd.DataFrame(dados)
            
            # Exportar para Excel
            if not os.path.exists("relatorios"):
                os.makedirs("relatorios")
            df.to_excel("relatorios/relatorio_financeiro.xlsx", index=False)
            
            messagebox.showinfo("Sucesso", "Relatório financeiro exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceiroManager(root)
    root.mainloop() 