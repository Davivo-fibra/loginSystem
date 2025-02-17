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
    homePage.pack_forget()  
    registerPage.pack() 

def go_to_login_page():
    homePage.pack_forget() 
    loginPage.pack()

def go_back_to_home():
    registerPage.pack_forget()  
    loginPage.pack_forget() 
    homePage.pack()  

def create_account():
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

homePage = tk.Frame(root)
homePage.pack()

button_register = tk.Button(homePage, text="Cadastro", command=go_to_register_page)
button_register.pack(pady=10)

button_login = tk.Button(homePage, text="Login", command=go_to_login_page)
button_login.pack(pady=10)

registerPage = tk.Frame(root)

label_name = tk.Label(registerPage, text="Nome:")
label_name.pack(pady=5)
entry_name = tk.Entry(registerPage)
entry_name.pack(pady=5)

label_email = tk.Label(registerPage, text="Email:")
label_email.pack(pady=5)
entry_email = tk.Entry(registerPage)
entry_email.pack(pady=5)

label_password = tk.Label(registerPage, text="Senha:")
label_password.pack(pady=5)
entry_password = tk.Entry(registerPage, show="*")
entry_password.pack(pady=5)

button_create_account = tk.Button(registerPage, text="Criar Cadastro", command=create_account)
button_create_account.pack(pady=10)



button_back_to_home_from_register = tk.Button(registerPage, text="Voltar para a Página Inicial", command=go_back_to_home)
button_back_to_home_from_register.pack(pady=10)

loginPage = tk.Frame(root)

label_login_name = tk.Label(loginPage, text="Nome:")
label_login_name.pack(pady=5)
entry_login_name = tk.Entry(loginPage)
entry_login_name.pack(pady=5)

label_login_password = tk.Label(loginPage, text="Senha:")
label_login_password.pack(pady=5)
entry_login_password = tk.Entry(loginPage, show="*")
entry_login_password.pack(pady=5)

button_login_action = tk.Button(loginPage, text="Logar", command=login)
button_login_action.pack(pady=10)

button_back_to_home_from_login = tk.Button(loginPage, text="Voltar para a Página Inicial", command=go_back_to_home)
button_back_to_home_from_login.pack(pady=10)

root.mainloop()