import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

class DashboardAvancado:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Avançado")
        self.root.geometry("1400x900")
        self.root.config(bg="#f0f0f0")
        
        # Conexão com MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["estoque"]
        self.produtos = self.db["produtos"]
        self.vendas = self.db["vendas"]
        
        # Configurar interface
        self.setup_ui()
        self.atualizar_dashboard()
        
        # Atualizar a cada 5 minutos
        self.root.after(300000, self.atualizar_dashboard)
    
    def setup_ui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = tk.Label(main_frame, text="Dashboard Avançado", 
                        font=("Arial", 24, "bold"), bg="#f0f0f0")
        title.pack(pady=10)
        
        # Frame para KPIs
        kpis_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        kpis_frame.pack(fill=tk.X, pady=10)
        
        # KPIs
        self.kpi_labels = {}
        kpis = [
            ("Vendas Hoje", "R$ 0,00", "#4CAF50"),
            ("Ticket Médio", "R$ 0,00", "#2196F3"),
            ("Produtos Vendidos", "0", "#FF9800"),
            ("Clientes Atendidos", "0", "#9C27B0"),
            ("Taxa de Conversão", "0%", "#E91E63"),
            ("Margem de Lucro", "0%", "#00BCD4")
        ]
        
        for i, (title, value, color) in enumerate(kpis):
            frame = tk.Frame(kpis_frame, bg=color)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)
            
            tk.Label(frame, text=title, font=("Arial", 12, "bold"), 
                    bg=color, fg="white").pack()
            self.kpi_labels[title] = tk.Label(frame, text=value, 
                                            font=("Arial", 16, "bold"), 
                                            bg=color, fg="white")
            self.kpi_labels[title].pack()
        
        # Frame para Gráficos
        graphs_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        graphs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Gráfico de Vendas por Período
        self.fig_vendas = plt.Figure(figsize=(6, 4))
        self.canvas_vendas = FigureCanvasTkAgg(self.fig_vendas, master=graphs_frame)
        self.canvas_vendas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Gráfico de Produtos Mais Vendidos
        self.fig_produtos = plt.Figure(figsize=(6, 4))
        self.canvas_produtos = FigureCanvasTkAgg(self.fig_produtos, master=graphs_frame)
        self.canvas_produtos.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Frame para Previsão de Demanda
        previsao_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        previsao_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(previsao_frame, text="Previsão de Demanda", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        
        self.fig_previsao = plt.Figure(figsize=(12, 4))
        self.canvas_previsao = FigureCanvasTkAgg(self.fig_previsao, master=previsao_frame)
        self.canvas_previsao.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para Alertas
        alerts_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        alerts_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(alerts_frame, text="Alertas em Tempo Real", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        
        self.alerts_tree = ttk.Treeview(alerts_frame, 
                                      columns=("Data", "Tipo", "Produto", "Mensagem"), 
                                      show="headings")
        self.alerts_tree.heading("Data", text="Data")
        self.alerts_tree.heading("Tipo", text="Tipo")
        self.alerts_tree.heading("Produto", text="Produto")
        self.alerts_tree.heading("Mensagem", text="Mensagem")
        self.alerts_tree.pack(fill=tk.X, padx=5, pady=5)
    
    def atualizar_dashboard(self):
        try:
            # Atualizar KPIs
            self.atualizar_kpis()
            
            # Atualizar gráficos
            self.atualizar_grafico_vendas()
            self.atualizar_grafico_produtos()
            
            # Atualizar previsão
            self.atualizar_previsao()
            
            # Atualizar alertas
            self.atualizar_alertas()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard: {str(e)}")
    
    def atualizar_kpis(self):
        try:
            hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Vendas Hoje
            vendas_hoje = sum(float(v.get("total", 0)) for v in self.vendas.find({"data": {"$gte": hoje}}))
            self.kpi_labels["Vendas Hoje"].config(text=f"R$ {vendas_hoje:.2f}")
            
            # Ticket Médio
            total_vendas = sum(float(v.get("total", 0)) for v in self.vendas.find())
            num_vendas = self.vendas.count_documents({})
            ticket_medio = total_vendas / num_vendas if num_vendas > 0 else 0
            self.kpi_labels["Ticket Médio"].config(text=f"R$ {ticket_medio:.2f}")
            
            # Produtos Vendidos
            produtos_vendidos = 0
            for venda in self.vendas.find():
                try:
                    produtos_vendidos += len(venda.get("itens", []))
                except (TypeError, ValueError):
                    continue
            self.kpi_labels["Produtos Vendidos"].config(text=str(produtos_vendidos))
            
            # Clientes Atendidos
            clientes_unicos = len(self.vendas.distinct("cliente"))
            self.kpi_labels["Clientes Atendidos"].config(text=str(clientes_unicos))
            
            # Taxa de Conversão
            total_produtos = self.produtos.count_documents({})
            taxa_conversao = (produtos_vendidos / total_produtos * 100) if total_produtos > 0 else 0
            self.kpi_labels["Taxa de Conversão"].config(text=f"{taxa_conversao:.1f}%")
            
            # Margem de Lucro (exemplo: 30%)
            margem_lucro = 30.0  # Este valor deveria ser calculado com base nos custos
            self.kpi_labels["Margem de Lucro"].config(text=f"{margem_lucro:.1f}%")
            
        except Exception as e:
            print(f"Erro ao atualizar KPIs: {e}")
            # Em caso de erro, mostrar valores zerados
            self.kpi_labels["Vendas Hoje"].config(text="R$ 0,00")
            self.kpi_labels["Ticket Médio"].config(text="R$ 0,00")
            self.kpi_labels["Produtos Vendidos"].config(text="0")
            self.kpi_labels["Clientes Atendidos"].config(text="0")
            self.kpi_labels["Taxa de Conversão"].config(text="0,0%")
            self.kpi_labels["Margem de Lucro"].config(text="0,0%")
    
    def atualizar_grafico_vendas(self):
        try:
            self.fig_vendas.clear()
            ax = self.fig_vendas.add_subplot(111)
            
            # Buscar vendas dos últimos 30 dias
            datas = []
            valores = []
            for i in range(30):
                data = datetime.now() - timedelta(days=i)
                inicio_dia = data.replace(hour=0, minute=0, second=0, microsecond=0)
                fim_dia = data.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                vendas = self.vendas.find({"data": {"$gte": inicio_dia, "$lte": fim_dia}})
                total = sum(float(v.get("total", 0)) for v in vendas)
                
                datas.append(data.strftime("%d/%m"))
                valores.append(total)
            
            if valores:
                ax.plot(datas[::-1], valores[::-1], marker='o')
                ax.set_title("Vendas dos Últimos 30 Dias")
                ax.set_xlabel("Data")
                ax.set_ylabel("Valor (R$)")
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            else:
                ax.text(0.5, 0.5, "Sem dados de vendas", 
                       horizontalalignment='center', verticalalignment='center')
            
            self.canvas_vendas.draw()
        except Exception as e:
            print(f"Erro ao atualizar gráfico de vendas: {e}")
            self.fig_vendas.clear()
            ax = self.fig_vendas.add_subplot(111)
            ax.text(0.5, 0.5, "Erro ao carregar dados", 
                   horizontalalignment='center', verticalalignment='center')
            self.canvas_vendas.draw()
    
    def atualizar_grafico_produtos(self):
        self.fig_produtos.clear()
        ax = self.fig_produtos.add_subplot(111)
        
        # Buscar produtos mais vendidos
        produtos = {}
        for venda in self.vendas.find():
            try:
                for item in venda.get("itens", []):
                    try:
                        nome_produto = str(item[0])
                        # Garantir que quantidade seja um número inteiro
                        try:
                            quantidade = int(item[2])
                        except (ValueError, TypeError):
                            quantidade = 0
                            
                        if nome_produto not in produtos:
                            produtos[nome_produto] = 0
                        produtos[nome_produto] += quantidade
                    except (IndexError, TypeError) as e:
                        print(f"Erro ao processar item da venda: {e}")
                        continue
            except Exception as e:
                print(f"Erro ao processar venda: {e}")
                continue
        
        if produtos:
            # Ordenar por quantidade vendida
            produtos_ordenados = dict(sorted(produtos.items(), key=lambda x: x[1], reverse=True)[:10])
            
            ax.bar(produtos_ordenados.keys(), produtos_ordenados.values())
            ax.set_title("Top 10 Produtos Mais Vendidos")
            ax.set_xlabel("Produto")
            ax.set_ylabel("Quantidade")
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, "Sem dados de vendas", 
                   horizontalalignment='center', verticalalignment='center')
        
        self.canvas_produtos.draw()
    
    def atualizar_previsao(self):
        try:
            self.fig_previsao.clear()
            ax = self.fig_previsao.add_subplot(111)
            
            # Coletar dados históricos
            datas = []
            valores = []
            for i in range(90):  # 90 dias de histórico
                data = datetime.now() - timedelta(days=i)
                inicio_dia = data.replace(hour=0, minute=0, second=0, microsecond=0)
                fim_dia = data.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                vendas = self.vendas.find({"data": {"$gte": inicio_dia, "$lte": fim_dia}})
                total = sum(float(v.get("total", 0)) for v in vendas)
                
                datas.append(data)
                valores.append(total)
            
            if len(valores) > 1:  # Precisamos de pelo menos 2 pontos para fazer a regressão
                # Preparar dados para regressão
                X = np.array(range(len(datas))).reshape(-1, 1)
                y = np.array(valores)
                
                # Treinar modelo
                model = LinearRegression()
                model.fit(X, y)
                
                # Fazer previsão para os próximos 30 dias
                X_future = np.array(range(len(datas), len(datas) + 30)).reshape(-1, 1)
                y_pred = model.predict(X_future)
                
                # Plotar dados históricos e previsão
                ax.plot(datas[::-1], valores[::-1], label='Histórico', marker='o')
                datas_futuras = [datas[-1] + timedelta(days=i+1) for i in range(30)]
                ax.plot(datas_futuras, y_pred, label='Previsão', linestyle='--', color='red')
                
                ax.set_title("Previsão de Vendas para os Próximos 30 Dias")
                ax.set_xlabel("Data")
                ax.set_ylabel("Valor (R$)")
                ax.legend()
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            else:
                ax.text(0.5, 0.5, "Dados insuficientes para previsão", 
                       horizontalalignment='center', verticalalignment='center')
            
            self.canvas_previsao.draw()
        except Exception as e:
            print(f"Erro ao atualizar previsão: {e}")
            self.fig_previsao.clear()
            ax = self.fig_previsao.add_subplot(111)
            ax.text(0.5, 0.5, "Erro ao gerar previsão", 
                   horizontalalignment='center', verticalalignment='center')
            self.canvas_previsao.draw()
    
    def atualizar_alertas(self):
        try:
            self.alerts_tree.delete(*self.alerts_tree.get_children())
            
            # Verificar produtos com estoque baixo
            produtos_baixos = self.produtos.find({"quantidade": {"$lt": 10}})
            for produto in produtos_baixos:
                try:
                    self.alerts_tree.insert("", "end", values=(
                        datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Estoque Baixo",
                        produto.get("nome", "Produto sem nome"),
                        f"Quantidade atual: {produto.get('quantidade', 0)}"
                    ))
                except Exception as e:
                    print(f"Erro ao processar alerta de estoque baixo: {e}")
                    continue
            
            # Verificar produtos sem vendas recentes
            data_limite = datetime.now() - timedelta(days=30)
            produtos_sem_vendas = self.produtos.find()
            for produto in produtos_sem_vendas:
                try:
                    vendas_recentes = self.vendas.find({
                        "data": {"$gte": data_limite},
                        "itens.0": produto.get("nome", "")
                    })
                    if not list(vendas_recentes):
                        self.alerts_tree.insert("", "end", values=(
                            datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Sem Vendas Recentes",
                            produto.get("nome", "Produto sem nome"),
                            "Sem vendas nos últimos 30 dias"
                        ))
                except Exception as e:
                    print(f"Erro ao processar alerta de vendas recentes: {e}")
                    continue
        except Exception as e:
            print(f"Erro ao atualizar alertas: {e}")
            messagebox.showerror("Erro", "Não foi possível atualizar os alertas")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardAvancado(root)
    root.mainloop() 