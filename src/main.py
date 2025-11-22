import os, sys
import time
from controller.categoria_controller import CategoriaController
from controller.veiculo_controller import VeiculoController
from controller.locacao_controller import LocacaoController
from reports.reports import Reports


def splash_oracle(dbq):
    counts = {}
    try:
        conn = dbq.connect()
        for t in ['categorias','veiculos','locacoes']:
            try:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT COUNT(1) FROM {t}")
                    counts[t] = cur.fetchone()[0]
            except Exception:
                counts[t] = 'N/A'
    except Exception as e:
        counts = {'categorias':'ERR','veiculos':'ERR','locacoes':'ERR'}
        print('Aviso: Oracle indisponível:', e)

    print('\n' + '='*100)
    print(' ' * 20 + '🏎 LOCADORA DE VEÍCULOS 🏎')
    print('='*100)
    print('Integrantes: Anderson Moreira, Gustavo Covre, Lucas Léllis, Mayara Hafez, Victor Alberto')
    print('-'*100)
    print(f" Registros atuais:")
    print(f"   Categorias: {counts.get('categorias')}")
    print(f"   Veículos:   {counts.get('veiculos')}")
    print(f"   Locações:   {counts.get('locacoes')}")
    print('-'*100)
    print("Professor: Howard Roatti  |  Disciplina: Banco de dados")
    print('='*100 + '\n')
    time.sleep(2)


def splash_mongo(db):
        print('\n' + '='*100)
        print(' ' * 20 + '🏎 LOCADORA DE VEÍCULOS 🏎')
        print('='*100)
        print('Integrantes: Anderson Moreira, Gustavo Covre, Lucas Léllis, Mayara Hafez, Victor Alberto')
        print('-'*100)
        print(f" Registros atuais:")
        print("Categorias:", db["categorias"].count_documents({}))
        print("Veículos:", db["veiculos"].count_documents({}))
        print("Locações:", db["locacoes"].count_documents({}))
        print('-'*100)
        print("Professor: Howard Roatti  |  Disciplina: Banco de dados")
        print('='*100 + '\n')
        time.sleep(2)


def pause():
    input('\nPressione Enter para continuar...')


def show_database_selection():
    print("\n=========== SELECIONE O BANCO DE DADOS ===========")
    print("1 - Oracle")
    print("2 - MongoDB")
    print("0 - Sair")
    return input("Opção: ").strip()


def show_menu():
    print('\n=== MENU PRINCIPAL ===')
    print('1 - Categorias')
    print('2 - Veículos')
    print('3 - Locações')
    print('4 - Relatórios')
    print('0 - Sair')

# ------------------- Menus de cadastro -------------------


def menu_categorias(db_type):
    c = CategoriaController(db_type=db_type)
    from model.categoria import Categoria
    while True:
        print('\n--- Categorias ---')
        print('1 - Listar')
        print('2 - Inserir')
        print('3 - Atualizar')
        print('4 - Excluir')
        print('0 - Voltar')
        op = input('Opção: ').strip()

        if op == '1':
            rows = c.list_all()
            for r in rows:
                print(r)
            pause()

        elif op == '2':
            nome = input('Nome: ')
            descricao = input('Descrição: ')
            cat = Categoria(nome=nome, descricao=descricao)
            c.insert(cat)
            print("Categoria inserida.")
            pause()

        elif op == '3':
            id = input('ID: ')
            nome = input('Novo nome: ')
            descricao = input('Nova descrição: ')
            c.update(id, nome, descricao)
            print("Atualizado.")
            pause()

        elif op == '4':
            id = input('ID: ')
            c.delete(id)
            print("Excluído.")
            pause()

        else:
            break


def menu_veiculos(db_type):
    c = VeiculoController(db_type=db_type)
    from model.veiculo import Veiculo

    while True:
        print("\n--- Veículos ---")
        print("1 - Listar")
        print("2 - Inserir")
        print("3 - Atualizar")
        print("4 - Excluir")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        if op == '1':
            rows = c.list_all()
            for r in rows:
                print(r)
            pause()

        elif op == '2':
            placa = input('Placa: ')
            modelo = input('Modelo: ')
            marca = input('Marca: ')
            ano = input('Ano: ')
            cor = input('Cor: ')
            km = float(input('KM: '))
            categoria_id = input("Categoria ID: ")

            v = Veiculo(
                placa=placa, modelo=modelo, marca=marca,
                ano=int(ano), cor=cor, kilometragem=km,
                categoria_id=int(categoria_id),
                status="disponível"
            )
            c.insert(v)
            print("Veículo inserido.")
            pause()

        elif op == '3':
            id = input("ID: ")
            print("Campos no formato campo=valor separados por vírgula")
            raw = input("Campos: ")

            kv = {}
            for part in raw.split(','):
                if '=' in part:
                    k, v = part.split('=')
                    kv[k.strip()] = v.strip()

            c.update(id, **kv)
            print("Atualizado.")
            pause()

        elif op == '4':
            id = input("ID: ")
            c.delete(id)
            print("Excluído.")
            pause()

        else:
            break


def menu_locacoes(db_type):
    c = LocacaoController(db_type=db_type)
    from model.locacao import Locacao

    while True:
        print("\n--- Locações ---")
        print("1 - Listar")
        print("2 - Inserir")
        print("3 - Atualizar")
        print("4 - Excluir")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        if op == '1':
            rows = c.list_all()
            for r in rows:
                print(r)
            pause()

        elif op == '2':
            veiculo_id = input("Veículo ID: ")
            cliente = input("Cliente: ")
            dr = input("Data retirada (YYYY-MM-DD): ")
            dp = input("Devolução prevista: ")
            vd = float(input("Valor diário: "))
            total = float(input("Total: "))

            loc = Locacao(
                veiculo_id=int(veiculo_id),
                cliente=cliente,
                data_retirada=dr,
                data_devolucao_prevista=dp,
                valor_diario=vd,
                total=total,
                status="ativa"
            )

            c.insert(loc)
            print("Locação inserida.")
            pause()

        elif op == '3':
            id = input("ID: ")
            raw = input("Campos a atualizar (campo=valor,...): ")

            kv = {}
            for part in raw.split(','):
                if '=' in part:
                    k, v = part.split('=')
                    kv[k.strip()] = v.strip()

            c.update(id, **kv)
            print("Atualizado.")
            pause()

        elif op == '4':
            id = input("ID: ")
            c.delete(id)
            print("Excluído.")
            pause()

        else:
            break


def menu_relatorios(db_type):
    r = Reports(db_type=db_type)
    while True:
        print("\n--- Relatórios ---")
        print("1 - Faturamento por categoria")
        print("2 - Locações + veículo")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        if op == '1':
            r.total_by_categoria()
            pause()
        elif op == '2':
            r.locacoes_with_veiculo()
            pause()
        else:
            break


# ------------------- Main -------------------

def main():

    while True:
        op = show_database_selection()

        if op == '1':
            db_type = "oracle"
            from utils.oracle_queries import OracleQueries
            dbq = OracleQueries()
            splash_oracle(dbq)

        elif op == '2':
            db_type = "mongo"
            from utils.mongo_connection import MongoConnection
            db = MongoConnection().get_db()
            splash_mongo(db)

        elif op == '0':
            print("Saindo...")
            break

        else:
            print("Opção inválida.")
            continue

        # menu principal
        while True:
            show_menu()
            op2 = input("Opção: ").strip()

            if op2 == '1':
                menu_categorias(db_type)
            elif op2 == '2':
                menu_veiculos(db_type)
            elif op2 == '3':
                menu_locacoes(db_type)
            elif op2 == '4':
                menu_relatorios(db_type)
            elif op2 == '0':
                break
            else:
                print("Opção inválida.")


if __name__ == "__main__":
    main()
