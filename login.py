import tkinter as tk
import psycopg2
import random
from tkinter import messagebox

# Informações de conexão com o banco de dados PostgreSQL
dbname = "LoginDB"
user = "davivo"
password = "davas"
host = "localhost"
port = "5432"

# Tenta estabelecer conexão com o banco de dados
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

# Funções para navegação entre as páginas
def go_to_register_page():
    """
    Função para ir para a página de registro, ocultando a página inicial.
    """
    home_page.pack_forget()  
    register_page.pack()

def go_to_login_page():
    """
    Função para ir para a página de login, ocultando a página inicial.
    """
    home_page.pack_forget() 
    login_page.pack()

def go_to_home_page():
    """
    Função para voltar para a página inicial, ocultando as páginas de registro e login.
    """
    register_page.pack_forget()  
    login_page.pack_forget() 
    home_page.pack()  

# Função para gerar um código aleatório
def generate_code():
    """
    Gera um código aleatório de 6 dígitos.
    """
    return ''.join(random.choices('0123456789', k=6))

# Função de registro, onde o usuário insere nome, email e senha
def register():
    """
    Função para realizar o registro de um novo usuário. Verifica se os campos não estão vazios e gera um código de verificação.
    """
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if name and email and password:
        global random_code
        random_code = generate_code()
        print(f"Código gerado: {random_code}") 
        label_code.pack(pady=5)
        entry_code.pack(pady=5)
        button_validate_code.pack(pady=10)
    else:
        messagebox.showerror("Erro", "Preencha todos os campos!")

# Função para validar o código gerado
def validate_code():
    """
    Valida o código inserido pelo usuário. Se estiver correto, realiza o cadastro no banco de dados.
    """
    user_code = entry_code.get()
    if user_code == random_code:
        name = entry_name.get()
        email = entry_email.get()
        password = entry_password.get()

        cursor = conn.cursor()
        cursor.execute("INSERT INTO register (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
        go_to_home_page()
    else:
        messagebox.showerror("Erro", "Código inválido!")

# Função de login, onde o usuário insere nome e senha para fazer login
def login():
    """
    Função para realizar o login do usuário. Verifica se as credenciais estão corretas no banco de dados.
    """
    name = entry_login_name.get()
    password = entry_login_password.get()

    if name and password:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM register WHERE name = %s AND password = %s", (name, password))
        user = cursor.fetchone() 
        cursor.close()
        
        if user:
            messagebox.showinfo("Login", f"Bem-vindo, {name}!")
            go_to_home_page()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha inválidos!")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos!")

# Inicializa a interface gráfica
root = tk.Tk()
root.title("Sistema de Cadastro e Login")
root.geometry("1000x600")

# Página inicial
home_page = tk.Frame(root)
home_page.pack()

# Botões de navegação para Cadastro e Login
button_register = tk.Button(home_page, text="Cadastro", command=go_to_register_page)
button_register.pack(pady=10)

button_login = tk.Button(home_page, text="Login", command=go_to_login_page)
button_login.pack(pady=10)

# Página de registro
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

# Botão para criar cadastro
button_register_action = tk.Button(register_page, text="Criar Cadastro", command=register)
button_register_action.pack(pady=10)

# Botão para voltar à página inicial
button_back_to_home_from_register = tk.Button(register_page, text="Voltar para a Página Inicial", command=go_to_home_page)
button_back_to_home_from_register.pack(pady=10)

# Campos de código para validação
label_code = tk.Label(register_page, text="Digite o código gerado no console:")
entry_code = tk.Entry(register_page)

# Botão para validar o código
button_validate_code = tk.Button(register_page, text="Validar Código", command=validate_code)

# Página de login
login_page = tk.Frame(root)

label_login_name = tk.Label(login_page, text="Nome:")
label_login_name.pack(pady=5)
entry_login_name = tk.Entry(login_page)
entry_login_name.pack(pady=5)

label_login_password = tk.Label(login_page, text="Senha:")
label_login_password.pack(pady=5)
entry_login_password = tk.Entry(login_page, show="*")
entry_login_password.pack(pady=5)

# Botão para login
button_login_action = tk.Button(login_page, text="Logar", command=login)
button_login_action.pack(pady=10)

# Botão para voltar à página inicial
button_back_to_home_from_login = tk.Button(login_page, text="Voltar para a Página Inicial", command=go_to_home_page)
button_back_to_home_from_login.pack(pady=10)

# Inicia o loop principal da interface
root.mainloop()
