import pymongo

def get_database():
    """Função para conectar ao MongoDB"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Conexão local
    db = client["employee_management"]  # Nome do banco de dados
    return db

def create_employee_collection():
    """Cria a coleção employees e insere um documento de teste"""
    db = get_database()

    # Criar um contador para auto-incremento (similar ao AUTO_INCREMENT do SQL)
    counters = db["counters"]
    if counters.count_documents({"_id": "eid"}, limit=1) == 0:
        counters.insert_one({"_id": "eid", "seq": 0})

    # Criar a coleção employees
    employees = db["employees"]

    # Inserir um documento de exemplo
    new_employee = {
        "eid": get_next_sequence("eid"),
        "name": "Teste",
        "email": "teste@email.com",
        "gender": "Masculino",
        "contact": "99999-9999",
        "dob": "1990-01-01",
        "doj": "2024-03-01",
        "pass": "senha123",
        "utype": "admin",
        "adress": "Rua Exemplo, 123",
        "salary": 5000
    }

    employees.insert_one(new_employee)
    print("Documento inserido com sucesso!")

def get_next_sequence(name):
    """Função para gerar um ID auto-incrementável"""
    db = get_database()
    result = db["counters"].find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return result["seq"]

if __name__ == "__main__":
    create_employee_collection()
