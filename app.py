from flask import Flask, redirect, render_template, url_for, request, flash
from models import User, obter_conexao
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():    
    return render_template('pages/index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha'] 

        if not User.exists(email):
            user = User(email=email, senha=senha)
            user.save()            
            # 6 - logar o usuário após cadatro
            login_user(user) 
            flash("Cadastro realizado com sucesso")
            return redirect(url_for('login'))
    return render_template('pages/register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']   
        user = User.get_by_email(email)

        if user and check_password_hash(user['senha'], senha):
            login_user(User.get(user['id']))
            flash("Você está logado")
            return redirect(url_for('recomend'))
        
        else:
            flash("Dados incorretos")
            return redirect(url_for('login'))
    return render_template('pages/login.html')
             

@app.route('/criar_tarefa', methods=['GET', 'POST'])
def criar_tarefa():

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descriçao']
        situacao = request.form['status']
        data_criacao = request.form['data_criação']
        prazo = request.form['prazo']
        prioridade = request.form['prioridade']
        palavra_chave = request.form['palavra_chave']
        categoria = request.form['categoria']

        conn = conexao.connection.cursor()
        conn.execute ("INSERT INTO tarefas(nome, descricao, situacao, data_criacao, prazo, prioridade, palavra_chave, categoria) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (nome, descricao, situacao, data_criacao, prazo, prioridade, palavra_chave, categoria,))
        conexao.connection.commit()
        coenxao.connection.close()
    
    return render_template("pages/criar_tarefa.html")

@app.route('/atualizar_tarefa')
def atualizar_tarefa():
    return render_template("pages/atualizar_tarefa.html")

@app.route('/listar_tarefa')
def listar_tarefa():
    return render_template("pages/listar_tarefa.html")

# 8 - logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
