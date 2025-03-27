import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pymongo

class SuporteManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Suporte")
        self.root.geometry("1200x700")
        self.root.config(bg="#f0f0f0")
        
        # Conexão com MongoDB
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["estoque"]
            self.tickets = self.db["tickets"]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(e)}")
            return

        # Variáveis
        self.var_assunto = tk.StringVar()
        self.var_prioridade = tk.StringVar(value="Normal")
        self.var_categoria = tk.StringVar(value="Geral")
        self.var_status = tk.StringVar(value="Aberto")
        
        # Frame Principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = tk.Label(main_frame, text="Central de Suporte", 
                        font=("Arial", 24, "bold"), bg="#f0f0f0")
        title.pack(pady=10)
        
        # Frame para Novo Ticket
        ticket_frame = tk.LabelFrame(main_frame, text="Novo Ticket", 
                                   font=("Arial", 12, "bold"), bg="white")
        ticket_frame.pack(fill=tk.X, pady=10)
        
        # Campos do Ticket
        tk.Label(ticket_frame, text="Assunto:", font=("Arial", 12), bg="white").grid(
            row=0, column=0, padx=5, pady=5)
        tk.Entry(ticket_frame, textvariable=self.var_assunto, font=("Arial", 12), 
                width=50).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(ticket_frame, text="Prioridade:", font=("Arial", 12), bg="white").grid(
            row=0, column=2, padx=5, pady=5)
        ttk.Combobox(ticket_frame, textvariable=self.var_prioridade, 
                     values=["Baixa", "Normal", "Alta", "Urgente"], 
                     state="readonly", width=15).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(ticket_frame, text="Categoria:", font=("Arial", 12), bg="white").grid(
            row=1, column=0, padx=5, pady=5)
        ttk.Combobox(ticket_frame, textvariable=self.var_categoria, 
                     values=["Geral", "Vendas", "Estoque", "Financeiro", "Sistema", "Outros"], 
                     state="readonly", width=15).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(ticket_frame, text="Descrição:", font=("Arial", 12), bg="white").grid(
            row=2, column=0, padx=5, pady=5)
        self.txt_descricao = tk.Text(ticket_frame, font=("Arial", 12), width=70, height=5)
        self.txt_descricao.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
        # Botões
        btn_frame = tk.Frame(ticket_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Enviar Ticket", command=self.enviar_ticket,
                 font=("Arial", 12), bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Limpar", command=self.limpar_campos,
                 font=("Arial", 12), bg="#f44336", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        # Frame para Lista de Tickets
        list_frame = tk.LabelFrame(main_frame, text="Meus Tickets", 
                                 font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para tickets
        self.tree = ttk.Treeview(list_frame, 
                                columns=("id", "data", "assunto", "categoria", "prioridade", "status"),
                                show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("data", text="Data")
        self.tree.heading("assunto", text="Assunto")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("prioridade", text="Prioridade")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=100)
        self.tree.column("data", width=150)
        self.tree.column("assunto", width=300)
        self.tree.column("categoria", width=150)
        self.tree.column("prioridade", width=100)
        self.tree.column("status", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.ver_ticket)
        
        # Carregar tickets
        self.carregar_tickets()
        
    def enviar_ticket(self):
        if not self.var_assunto.get():
            messagebox.showwarning("Aviso", "Por favor, informe o assunto do ticket!")
            return
            
        if not self.txt_descricao.get("1.0", tk.END).strip():
            messagebox.showwarning("Aviso", "Por favor, descreva seu problema!")
            return
            
        try:
            ticket = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "data": datetime.now(),
                "assunto": self.var_assunto.get(),
                "categoria": self.var_categoria.get(),
                "prioridade": self.var_prioridade.get(),
                "status": "Aberto",
                "descricao": self.txt_descricao.get("1.0", tk.END).strip(),
                "respostas": []
            }
            
            self.tickets.insert_one(ticket)
            messagebox.showinfo("Sucesso", "Ticket enviado com sucesso!")
            self.limpar_campos()
            self.carregar_tickets()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar ticket: {str(e)}")
    
    def limpar_campos(self):
        self.var_assunto.set("")
        self.var_prioridade.set("Normal")
        self.var_categoria.set("Geral")
        self.txt_descricao.delete("1.0", tk.END)
    
    def carregar_tickets(self):
        try:
            # Limpar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Carregar tickets do MongoDB
            tickets = self.tickets.find().sort("data", -1)
            for ticket in tickets:
                self.tree.insert("", tk.END, values=(
                    ticket["id"],
                    ticket["data"].strftime("%d/%m/%Y %H:%M"),
                    ticket["assunto"],
                    ticket["categoria"],
                    ticket["prioridade"],
                    ticket["status"]
                ))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tickets: {str(e)}")
    
    def ver_ticket(self, event):
        try:
            item = self.tree.selection()[0]
            ticket_id = self.tree.item(item)["values"][0]
            
            # Buscar ticket no MongoDB
            ticket = self.tickets.find_one({"id": ticket_id})
            if ticket:
                # Criar nova janela para detalhes do ticket
                detalhes = tk.Toplevel(self.root)
                detalhes.title(f"Ticket #{ticket_id}")
                detalhes.geometry("800x600")
                
                # Frame principal
                frame = tk.Frame(detalhes, padx=20, pady=20)
                frame.pack(fill=tk.BOTH, expand=True)
                
                # Informações do ticket
                tk.Label(frame, text=f"Assunto: {ticket['assunto']}", 
                        font=("Arial", 12, "bold")).pack(anchor=tk.W)
                tk.Label(frame, text=f"Status: {ticket['status']}", 
                        font=("Arial", 12)).pack(anchor=tk.W)
                tk.Label(frame, text=f"Categoria: {ticket['categoria']}", 
                        font=("Arial", 12)).pack(anchor=tk.W)
                tk.Label(frame, text=f"Prioridade: {ticket['prioridade']}", 
                        font=("Arial", 12)).pack(anchor=tk.W)
                tk.Label(frame, text=f"Data: {ticket['data'].strftime('%d/%m/%Y %H:%M')}", 
                        font=("Arial", 12)).pack(anchor=tk.W)
                
                # Descrição
                tk.Label(frame, text="Descrição:", font=("Arial", 12, "bold")).pack(
                    anchor=tk.W, pady=(20,5))
                txt_desc = tk.Text(frame, font=("Arial", 12), height=5)
                txt_desc.insert("1.0", ticket["descricao"])
                txt_desc.config(state="disabled")
                txt_desc.pack(fill=tk.X)
                
                # Respostas
                tk.Label(frame, text="Respostas:", font=("Arial", 12, "bold")).pack(
                    anchor=tk.W, pady=(20,5))
                
                for resposta in ticket.get("respostas", []):
                    frame_resp = tk.Frame(frame, relief=tk.RIDGE, bd=1)
                    frame_resp.pack(fill=tk.X, pady=5)
                    
                    tk.Label(frame_resp, text=f"Data: {resposta['data'].strftime('%d/%m/%Y %H:%M')}", 
                            font=("Arial", 10)).pack(anchor=tk.W, padx=5)
                    tk.Label(frame_resp, text=resposta["texto"], 
                            font=("Arial", 11), wraplength=700).pack(padx=5, pady=5)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir ticket: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SuporteManager(root)
    root.mainloop() 