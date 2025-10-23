
CREATE TABLE categorias (
    id INT PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    descricao VARCHAR2(400)
);

CREATE TABLE veiculos (
    id INT PRIMARY KEY,
    placa VARCHAR2(12) UNIQUE NOT NULL,
    modelo VARCHAR2(100) NOT NULL,
    marca VARCHAR2(100),
    ano NUMBER(4),
    cor VARCHAR2(50),
    status VARCHAR2(30) DEFAULT 'disponivel' NOT NULL,
    kilometragem INT(12,2) DEFAULT 0,
    categoria_id INT,
    CONSTRAINT fk_veiculo_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE locacoes (
    id INT PRIMARY KEY,
    veiculo_id INT NOT NULL,
    cliente VARCHAR2(200) NOT NULL,
    data_retirada DATE,
    data_devolucao_prevista DATE,
    data_devolucao_real DATE,
    valor_diario INT(12,2) DEFAULT 0,
    total INT(12,2),
    status VARCHAR2(30) DEFAULT 'ativa' NOT NULL,
    CONSTRAINT fk_locacao_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
);


CREATE INDEX idx_veiculo_marca_modelo ON veiculos(marca, modelo);
CREATE INDEX idx_locacao_status ON locacoes(status);


CREATE SEQUENCE seq_categorias START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_veiculos START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_locacoes START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_categorias_bi
BEFORE INSERT ON categorias
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
  SELECT seq_categorias.NEXTVAL INTO :NEW.id FROM dual;
END;


CREATE OR REPLACE TRIGGER trg_veiculos_bi
BEFORE INSERT ON veiculos
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
  SELECT seq_veiculos.NEXTVAL INTO :NEW.id FROM dual;
END;


CREATE OR REPLACE TRIGGER trg_locacoes_bi
BEFORE INSERT ON locacoes
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
  SELECT seq_locacoes.NEXTVAL INTO :NEW.id FROM dual;
END;


