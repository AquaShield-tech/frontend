DROP DATABASE IF EXISTS aquashield;
CREATE DATABASE IF NOT EXISTS aquashield;
USE aquashield;

CREATE TABLE empresa (
    idEmpresa INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cnpj CHAR(14),
    email VARCHAR(50)
); 

CREATE TABLE ETA(
idETA INT PRIMARY KEY AUTO_INCREMENT,
pais VARCHAR(100),
numero VARCHAR(150),
estado VARCHAR(100),
rua VARCHAR(50),
CEP CHAR(8),
fkEmpresa INT ,
CONSTRAINT fkETAempresa FOREIGN KEY(fkEmpresa) REFERENCES empresa(idEmpresa)
);

CREATE TABLE usuario (
idUsuario INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(50),
email VARCHAR(50),
senha VARCHAR(50),
cargo VARCHAR(100)NOT NULL CHECK (cargo IN ("Gestor", "Técnico", "Controlador")),
fkEmpresa INT,
fkETA INT,
CONSTRAINT fkUsuarioEmpresa FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa),
CONSTRAINT fkUsuarioETA FOREIGN KEY (fkETA) REFERENCES ETA(idETA)
);

CREATE TABLE maquina(
idMaquina INT PRIMARY KEY AUTO_INCREMENT,
numeracao VARCHAR(100),
IPMac CHAR(12),
fkEmpresa INT,
CONSTRAINT fkMaquinaEmpresa FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa));


CREATE TABLE Processador(
 id INT PRIMARY KEY AUTO_INCREMENT,
 temperatura DECIMAL(3,1),
 frequencia DECIMAL(7,2),
 porcentagem_de_uso DECIMAL(5,2),
 fkMaquina INT,
 fkEmpresa INT,
 CONSTRAINT fkMaquina FOREIGN KEY (fkMaquina) REFERENCES Maquina(idMaquina),
 CONSTRAINT fkEmpresa FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa));
 
 
 CREATE TABLE memoria(
 idMemoria INT PRIMARY KEY AUTO_INCREMENT,
 memoria_usada INT,
 memoria_disponivel INT,
 fkMaquina INT,
 fkEmpresa INT,
 CONSTRAINT fkMaquina FOREIGN KEY (fkMaquina) REFERENCES Maquina(idMaquina),
 CONSTRAINT fkEmpresa FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa)
 );
 
 CREATE TABLE disco(
 idDisco INT PRIMARY KEY AUTO_INCREMENT,
 discoUso INT,
 espaçoLivre INT,
 fkMaquina INT,
 fkEmpresa INT,
 CONSTRAINT fkMaquina FOREIGN KEY (fkMaquina) REFERENCES Maquina(idMaquina),
 CONSTRAINT fkEmpresa FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa)
 );
 
INSERT INTO cargo (id,nome) VALUES
(1,"Técnico de Automação"),
(2,"Controlador de Sistemas De Saneamento")
