DROP DATABASE IF EXISTS aquashield;
CREATE DATABASE IF NOT EXISTS aquashield;
USE aquashield;

CREATE TABLE empresa (
    idEmpresa INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cnpj CHAR(14),
    email VARCHAR(50)
); 

CREATE TABLE cargo (
idCargo INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(50) NOT NULL
);

CREATE TABLE usuario (
idUsuario INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(50),
email VARCHAR(50),
senha VARCHAR(50),
fkCargo INT,
fkEmpresa INT,
CONSTRAINT fkUsuarioCargo FOREIGN KEY (fkCargo) REFERENCES cargo(idCargo),
CONSTRAINT fkUsuarioEmpresa FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa)
);

CREATE TABLE maquina(
idMaquina INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100),
fkEmpresa INT,
CONSTRAINT fkMaquinaEmpresa FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa));


CREATE TABLE processador(
 idProcessador INT PRIMARY KEY AUTO_INCREMENT,
 dtHora DATETIME DEFAULT CURRENT_TIMESTAMP,
 temperatura DECIMAL(3,1),
 frequencia DECIMAL(7,2),
 porcentagemUso DECIMAL(5,2),
 fkMaquina INT,
 CONSTRAINT fkProcessadorMaquina FOREIGN KEY (fkMaquina) REFERENCES Maquina(idMaquina)
 );
 
 
 CREATE TABLE memoria(
 idMemoria INT PRIMARY KEY AUTO_INCREMENT,
 dtHora DATETIME DEFAULT CURRENT_TIMESTAMP,
 memoria_usada INT,
 memoria_disponivel INT,
 fkMaquina INT,
 CONSTRAINT fkMemoriaMaquina FOREIGN KEY (fkMaquina) REFERENCES Maquina(idMaquina)
 
 );
 
 CREATE TABLE disco(
 idDisco INT PRIMARY KEY AUTO_INCREMENT,
 dtHora DATETIME DEFAULT CURRENT_TIMESTAMP,
 discoUso INT,
 espaçoLivre INT,
 fkMaquina INT,
 CONSTRAINT fkDiscoMaquina FOREIGN KEY (fkMaquina) REFERENCES Maquina(idMaquina)
 
 );
 
INSERT INTO cargo (idCargo,nome) VALUES
(1,"Técnico de Automação"),
(2,"Controlador de Sistemas De Saneamento")
