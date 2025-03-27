import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from employee import EmployeeManagementApp
from supplier import SupplierClass
from category import CategoryClass
from products import ProductManager
from sales import SalesClass
from billing import POS
from financeiro import FinanceiroManager
from fidelidade import FidelidadeManager
from dashboard_avancado import DashboardAvancado
from analise_avancada import AnaliseAvancada
from suporte import SuporteManager
import pymongo
import hashlib
from datetime import datetime

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Sistema De Gestão")
        self.root.config(bg="white")
        
        # Conexão com MongoDB
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["estoque"]
            self.users = self.db["usuarios"]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(e)}")
            return

        # ==== Title ====
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Sistema de Gestão", image=self.icon_title, compound=LEFT, 
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # ==== Botão Logout ====
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"), 
                            bg="yellow", cursor="hand2", command=self.logout)
        btn_logout.place(x=1150, y=10, height=50, width=150)

        # ==== Tempo ====
        self.lbl_clock = Label(self.root, 
                       text="Bem-vindo ao Sistema de Gestão\t | Data: DD-MM-YYYY\t | Hora: HH:MM:SS", 
                       font=("times new roman", 15, "bold"), 
                       bg="#4d636d", fg="white", anchor="w")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        
        # ==== Menu esquerdo ====
        lefMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        lefMenu.place(x=0, y=102, width=200, height=665)

        # ==== Ajuste correto da imagem no menu ====
        menu_img_path = "images/menu_im.png"
        if os.path.exists(menu_img_path):
            self.MenuLogo = Image.open(menu_img_path)
            self.MenuLogo = self.MenuLogo.resize((100, 100), Image.Resampling.LANCZOS)
            self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
            lbl_menuLogo = Label(lefMenu, image=self.MenuLogo, bg="white")
            lbl_menuLogo.pack(side=TOP, fill=X)
        else:
            lbl_menuLogo = Label(lefMenu, text="Imagem não encontrada!", fg="red", bg="white")
            lbl_menuLogo.pack(side=TOP, fill=X)

        # ==== Menu ====
        lbl_menu = Label(lefMenu, text="Menu", font=("times new roman", 15, "bold"), bg="#009688", fg="white")
        lbl_menu.pack(side=TOP, fill=X)

        # ==== Ícone dos botões ====
        self.icon_menu = PhotoImage(file="images/side.png")

        # ==== Botões do Menu ====
        btn_employee = Button(lefMenu, text="  Employee", command=self.employee, image=self.icon_menu, compound=LEFT, padx=5,
                              font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_employee.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_supplier = Button(lefMenu, text="  Supplier", command=self.supplier, image=self.icon_menu, compound=LEFT, padx=5,
                              font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_supplier.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_category = Button(lefMenu, text="  Category", command=self.category, image=self.icon_menu, compound=LEFT, padx=5,
                              font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_category.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_products = Button(lefMenu, text="  Products", command=self.products, image=self.icon_menu, compound=LEFT, padx=5,
                              font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_products.pack(side=TOP, fill=X, pady=2, padx=5)
        
        btn_billing = Button(lefMenu, text="  Billing", command=self.billing, image=self.icon_menu, compound=LEFT, padx=5,
                          font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_billing.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_sales = Button(lefMenu, text="  Sales", command=self.sales, image=self.icon_menu, compound=LEFT, padx=5,
                           font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_sales.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_financeiro = Button(lefMenu, text="  Financeiro", command=self.financeiro, image=self.icon_menu, compound=LEFT, padx=5,
                           font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_financeiro.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_fidelidade = Button(lefMenu, text="  Fidelidade", command=self.fidelidade, image=self.icon_menu, compound=LEFT, padx=5,
                           font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_fidelidade.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_dashboard_avancado = Button(lefMenu, text="  Dashboard Avançado", command=self.dashboard_avancado, image=self.icon_menu, compound=LEFT, padx=5,
                           font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_dashboard_avancado.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_analise = Button(lefMenu, text="  Análise Avançada", command=self.analise_avancada, image=self.icon_menu, compound=LEFT, padx=5,
                           font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_analise.pack(side=TOP, fill=X, pady=2, padx=5)

        btn_suporte = Button(lefMenu, text="  Suporte", command=self.suporte, image=self.icon_menu, compound=LEFT, padx=5,
                           font=("times new roman", 12, "bold"), bg="white", bd=2, cursor="hand2", height=35)
        btn_suporte.pack(side=TOP, fill=X, pady=2, padx=5)

        # === Conteúdo ===
        self.lbl_employee = Label(self.root, text="Total Employee\n [ 0 ]", 
                                  bd=5, relief=RIDGE, bg="#33bbf9", fg="white", 
                                  font=("Times New Roman", 20, "bold"))
        self.lbl_employee.place(x=300, y=100, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n [ 0 ]", 
                                  bd=5, relief=RIDGE, bg="#ffcc00", fg="white", 
                                  font=("Times New Roman", 20, "bold"))
        self.lbl_supplier.place(x=650, y=100, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n [ 0 ]", 
                                  bd=5, relief=RIDGE, bg="#ff5733", fg="white", 
                                  font=("Times New Roman", 20, "bold"))
        self.lbl_category.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n [ 0 ]", 
                               bd=5, relief=RIDGE, bg="#33bb77", fg="white", 
                               font=("Times New Roman", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # Sistema de Login
        self.login_window()

    def login_window(self):
        self.root.withdraw()
        self.login_win = Toplevel()
        self.login_win.geometry("400x300+500+200")
        self.login_win.title("Login")

        Label(self.login_win, text="Usuário:").pack(pady=10)
        self.username = Entry(self.login_win)
        self.username.pack(pady=5)

        Label(self.login_win, text="Senha:").pack(pady=10)
        self.password = Entry(self.login_win, show="*")
        self.password.pack(pady=5)

        Button(self.login_win, text="Entrar", command=self.validate_login).pack(pady=20)

    def validate_login(self):
        username = self.username.get()
        password = self.password.get()
        
        if username == "Leo" and password == "123":
            self.login_win.destroy()
            self.root.deiconify()
            self.current_user = {"username": "Leo"}
            self.update_welcome_message()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
    
    def update_welcome_message(self):
        welcome_text = f"Bem-vindo, {self.current_user['username']} | Data: {datetime.now().strftime('%d-%m-%Y')} | Hora: {datetime.now().strftime('%H:%M:%S')}"
        self.lbl_clock.config(text=welcome_text)

    def logout(self):
        if messagebox.askyesno("Logout", "Você deseja realmente encerrar o sistema?"):
            os._exit(0)

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeManagementApp(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_win)

    def products(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductManager(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SalesClass(self.new_win)
        
    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = POS(self.new_win)    

    def financeiro(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = FinanceiroManager(self.new_win)

    def fidelidade(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = FidelidadeManager(self.new_win)

    def dashboard_avancado(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = DashboardAvancado(self.new_win)

    def analise_avancada(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = AnaliseAvancada(self.new_win)

    def suporte(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SuporteManager(self.new_win)

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
