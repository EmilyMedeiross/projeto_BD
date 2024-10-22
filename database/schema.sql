CREATE DATABASE IF NOT EXISTS `db_tarefas`;
USE `db_tarefas`;

CREATE TABLE IF NOT EXISTS tb_users (
    use_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    use_email TEXT NOT NULL,
    use_senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_tarefas (
    tar_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    tar_nome TEXT NOT NULL,
    tar_descricao TEXT NOT NULL,
    tar_situacao TEXT NOT NULL,
    tar_data_criacao DATE NOT NULL,
    tar_prazo INT NOT NULL,
    tar_prioridade TEXT NOT NULL,
    tar_palavra_chave TEXT NOT NULL,
    tar_categoria TEXT NOT NULL
    FOREIGN KEY (tar_user_id) REFERENCES tb_users(user_id)
);

