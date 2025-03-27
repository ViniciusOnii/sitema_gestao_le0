import os
import tkinter as tk
from tkinter import END, Scrollbar, messagebox

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Vendas")
        self.root.geometry("1000x800")

        # Frame para a Listbox e a Scrollbar
        frame_left = tk.Frame(self.root)
        frame_left.pack(side="left", padx=10, pady=10, fill="y")

        tk.Label(frame_left, text="Arquivos .txt:", font=("Arial", 12, "bold"), fg="blue").pack()

        # Listbox para exibir os arquivos
        self.Sales_List = tk.Listbox(frame_left, font=("Arial", 12), height=15, width=30)
        self.Sales_List.pack(side="left", fill="y")

        # Scrollbar para a Listbox
        scrollbar = Scrollbar(frame_left, command=self.Sales_List.yview)
        scrollbar.pack(side="right", fill="y")
        self.Sales_List.config(yscrollcommand=scrollbar.set)

        # Área de texto para mostrar o conteúdo do arquivo
        frame_right = tk.Frame(self.root)
        frame_right.pack(side="right", padx=10, pady=10, expand=True, fill="both")

        tk.Label(frame_right, text="Conteúdo do Arquivo:", font=("Arial", 12, "bold"), fg="green").pack()

        self.text_area = tk.Text(frame_right, font=("Arial", 12), height=15, width=40, wrap="word", bg="#f0f8ff")
        self.text_area.pack(expand=True, fill="both")

        # Botão para carregar arquivos
        btn_show = tk.Button(self.root, text="Carregar Arquivos", font=("Arial", 12), command=self.show)
        btn_show.pack(pady=5)

        # Campo de pesquisa
        self.search_entry = tk.Entry(self.root, font=("Arial", 12))
        self.search_entry.pack(pady=5)
        self.search_entry.insert(0, "Buscar arquivo...")
        self.search_entry.bind("<KeyRelease>", self.search_file)

        # Evento de clique na Listbox para carregar o conteúdo do arquivo
        self.Sales_List.bind("<<ListboxSelect>>", self.display_content)

        # Verificar se a pasta 'bill' existe ao iniciar
        self.check_folder()

    def check_folder(self):
        folder_path = "bill"
        if not os.path.exists(folder_path):
            if messagebox.askyesno("Pasta não encontrada", "A pasta 'bill' não existe. Deseja criá-la?"):
                os.makedirs(folder_path)
                messagebox.showinfo("Sucesso", "A pasta 'bill' foi criada com sucesso!")
            else:
                messagebox.showerror("Erro", "A pasta 'bill' é necessária para listar os arquivos.")

    def show(self):
        self.Sales_List.delete(0, END)
        folder_path = "bill"

        try:
            for file in os.listdir(folder_path):
                if file.lower().endswith(".txt"):
                    self.Sales_List.insert(END, file)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os arquivos: {str(e)}")

    def search_file(self, event):
        search_term = self.search_entry.get().lower()
        self.Sales_List.delete(0, END)

        folder_path = "bill"
        try:
            for file in os.listdir(folder_path):
                if file.lower().endswith(".txt") and search_term in file.lower():
                    self.Sales_List.insert(END, file)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar arquivos: {str(e)}")

    def display_content(self, event):
        selected_index = self.Sales_List.curselection()
        if not selected_index:
            return

        file_name = self.Sales_List.get(selected_index)
        file_path = os.path.join("bill", file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_area.delete("1.0", END)
            self.text_area.insert(END, content)
        except Exception as e:
            self.text_area.delete("1.0", END)
            self.text_area.insert(END, f"Erro ao abrir arquivo: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesClass(root)
    root.mainloop()
