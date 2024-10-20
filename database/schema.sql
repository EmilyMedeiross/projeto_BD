CREATE DATABASE IF NOT EXISTS `db_taferas`;
USE `db_tarefas`;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    situacao TEXT NOT NULL,
    data_criacao DATE NOT NULL,
    prazo INT NOT NULL,
    prioridade TEXT NOT NULL,
    palavra_chave TEXT NOT NULL,
    categoria TEXT NOT NULL
);

