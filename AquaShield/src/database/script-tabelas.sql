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


CREATE TABLE componente(
idComponente INT PRIMARY KEY AUTO_INCREMENT,
nomeComponente VARCHAR(50),
unidadeMedida VARCHAR(100)
);

CREATE TABLE registro(
idRegistro INT PRIMARY KEY AUTO_INCREMENT,
fkMaquina INT,
fkComponente INT,
valorCaptura VARCHAR(500),
valorMaximo VARCHAR(100),
dtHora DATETIME DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT fkMaquinaEmpresaRegistro FOREIGN KEY (fkMaquina) REFERENCES maquina(idMaquina),
CONSTRAINT fkComponente FOREIGN KEY (fkComponente) REFERENCES Componente(idComponente)
);

CREATE TABLE alertas (
    idAlertas INT PRIMARY KEY AUTO_INCREMENT,
    fkMaquina INT,
    fkComponente INT,
    descricao VARCHAR(100),
    nivel VARCHAR(45),
    dtHora DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fkAlertasMaquina FOREIGN KEY (fkMaquina) REFERENCES maquina(idMaquina),
    CONSTRAINT fkAlertasComponente FOREIGN KEY (fkComponente) REFERENCES componente(idComponente)
);

