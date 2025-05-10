from faker import Faker
import pandas as pd
import random
import json
from datetime import datetime, timedelta

# ---------- Funções Utilitárias ----------

def carregar_json(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho} não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {caminho} está mal formatado.")
        return {}

# ---------- Função para Gerar Vendas ----------

def gerar_vendas(cliente, num_vendas_cliente, produtos, tipo_loja, data_inicio, data_fim, canal):
    vendas = []
    for _ in range(num_vendas_cliente):
        data = fake.date_between_dates(date_start=data_inicio, date_end=data_fim)
        produto = random.choice(produtos['produtos_categorizados'])  # Produto aleatório
        
        if tipo_loja == 'Online':
            product_id = next((p['ProductID'] for p in equivalencia_produtos if p['Nome_JSON'] == produto['nome']), None)
            venda = {
                'sale_id': f'S{cliente["customer_id"]}_{_+1}',
                'date': data.strftime('%Y-%m-%d'),
                'products': [{
                    'product_id': product_id,
                    'name': produto['nome'],
                    'category': produto['categoria'],
                    'price': round(random.uniform(20, 1500), 2),
                    'quantity': random.randint(1, 5),
                    'discount': random.randint(0, 50),
                }],
                'customer_id': cliente['customer_id'],
                'email': cliente['Email'],
                'district': cliente['Distrito'],
                'channel': canal
            }
        else:
            venda = {
                'Data_Venda': data.strftime('%d/%m/%Y'),
                'Produto': produto['nome'],
                'Categoria': produto['categoria'],
                'Quantidade': random.randint(1, 5),
                'Preço': round(random.uniform(20, 1500), 2),
                'Percentagem_Desconto': random.randint(0, 50),
                'Cliente_Nome': cliente['Nome'],
                'Concelho': cliente['Concelho'],
                'Canal': canal
            }
        vendas.append(venda)
    return vendas

# ---------- Introdução de Valores Nulos Aleatórios ----------

def inserir_nulls_vendas(vendas, percentual_nulos=0.05):
    # Limitar a quantidade de vendas com valores nulos
    num_vendas_total = len(vendas)
    num_vendas_nulas = int(num_vendas_total * percentual_nulos)  # Calculando o número de vendas com nulos
    vendas_com_nulos = random.sample(vendas, num_vendas_nulas)  # Seleciona aleatoriamente as vendas a afetar com nulos
    
    for venda in vendas_com_nulos:
        campos_possiveis = list(venda.keys())  # Obtendo todos os campos possíveis
        num_campos_a_anular = random.randint(1, len(campos_possiveis) // 2)  # Selecionar entre 1 e metade dos campos para serem nulos
        campos_a_anular = random.sample(campos_possiveis, num_campos_a_anular)  # Selecionando aleatoriamente os campos a anular

        for campo in campos_a_anular:
            venda[campo] = None  # Atribuindo None para o campo selecionado
    return vendas

# ---------- Carregamento de Dados ----------

produtos_categorizados_fisicos = carregar_json('dados/produtoscat_fisicos.json')
produtos_categorizados_online = carregar_json('dados/produtoscat_online.json')
equivalencia_produtos = carregar_json('dados/equivalencia_produtos.json')

# Inicializar Faker
fake = Faker('pt_PT')

# Carregar os dados de clientes gerados anteriormente
df_clientes = pd.read_csv('clientes.csv')

# Gerar Tabela de Equivalência de Clientes
equivalencia_clientes = df_clientes[['Nome', 'Profissão', 'EstadoCivil', 'Sexo', 'Distrito', 'Concelho', 'DataNascimento', 'Email']].copy()
equivalencia_clientes['customer_id'] = [f'C{i+100}' for i in range(len(df_clientes))]
equivalencia_clientes.to_csv('equivalencia_clientes.csv', index=False)

# 3. Gerar Tabela de Equivalência de Produtos (Atualizada com Todos os Produtos)
pd.DataFrame(equivalencia_produtos).to_csv('equivalencia_produtos.csv', index=False)

# 4. Gerar Registos da Loja Física com mais vendas por cliente (Fonte 1: Excel)
vendas_fisicas = []
for i in range(len(df_clientes)):  # Cada cliente tem entre 5 e 15 vendas
    cliente = equivalencia_clientes.iloc[i]
    num_vendas_cliente = random.randint(5, 15)
    vendas_fisicas.extend(gerar_vendas(cliente, num_vendas_cliente, produtos_categorizados_fisicos, 'Fisica', datetime(2010, 1, 1), datetime(2020, 12, 31), 'Loja Física'))

# ---------- Inserir valores nulos aleatoriamente nas vendas ----------

vendas_fisicas = inserir_nulls_vendas(vendas_fisicas, percentual_nulos=0.05)  # 5% de vendas com valores nulos

# Criar DataFrame e salvar
df_vendas_fisicas = pd.DataFrame(vendas_fisicas)
df_vendas_fisicas.to_excel('vendas_loja_fisica.xlsx', index=False)

# 5. Gerar Registos da Loja Online com mais vendas por cliente (Fonte 2: JSON)
vendas_online = []
for i in range(len(df_clientes)):  # Cada cliente tem entre 5 e 15 vendas
    cliente = equivalencia_clientes.iloc[i]
    num_vendas_cliente = random.randint(5, 15)
    vendas_online.extend(gerar_vendas(cliente, num_vendas_cliente, produtos_categorizados_online, 'Online', datetime(2021, 1, 1), datetime(2025, 4, 12), 'Online'))

# ---------- Inserir valores nulos aleatoriamente nas vendas ----------

vendas_online = inserir_nulls_vendas(vendas_online, percentual_nulos=0.05)  # 5% de vendas com valores nulos

# Salvar dados da loja online
with open('vendas_loja_online.json', 'w') as f:
    json.dump(vendas_online, f, indent=4)
