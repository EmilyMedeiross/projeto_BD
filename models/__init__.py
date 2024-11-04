
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
        cursor.execute("INSERT INTO tb_users (use_email, use_senha) VALUES (%s, %s)", (self._email, self._hash,))
        teste = cursor.fetchone()
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        return True
    
    def save_tarefas(nome, descricao, situacao, data_criacao, prioridade, palavra_chave, categoria, use_id):        
        conn = obter_conexao()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute ("INSERT INTO tb_tarefas(tar_nome, tar_descricao, tar_situacao, tar_data_criacao, tar_prioridade, tar_palavra_chave, tar_categoria, tar_use_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (nome, descricao, situacao, data_criacao,  prioridade, palavra_chave, categoria, use_id,))
        conn.commit()
        conn.close()
        return True
        
    @classmethod
    def atualizar_tarefas(nome, descricao, situacao, data_criacao, prioridade, palavra_chave, categoria, tar_id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("UPDATE tb_tarefas SET tar_nome = %s, tar_descricao = %s, tar_situacao = %s, tar_data_criacao = %s, tar_prioridade = %s, tar_palavra_chave = %s, tar_categoria = %s WHERE tar_id = %s", 
                       (nome, descricao, situacao, data_criacao, prioridade, palavra_chave, categoria, tar_id))
            
        conn.commit()
        conn.close()
        return True
        
    @classmethod
    def atualizar_tarefas(cls, use_id, nome, descricao, situacao, data_criacao, prioridade, palavra_chave, categoria, tar_id):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)

        query = """
        UPDATE tb_tarefas
        SET tar_nome = %s, tar_descricao = %s, tar_situacao = %s,
            tar_data_criacao = %s, tar_prioridade = %s,
            tar_palavra_chave = %s, tar_categoria = %s
        WHERE tar_id = %s AND tar_use_id = %s;
        """
        valores = (nome, descricao, situacao,
                data_criacao, prioridade,
                palavra_chave, categoria, tar_id, use_id)

        cursor.execute(query, valores)
        conn.commit()
        conn.close()
        return True

    @classmethod
    def listar_tarefas(cls, use_id, filtros=None):
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM tb_tarefas WHERE tar_use_id = %s"
        params = [use_id]

        if filtros:
            if filtros.get('status'):
                query += " AND tar_situacao = %s"
                params.append(filtros['status'])
            if filtros.get('data_criacao'):
                query += " AND tar_data_criacao = %s"
                params.append(filtros['data_criacao'])
            if filtros.get('prioridade'):
                query += " AND tar_prioridade = %s"
                params.append(filtros['prioridade'])
            if filtros.get('palavra_chave'):
                query += " AND tar_palavra_chave LIKE %s"
                params.append(f"%{filtros['palavra_chave']}%")
            if filtros.get('categoria'):
                query += " AND tar_categoria = %s"
                params.append(filtros['categoria'])

        cursor.execute(query, params)
        tarefas = cursor.fetchall()
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
    
