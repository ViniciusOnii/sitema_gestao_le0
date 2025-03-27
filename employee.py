import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("900x600")  # Tamanho inicial da janela
        self.root.config(bg="#F4F4F9")
        
        # Variáveis de entrada
        self.emp_no = tk.StringVar()
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.address = tk.StringVar()
        self.gender = tk.StringVar()
        self.dob = tk.StringVar()
        self.contact_no = tk.StringVar()
        self.doj = tk.StringVar()
        self.password = tk.StringVar()
        self.user_type = tk.StringVar(value='Admin')
        self.salary = tk.StringVar()
        
        # Configuração do MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["employee_management"]
        self.collection = self.db["employees"]
        
        # Lista de campos: cada item é uma tupla (label, variável, is_combo)
        # Para campos do tipo combo, definimos True; caso contrário, False.
        self.fields = [
            ("Emp No", self.emp_no, False),
            ("Name", self.name, False),
            ("Email", self.email, False),
            ("Address", self.address, False),
            ("Gender", self.gender, True),
            ("D.O.B", self.dob, False),
            ("Contact No", self.contact_no, False),
            ("D.O.J", self.doj, False),
            ("Password", self.password, False),
            ("User Type", self.user_type, True),
            ("Salary", self.salary, False)
        ]
        
        self.create_widgets()
        self.update_treeview()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#F4F4F9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título centralizado
        title = tk.Label(main_frame, text="Employee Management", 
                         font=("Arial", 20, "bold"), bg="#F4F4F9")
        title.pack(pady=15)
        
        # Frame para os campos de entrada (estilo Bootstrap com 3 colunas por linha)
        fields_frame = tk.Frame(main_frame, bg="#F4F4F9")
        fields_frame.pack(fill=tk.X, pady=10)
        
        num_cols = 3
        num_fields = len(self.fields)
        num_rows = (num_fields + num_cols - 1) // num_cols  # Calcula quantas linhas serão necessárias
        
        field_index = 0
        for r in range(num_rows):
            row_frame = tk.Frame(fields_frame, bg="#F4F4F9")
            row_frame.pack(fill=tk.X, pady=5)
            # Cada linha terá até 3 colunas
            for c in range(num_cols):
                if field_index < num_fields:
                    label_text, var, is_combo = self.fields[field_index]
                    # Container para cada campo (coluna)
                    col_frame = tk.Frame(row_frame, bg="#F4F4F9")
                    col_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
                    
                    # Label do campo
                    tk.Label(col_frame, text=label_text, font=("Arial", 12), 
                             bg="#F4F4F9").pack(anchor="w")
                    
                    # Campo de entrada ou Combobox
                    if is_combo:
                        # Definindo os valores conforme o campo
                        values = ["Male", "Female"] if label_text == "Gender" else ["Admin", "Employee"]
                        ttk.Combobox(col_frame, textvariable=var, font=("Arial", 12),
                                     values=values, state="readonly").pack(fill=tk.X)
                    else:
                        tk.Entry(col_frame, textvariable=var, font=("Arial", 12)).pack(fill=tk.X)
                    
                    field_index += 1
        
        # Frame para os botões de ação
        button_frame = tk.Frame(main_frame, bg="#F4F4F9")
        button_frame.pack(pady=20)
        
        btn_texts = ["Save", "Update", "Delete", "Clear"]
        commands = [self.save_employee, self.update_employee, self.delete_employee, self.clear_fields]
        colors = ["#4CAF50", "#2196F3", "#F44336", "#FFC107"]
        
        for text, cmd, color in zip(btn_texts, commands, colors):
            tk.Button(button_frame, text=text, command=cmd, font=("Arial", 12, "bold"),
                      bg=color, fg="white").pack(side=tk.LEFT, padx=10)
        
        # Frame para a Treeview (tabela de dados)
        tree_frame = tk.Frame(main_frame, bg="#F4F4F9")
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = [field[0] for field in self.fields]
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.load_selected_employee)
    
    def save_employee(self):
        data = {
            "Emp No": self.emp_no.get(),
            "Name": self.name.get(),
            "Email": self.email.get(),
            "Address": self.address.get(),
            "Gender": self.gender.get(),
            "D.O.B": self.dob.get(),
            "Contact No": self.contact_no.get(),
            "D.O.J": self.doj.get(),
            "Password": self.password.get(),
            "User Type": self.user_type.get(),
            "Salary": self.salary.get()
        }
        self.collection.insert_one(data)
        self.update_treeview()
    
    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for employee in self.collection.find():
            values = (
                employee.get("Emp No", ""),
                employee.get("Name", ""),
                employee.get("Email", ""),
                employee.get("Address", ""),
                employee.get("Gender", ""),
                employee.get("D.O.B", ""),
                employee.get("Contact No", ""),
                employee.get("D.O.J", ""),
                employee.get("Password", ""),
                employee.get("User Type", ""),
                employee.get("Salary", "")
            )
            self.tree.insert("", tk.END, values=values)
    
    def update_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_emp_no = self.tree.item(selected_item)["values"][0]
            updated_data = {
                "Matrícula": self.emp_no.get(),
                "Nome": self.name.get(),
                "E-mail": self.email.get(),
                "Endereço": self.address.get(),
                "Sexo": self.gender.get(),
                "Dt. Nasc.": self.dob.get(),
                "Telefone": self.contact_no.get(),
                "Dt. Adm.": self.doj.get(),
                "Senha": self.password.get(),
                "Tipo de Usuário": self.user_type.get(),
                "Salário": self.salary.get()
            }
            self.collection.update_one({"Emp No": selected_emp_no}, {"$set": updated_data})
            self.update_treeview()
        else:
            messagebox.showwarning("Seleção", "Por favor, selecione um funcionário para atualizar.")
    
    def delete_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_emp_no = self.tree.item(selected_item)["values"][0]
            self.collection.delete_one({"Emp No": selected_emp_no})
            self.update_treeview()
        else:
            messagebox.showwarning("Seleção", "Por favor, selecione um funcionário para excluir.")
    
    def load_selected_employee(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            employee = self.tree.item(selected_item)["values"]
            self.emp_no.set(employee[0])
            self.name.set(employee[1])
            self.email.set(employee[2])
            self.address.set(employee[3])
            self.gender.set(employee[4])
            self.dob.set(employee[5])
            self.contact_no.set(employee[6])
            self.doj.set(employee[7])
            self.password.set(employee[8])
            self.user_type.set(employee[9])
            self.salary.set(employee[10])
    
    def clear_fields(self):
        for var in [self.emp_no, self.name, self.email, self.address, self.gender, 
                    self.dob, self.contact_no, self.doj, self.password, self.user_type, self.salary]:
            var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
