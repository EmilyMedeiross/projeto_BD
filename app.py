from flask import Flask, redirect, render_template, url_for, request, flash
from models import User, obter_conexao
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

#from flask_mysqldb import MySQL

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
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
        confsenha = request.form['confsenha']

         # Verifica se a senha e a confirmação da senha são iguais
        if senha != confsenha:
            flash("As senhas não coincidem, por favor tente novamente.")
            return redirect(url_for('register'))

        if not User.exists(email):
            user = User(email=email, senha=senha)
            user.save()            
            # 6 - logar o usuário após cadatro
            login_user(user) 
            flash("Cadastro realizado com sucesso")
            return redirect(url_for('login'))
        
        else:
            flash("Usuário já existe. Tente novamente.")
            return redirect(url_for('register'))
        
    return render_template('pages/register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']   
        user = User.get_by_email(email)

        if user and check_password_hash(user['use_senha'], senha):
            login_user(User.get(user['use_id']))
            flash("Você está logado")
            return render_template('pages/criar_tarefa.html')
        
        else:
            flash("Dados incorretos")
            return redirect(url_for('login'))
    return render_template('pages/login.html')
             


@app.route('/criar_tarefa', methods=['GET', 'POST'])
@login_required
def criar_tarefa():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        situacao = request.form['status']
        data_criacao = request.form['prazo']
        prioridade = request.form['prioridade']
        palavra_chave = request.form['palavra_chave']
        categoria = request.form['categoria']
        use_id = current_user.get_id()

        User.save_tarefas(nome, descricao, situacao, data_criacao, prioridade, palavra_chave, categoria, use_id)

    tarefas = None
    if current_user.is_authenticated:
        tarefas = User.listar_tarefas(current_user.get_id())

    return render_template("pages/listar_tarefa.html", tarefas=tarefas)

@app.route('/atualizar_tarefa')
@app.route('/atualizar_tarefa/<int:tar_id>', methods=['GET', 'POST'])
def atualizar_tarefa(tar_id=none):

    if request.method == 'POST':

        nome = request.form['nome']
        descricao = request.form['descricao']
        situacao = request.form['status']
        data_criacao = request.form['data_criacao']
       # prazo = request.form['prazo']
        prioridade = request.form['prioridade']
        palavra_chave = request.form['palavra_chave']
        categoria = request.form['categoria']
        tarefas = User(tar_id, descricao, situacao, data_criacao, prioridade, palavra_chave, categoria)
        tarefas.atualizar_tarefas()

    return render_template("pages/atualizar_tarefa.html")


@app.route('/listar_tarefa', methods=['POST', 'GET'])
def listar_tarefa():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    tarefas = User.listar_tarefas(current_user.get_id())
    return render_template('pages/listar_tarefa.html', tarefas=tarefas)
   


@app.route('/deletar')
def deletar():
    if request.method == 'POST':
      tarefa = request.form['tarefa']
      tarefas = User(tarefa=tarefa)
      tarefas.deletar_tarefas
    return render_template("pages/deletar.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
