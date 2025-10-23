import json
import cx_Oracle
from pandas import DataFrame

class OracleQueries:
    def __init__(self, can_write: bool = False):
        """
        Inicializa a conexão com o Oracle. O parâmetro can_write define se
        a conexão pode executar operações de escrita.
        """
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1'
        self.conn = None

        # Lê usuário e senha do arquivo de autenticação
        try:
            with open("conexion/passphrase/authentication.oracle", "r") as f:
                content = f.read().strip()
                parts = [p.strip() for p in content.split(',')]
                if len(parts) >= 2:
                    self.user, self.passwd = parts[0], parts[1]
                else:
                    raise Exception(
                        "authentication.oracle must contain 'user,password' on a single line."
                    )
        except FileNotFoundError:
            raise Exception("Arquivo de autenticação não encontrado em 'conexion/passphrase/authentication.oracle'")

    def __del__(self):
        """Fecha a conexão ao destruir o objeto"""
        self.close()

    def connect(self):
        """Abre a conexão com o banco, se ainda não estiver aberta"""
        if self.conn is None:
            try:
                dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)
                self.conn = cx_Oracle.connect(user=self.user, password=self.passwd, dsn=dsn)
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                print(f"Erro ao conectar ao Oracle: {error.message}")
                raise
        return self.conn

    def sqlToDataFrame(self, query: str, params: dict = None) -> DataFrame:
        """Executa um SELECT e retorna um DataFrame"""
        conn = self.connect()
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            rows = cur.fetchall()
            columns = [col[0].lower() for col in cur.description]
        return DataFrame(rows, columns=columns)

    def sqlToMatrix(self, query: str, params: dict = None) -> tuple:
        """Executa um SELECT e retorna uma matriz e lista de colunas"""
        conn = self.connect()
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            rows = cur.fetchall()
            matrix = [list(row) for row in rows]
            columns = [col[0].lower() for col in cur.description]
        return matrix, columns

    def sqlToJson(self, query: str, params: dict = None) -> str:
        """Executa um SELECT e retorna o resultado em JSON"""
        conn = self.connect()
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            columns = [col[0].lower() for col in cur.description]
            cur.rowfactory = lambda *args: dict(zip(columns, args))
            rows = cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query: str, params: dict = None):
        """Executa uma operação de escrita (INSERT, UPDATE, DELETE)"""
        if not self.can_write:
            raise Exception("Can't write using this connection")
        conn = self.connect()
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
        conn.commit()

    def executeDDL(self, query: str, params: dict = None):
        """Executa comandos DDL (CREATE, ALTER, DROP)"""
        conn = self.connect()
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
        conn.commit()

    def close(self):
        """Fecha a conexão, se estiver aberta"""
        if getattr(self, 'conn', None):
            try:
                self.conn.close()
            except Exception:
                pass
            finally:
                self.conn = None
