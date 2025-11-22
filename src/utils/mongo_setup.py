from mongo_connection import MongoConnection

def criar_collections_mongo():
    conn= MongoConnection()
    db = conn.get_db()

    collections = ["categoria", "veiculo", "locacao"]

    existentes = db.list_collection_names()

    for col in collections:
        if col not in existentes:
            db.create_collection(col)
            print(f"Coleção criada no MongoDB: {col}")


criar_collections_mongo()