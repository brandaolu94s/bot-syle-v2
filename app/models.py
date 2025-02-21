from config import Config
import pytz
from sqlalchemy import Text, Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

e = Config()
Base = declarative_base()


# ✅ SQLAlchemy Model (Database ORM)
class GuiaExame(Base):
    """
    SQLAlchemy ORM model for GuiaExame (Database table).
    """
    __tablename__ = 'GuiaExame'

    id = Column(Integer, primary_key=True, autoincrement=True)
    idsydle = Column(String, nullable=False)
    codigo_guia = Column(String(25))
    codigo_funcionario = Column(Integer, nullable=False)
    sequencial_pedido_exame = Column(String(25))
    empresa_socnet = Column(Boolean, default=False)
    codigo_empresa_principal = Column(Integer, nullable=False)
    codigo_empresa_cliente = Column(Integer, default=0)
    prestador_socnet = Column(Boolean, default=False)
    codigo_prestador = Column(Integer, nullable=False)
    tipo_exame = Column(Integer, nullable=False)
    exames = Column(String)
    pcd = Column(Boolean, default=False)
    data_exame = Column(String, nullable=False)
    hora_inicio = Column(String)
    hora_fim = Column(String)
    file_extension = Column(String(10))
    file_name = Column(String(255))
    file_content = Column(String)
    status_fila = Column(Integer, default=0)
    mensagem = Column(String(255))
    hora_processamento = Column(DateTime)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)


############################# DDL GUIA LOGS
#
#   CREATE TABLE GuiaLogs (
#    id INT PRIMARY KEY IDENTITY(1,1),
#    execution_id VARCHAR(255) NULL,
#    id_GuiaExame VARCHAR(255) NULL,
#    file_name VARCHAR(255) NOT NULL,
#    function_name VARCHAR(255) NOT NULL,
#    execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#    return_data NVARCHAR(MAX) -- JSONB is not supported in SQL Server, use NVARCHAR(MAX) to store JSON data
#    );
##############################


# Define ORM model
class GuiaLogs(Base):
    __tablename__ = e.LOG_TABLE
    id = Column(Integer, primary_key=True, autoincrement=True)
    execution_id = Column(String(255), nullable=True)
    id_GuiaExame = Column(String(255), nullable=True)
    file_name = Column(String(255), nullable=False)
    function_name = Column(String(255), nullable=False)
    execution_time = Column(DateTime, default=lambda: datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
    status = Column(String(50), nullable=True)
    message = Column(String(255), nullable=True)
    return_data = Column(Text, nullable=True)  # Storing JSON as text




