from flask_login import UserMixin
import mysql
import _mysql_connector as mysql
from werkzeug.security import generate_password_hash, check_password_hash


def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_tarefas"
    )

class User(UserMixin):
    _hash : str
    def __init__(self, **kwargs):
        self._id = None
        if 'email' in kwargs.keys():
            self._email = kwargs['email']
        if 'senha' in kwargs.keys():
            self._senha = kwargs['senha']
        if 'hash' in kwargs.keys():
            self._hash = kwargs['hash']
        if 'nome' in kwargs.keys():
            self._nome = kwargs['nome']
        if 'descricao' in kwargs.keys():
            self._descricao = kwargs['descricao']
        if 'situacao' in kwargs.keys():
            self._situacao = kwargs['situacao']
        if 'data_criacao' in kwargs.keys():
            self._data_criacao = kwargs['data_criacao']
        if 'prazo' in kwargs.keys():
            self._prazo = kwargs['prazo']
        if 'prioridade' in kwargs.keys():
            self._prioridade = kwargs['prioridade']
        if 'palavra_chave' in kwargs.keys():
            self._palavra_chave = kwargs['palavra_chave']
        if 'categoria' in kwargs.keys():
            self._categoria = kwargs['categoria']
        
    def get_id(self):
        return str(self._id)

    
    @property
    def _senha(self):
        return self._hash
    
    @_senha.setter
    def _senha(self, senha):
        self._hash = generate_password_hash(senha)

    
    def save(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO users(email, senha) VALUES (%s, %s)", (self._email, self._hash,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True
    
    def save_tarefas(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute ("INSERT INTO tarefas(nome, descricao, situacao, data_criacao, prazo, prioridade, palavra_chave, categoria) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (self.nome, self.descricao, self.situacao, self.data_criacao, self.prazo, self.prioridade, self.palavra_chave, self.categoria,))
        conn.commit()
        conn.close()
        return True
    
    def listar_tarefas(cls):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pecas")
        tarefas = conn.fetchall()
        conn.close()
        return tarefas
    
     
    def deletar_tarefas(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("DELETE FROM pecas WHERE id = %s", (id,))
        conn.close()
        return True
    
    """def all_favoritos(cls):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT livro, escritor FROM favoritos")
        favoritos = cursor.fetchall()
        conn.commit()
        conn.close()
        return favoritos"""
    
    @classmethod
    def get(cls,user_id):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user:
            loaduser = User(email=user['email'] , hash=user['senha'])
            loaduser._id = user['id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, email):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        if user:
            return True
        else:
            return False
    
    
    
    @classmethod
    def get_by_email(cls,email):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT id, email, senha FROM users WHERE email = %s", (email,))
        user = cursor.fetchone() 
        conn.commit()
        conn.close()
    
        return user
