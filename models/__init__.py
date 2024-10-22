
from flask_login import UserMixin
import mysql
import mysql.connector 
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
        cursor.execute("INSERT INTO tb_users(use_email, use_senha) VALUES (%s, %s)", (self._email, self._hash,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True
    
    def save_tarefas(nome, descricao, situacao, data_criacao, prazo, prioridade, palavra_chave, categoria, use_id):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute ("INSERT INTO tb_tarefas(tar_nome, tar_descricao, tar_situacao, tar_data_criacao, tar_prazo, tar_prioridade, tar_palavra_chave, tar_categoria, tar_use_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %r)", (nome, descricao, situacao, data_criacao, prazo, prioridade, palavra_chave, categoria, use_id,))
        conn.commit()
        conn.close()
        return True

    def atualizar_tarefas(id_tar, descricao, situacao, data_criacao, prazo, prioridade, palavra_chave, categoria):
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)
        
        query = """
        UPDATE tb_tarefas
        SET tar_descricao = %s, tar_situacao = %s, 
            tar_data_criacao = %s, tar_prazo = %s, tar_prioridade = %s, 
            tar_palavra_chave = %s, tar_categoria = %s
        WHERE tar_id = %s;
        """
        valores = (descricao, situacao, 
               data_criacao, prazo, prioridade, 
               palavra_chave, categoria, id_tar)
        
        cursor.execute (query, valores)
        conn.commit()
        conn.close()
        return True
        
    @classmethod
    def listar_tarefas(cls):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_tarefas")
        tarefas = conn.fetchall()
        conn.close()
        return tarefas

    def deletar_tarefas(self):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("DELETE FROM tb_tarefas WHERE tar_id = %s", (self._id,))
        conn.close()
        return True
 
    @classmethod
    def get(cls, user_id):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_users WHERE use_id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user:
            loaduser = User(email=user['use_email'] , senha=user['use_senha'])
            loaduser._id = user['use_id']
            return loaduser
        else:
            return None
        
    
    @classmethod
    def exists(cls, email):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_users WHERE use_email = %s", (email,))
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        if user:
            return True
        else:
            return False
            
    @classmethod
    def get_by_email(cls, email):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT use_id, use_email, use_senha FROM tb_users WHERE use_email = %s", (email,))
        user = cursor.fetchone() 
        conn.commit()
        conn.close()
    
        return user
    
    
