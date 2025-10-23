import os, sys
import time
from controller.categoria_controller import CategoriaController
from controller.veiculo_controller import VeiculoController
from controller.locacao_controller import LocacaoController
from reports.reports import Reports
from utils.oracle_queries import OracleQueries


def splash(dbq):
    """Tela inicial com contagem de registros"""
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
        print(' Aviso: não foi possível conectar ao banco — verifique credenciais e se o Oracle está em execução.')
        print('Erro:', e)

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


def pause():
    input('\nPressione Enter para continuar...')


def show_menu():
    print('\n=== MENU PRINCIPAL ===')
    print('1 - Categorias')
    print('2 - Veículos')
    print('3 - Locações')
    print('4 - Relatórios')
    print('0 - Sair')


# ------------------- Menus de cadastro -------------------

def menu_categorias():
    c = CategoriaController(can_write=True)
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
            print('\nID | Nome | Descrição')
            print('-'*40)
            for r in rows:
                print(f"{r[0]} | {r[1]} | {r[2]}")
            pause()

        elif op == '2':
            while True:
                nome = input('Nome: ')
                descricao = input('Descrição: ')
                cat = Categoria(nome=nome, descricao=descricao)
                c.insert(cat)
                print('Categoria inserida com sucesso.\n')
                print('1 - Inserir outra')
                print('0 - Voltar')
                sub = input('Opção: ').strip()
                if sub != '1':
                    break

        elif op == '3':
            id = input('ID a atualizar: ')
            nome = input('Novo nome: ')
            descricao = input('Nova descrição: ')
            c.update(int(id), nome, descricao)
            print('Categoria atualizada.')
            pause()

        elif op == '4':
            while True:
                id = input('ID a excluir: ')
                c.delete(int(id))
                print('Categoria excluída com sucesso.\n')
                print('1 - Excluir outra')
                print('0 - Voltar')
                sub = input('Opção: ').strip()
                if sub != '1':
                    break
        else:
            break


def menu_veiculos():
    c = VeiculoController(can_write=True)
    from model.veiculo import Veiculo
    while True:
        print('\n--- Veículos ---')
        print('1 - Listar')
        print('2 - Inserir')
        print('3 - Atualizar (campos separados por vírgula)')
        print('4 - Excluir')
        print('0 - Voltar')
        op = input('Opção: ').strip()

        if op == '1':
            rows = c.list_all()
            print('\nID | Placa | Modelo | Marca | Ano | Cor | Status | KM | Categoria_ID')
            print('-'*70)
            for r in rows:
                print(" | ".join(str(i) for i in r))
            pause()

        elif op == '2':
            while True:
                placa = input('Placa: ')
                modelo = input('Modelo: ')
                marca = input('Marca: ')
                ano = input('Ano: ')
                cor = input('Cor: ')
                kilometragem = input('Kilometragem (decimal): ')
                categoria_id = input('Categoria ID (ou vazio): ')
                v = Veiculo(
                    placa=placa,
                    modelo=modelo,
                    marca=marca,
                    ano=int(ano) if ano else None,
                    cor=cor,
                    kilometragem=float(kilometragem) if kilometragem else 0.0,
                    categoria_id=int(categoria_id) if categoria_id else None,
                    status='disponível'
                )
                c.insert(v)
                print('Veículo inserido com sucesso.\n')
                print('1 - Inserir outro')
                print('0 - Voltar')
                sub = input('Opção: ').strip()
                if sub != '1':
                    break

        elif op == '3':
            id = input('ID a atualizar: ')
            print('Digite campos no formato campo=valor separados por vírgula (ex: cor=Azul,ano=2020)')
            raw = input('Campos: ')
            kvs = {}
            for part in raw.split(','):
                if '=' in part:
                    k, v = part.split('=', 1)
                    kvs[k.strip()] = v.strip()
            if 'ano' in kvs:
                kvs['ano'] = int(kvs['ano'])
            if 'kilometragem' in kvs:
                kvs['kilometragem'] = float(kvs['kilometragem'])
            c.update(int(id), **kvs)
            print('Veículo atualizado.')
            pause()

        elif op == '4':
            while True:
                id = input('ID a excluir: ')
                c.delete(int(id))
                print('Veículo excluído com sucesso.\n')
                print('1 - Excluir outro')
                print('0 - Voltar')
                sub = input('Opção: ').strip()
                if sub != '1':
                    break
        else:
            break


def menu_locacoes():
    c = LocacaoController(can_write=True)
    from model.locacao import Locacao
    while True:
        print('\n--- Locações ---')
        print('1 - Listar')
        print('2 - Inserir')
        print('3 - Atualizar')
        print('4 - Excluir')
        print('0 - Voltar')
        op = input('Opção: ').strip()

        if op == '1':
            rows = c.list_all()
            print('\nID | Veículo_ID | Cliente | Data Retirada | Data Devolução Prevista | Valor Diário | Total | Status')
            print('-'*90)
            for r in rows:
                print(" | ".join(str(i) if i is not None else "" for i in r))
            pause()

        elif op == '2':
            while True:
                veiculo_id = input('Veiculo ID: ')
                cliente = input('Cliente: ')
                data_retirada = input('Data retirada (YYYY-MM-DD): ')
                data_prev = input('Data devolução prevista (YYYY-MM-DD): ')
                valor_diario = input('Valor diário: ')
                total = input('Valor Total: ')
                l = Locacao(
                    veiculo_id=int(veiculo_id),
                    cliente=cliente,
                    data_retirada=data_retirada if data_retirada else None,
                    data_devolucao_prevista=data_prev if data_prev else None,
                    valor_diario=float(valor_diario) if valor_diario else 0.0,
                    total=float(total) if total else None,
                    status='ativa'
                )
                c.insert(l)
                print('Locação inserida com sucesso.\n')
                print('1 - Inserir outra')
                print('0 - Voltar')
                sub = input('Opção: ').strip()
                if sub != '1':
                    break

        elif op == '3':
            id = input('ID a atualizar: ')
            print('Digite campos no formato campo=valor separados por vírgula (ex: status=devolvida,total=200.0,data_retirada=2025-10-01)')
            raw = input('Campos: ')
            kvs = {}
            for part in raw.split(','):
                if '=' in part:
                    k, v = part.split('=', 1)
                    kvs[k.strip()] = v.strip()
            if 'valor_diario' in kvs:
                kvs['valor_diario'] = float(kvs['valor_diario'])
            if 'total' in kvs:
                kvs['total'] = float(kvs['total'])
            c.update(int(id), **kvs)
            print('Locação atualizada.')
            pause()

        elif op == '4':
            while True:
                id = input('ID a excluir: ')
                c.delete(int(id))
                print('Locação excluída com sucesso.\n')
                print('1 - Excluir outra')
                print('0 - Voltar')
                sub = input('Opção: ').strip()
                if sub != '1':
                    break
        else:
            break


# ------------------- Menu Relatórios -------------------

def menu_relatórios():
    r = Reports()
    while True:
        print('\n--- Relatórios ---')
        print('1 - Total faturado por categoria')
        print('2 - Locações com dados do veículo')
        print('0 - Voltar')
        op = input('Opção: ').strip()
        if op == '1':
            out = r.total_by_categoria()
            print(f'Relatório gerado: {out}')
            pause()
        elif op == '2':
            out = r.locacoes_with_veiculo()
            print(f'Relatório gerado: {out}')
            pause()
        else:
            break


# ------------------- Main -------------------

def main():
    cred_path = 'conexion/passphrase/authentication.oracle'
    if not os.path.exists(cred_path):
        print(f'Arquivo de credenciais não encontrado em {cred_path}')
        sys.exit(1)

    dbq = OracleQueries(can_write=False)
    splash(dbq)

    while True:
        show_menu()
        op = input('Opção: ').strip()
        if op == '1':
            menu_categorias()
        elif op == '2':
            menu_veiculos()
        elif op == '3':
            menu_locacoes()
        elif op == '4':
            menu_relatórios()
        elif op in ('0', ''):
            print('Saindo...')
            break
        else:
            print('Opção inválida.')


if __name__ == '__main__':
    main()
