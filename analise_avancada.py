import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import calendar
import seaborn as sns

class AnaliseAvancada:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise Avançada")
        self.root.geometry("1400x900")
        self.root.config(bg="#f0f0f0")
        
        # Conexão com MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["estoque"]
        self.vendas = self.db["vendas"]
        self.produtos = self.db["produtos"]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = tk.Label(main_frame, text="Análise Avançada", 
                        font=("Arial", 24, "bold"), bg="#f0f0f0")
        title.pack(pady=10)
        
        # Frame para Controles
        controls_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Botões de Controle
        btn_sazonalidade = tk.Button(controls_frame, text="Análise Sazonal",
                                   command=self.mostrar_sazonalidade,
                                   font=("Arial", 12), bg="#4CAF50", fg="white")
        btn_sazonalidade.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_relatorio = tk.Button(controls_frame, text="Gerar Relatório",
                                command=self.gerar_relatorio,
                                font=("Arial", 12), bg="#2196F3", fg="white")
        btn_relatorio.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_categorias = tk.Button(controls_frame, text="Análise por Categoria",
                                 command=self.analise_categorias,
                                 font=("Arial", 12), bg="#FF9800", fg="white")
        btn_categorias.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Frame para Gráficos
        self.graphs_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
        self.graphs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def mostrar_sazonalidade(self):
        # Limpar frame de gráficos
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
            
        # Criar figura para análise sazonal
        fig = plt.Figure(figsize=(12, 8))
        
        # Coletar dados de vendas por mês
        vendas_por_mes = {}
        for venda in self.vendas.find():
            data = venda.get("data")
            if data:
                mes = data.month
                total = float(venda.get("total", 0))
                vendas_por_mes[mes] = vendas_por_mes.get(mes, 0) + total
        
        # Criar gráfico
        ax = fig.add_subplot(111)
        meses = list(calendar.month_abbr)[1:]
        valores = [vendas_por_mes.get(i, 0) for i in range(1, 13)]
        
        ax.bar(meses, valores)
        ax.set_title("Vendas por Mês")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Total de Vendas (R$)")
        plt.setp(ax.get_xticklabels(), rotation=45)
        
        # Adicionar canvas ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def gerar_relatorio(self):
        try:
            # Criar DataFrame com dados de vendas
            vendas_data = []
            for venda in self.vendas.find():
                vendas_data.append({
                    'Data': venda.get('data', ''),
                    'Total': float(venda.get('total', 0)),
                    'Itens': len(venda.get('itens', [])),
                    'Cliente': venda.get('cliente', '')
                })
            
            df = pd.DataFrame(vendas_data)
            
            # Gerar relatório PDF
            doc = SimpleDocTemplate("relatorio_vendas.pdf", pagesize=letter)
            elements = []
            
            # Título
            styles = getSampleStyleSheet()
            elements.append(Paragraph("Relatório de Vendas", styles['Title']))
            
            # Tabela de resumo
            data = [
                ['Métrica', 'Valor'],
                ['Total de Vendas', f"R$ {df['Total'].sum():.2f}"],
                ['Média por Venda', f"R$ {df['Total'].mean():.2f}"],
                ['Número de Vendas', len(df)],
                ['Total de Itens Vendidos', df['Itens'].sum()]
            ]
            
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(t)
            
            # Gerar PDF
            doc.build(elements)
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def analise_categorias(self):
        # Limpar frame de gráficos
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
        
        # Criar figura para análise por categoria
        fig = plt.Figure(figsize=(12, 8))
        
        # Coletar dados de vendas por categoria
        vendas_categoria = {}
        for venda in self.vendas.find():
            for item in venda.get("itens", []):
                try:
                    produto = self.produtos.find_one({"nome": item[0]})
                    if produto:
                        categoria = produto.get("categoria", "Sem Categoria")
                        quantidade = int(item[2])
                        valor = float(item[1]) * quantidade
                        vendas_categoria[categoria] = vendas_categoria.get(categoria, 0) + valor
                except Exception as e:
                    print(f"Erro ao processar item: {e}")
                    continue
        
        # Criar gráfico
        ax = fig.add_subplot(111)
        categorias = list(vendas_categoria.keys())
        valores = list(vendas_categoria.values())
        
        # Gráfico de pizza
        ax.pie(valores, labels=categorias, autopct='%1.1f%%')
        ax.set_title("Vendas por Categoria")
        
        # Adicionar canvas ao frame
        canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnaliseAvancada(root)
    root.mainloop() 