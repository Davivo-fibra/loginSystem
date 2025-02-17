import tkinter as tk
import psycopg2
import random
from tkinter import messagebox

dbname = "LoginDB"
user = "davivo"
password = "davas"
host = "localhost"
port = "5432"
randomnumber=''.join(random.choices('0123456789', k=6))

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

def go_to_register_page():
    home_page.pack_forget()  
    register_page.pack() 

def go_to_login_page():
    home_page.pack_forget() 
    login_page.pack()

def go_back_to_home():
    register_page.pack_forget()  
    login_page.pack_forget() 
    home_page.pack()  

def register():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if name and email and password:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO register (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
        go_back_to_home()
        print(randomnumber)
    else:
        messagebox.showerror("Erro", "Preencha todos os campos!")

def login():
    name = entry_login_name.get()
    password = entry_login_password.get()

    if name and password:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM register WHERE name = %s AND password = %s", (name, password))
        user = cursor.fetchone() 
        cursor.close()
        
        if user:
            messagebox.showinfo("Login", f"Bem-vindo, {name}!")
            go_back_to_home()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha inválidos!")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos!")

root = tk.Tk()
root.title("Sistema de Cadastro e Login")
root.geometry("1000x600")

home_page = tk.Frame(root)
home_page.pack()

button_register = tk.Button(home_page, text="Cadastro", command=go_to_register_page)
button_register.pack(pady=10)

button_login = tk.Button(home_page, text="Login", command=go_to_login_page)
button_login.pack(pady=10)

register_page = tk.Frame(root)

label_name = tk.Label(register_page, text="Nome:")
label_name.pack(pady=5)
entry_name = tk.Entry(register_page)
entry_name.pack(pady=5)

label_email = tk.Label(register_page, text="Email:")
label_email.pack(pady=5)
entry_email = tk.Entry(register_page)
entry_email.pack(pady=5)

label_password = tk.Label(register_page, text="Senha:")
label_password.pack(pady=5)
entry_password = tk.Entry(register_page, show="*")
entry_password.pack(pady=5)

button_register = tk.Button(register_page, text="Criar Cadastro", command=register)
button_register.pack(pady=10)

button_back_to_home_from_register = tk.Button(register_page, text="Voltar para a Página Inicial", command=go_back_to_home)
button_back_to_home_from_register.pack(pady=10)

login_page = tk.Frame(root)

label_login_name = tk.Label(login_page, text="Nome:")
label_login_name.pack(pady=5)
entry_login_name = tk.Entry(login_page)
entry_login_name.pack(pady=5)

label_login_password = tk.Label(login_page, text="Senha:")
label_login_password.pack(pady=5)
entry_login_password = tk.Entry(login_page, show="*")
entry_login_password.pack(pady=5)

button_login_action = tk.Button(login_page, text="Logar", command=login)
button_login_action.pack(pady=10)

button_back_to_home_from_login = tk.Button(login_page, text="Voltar para a Página Inicial", command=go_back_to_home)
button_back_to_home_from_login.pack(pady=10)

root.mainloop()