from oracle_queries import OracleQueries
from mongo_connection import MongoConnection


def migrar_tudo_para_mongo():
    oracle = OracleQueries()
    mongo = MongoConnection().get_db()

    print("\n=== Migrando dados do Oracle → MongoDB ===\n")


    # MIGRAR CATEGORIAS

    categorias, colunas = oracle.sqlToMatrix(
        "SELECT id, nome, descricao FROM categorias"
    )

    categorias = categorias or []

    for c in categorias:
        mongo.categorias.update_one(
            {"id": c[0]},
            {"$set": {
                "id": c[0],
                "nome": c[1],
                "descricao": c[2]
            }},
            upsert=True
        )

    print(f"[OK] Categorias migradas: {len(categorias)}")

    # MIGRAR VEÍCULOS
 
    veiculos, colunas = oracle.sqlToMatrix(
        """
        SELECT id, placa, modelo, marca, ano, cor, status,
               kilometragem, categoria_id
        FROM veiculos
        """
    )

    veiculos = veiculos or []

    for v in veiculos:
        mongo.veiculos.update_one(
            {"id": v[0]},
            {"$set": {
                "id": v[0],
                "placa": v[1],
                "modelo": v[2],
                "marca": v[3],
                "ano": v[4],
                "cor": v[5],
                "status": v[6],
                "kilometragem": v[7],
                "categoria_id": v[8]
            }},
            upsert=True
        )

    print(f"[OK] Veículos migrados: {len(veiculos)}")

    # MIGRAR LOCAÇÕES

    locacoes, colunas = oracle.sqlToMatrix(
        """
        SELECT id, veiculo_id, cliente,
               TO_CHAR(data_retirada,'YYYY-MM-DD'),
               TO_CHAR(data_devolucao_prevista,'YYYY-MM-DD'),
               TO_CHAR(data_devolucao_real,'YYYY-MM-DD'),
               valor_diario, total, status
        FROM locacoes
        """
    )

    locacoes = locacoes or []

    for l in locacoes:
        mongo.locacoes.update_one(
            {"id": l[0]},
            {"$set": {
                "id": l[0],
                "veiculo_id": l[1],
                "cliente": l[2],
                "data_retirada": l[3],
                "data_devolucao_prevista": l[4],
                "data_devolucao_real": l[5] if l[5] else None,
                "valor_diario": l[6],
                "total": l[7],
                "status": l[8]
            }},
            upsert=True
        )

    print(f"[OK] Locações migradas: {len(locacoes)}")

    print("\n=== Migração concluída com sucesso! ===")


migrar_tudo_para_mongo()
