import json
import random
import pandas as pd
from faker import Faker
from datetime import datetime

# ---------- Funções Utilitárias ----------

def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def gerar_email(nome, sobrenome, dominios, existentes):
    base = f"{nome}.{sobrenome}".lower()
    dominio = random.choice(dominios)
    email = f"{base}@{dominio}"
    while email in existentes:
        email = f"{base}{random.randint(1, 999)}@{dominio}"
    return email

def inserir_nulls_clientes(clientes, percentual_nulos=0.05):
    # Limitar a quantidade de clientes com valores nulos
    num_clientes_total = len(clientes)
    num_clientes_nulos = int(num_clientes_total * percentual_nulos)  # Calculando o número de clientes com nulos
    clientes_com_nulos = random.sample(clientes, num_clientes_nulos)  # Seleciona aleatoriamente os clientes a afetar com nulos
    
    for cliente in clientes_com_nulos:
        campos_possiveis = list(cliente.keys())  # Obtendo todos os campos possíveis
        num_campos_a_anular = random.randint(1, len(campos_possiveis) // 2)  # Selecionar entre 1 e metade dos campos para serem nulos
        campos_a_anular = random.sample(campos_possiveis, num_campos_a_anular)  # Selecionando aleatoriamente os campos a anular

        for campo in campos_a_anular:
            cliente[campo] = None  # Atribuindo None para o campo selecionado
    return clientes


# ---------- Carregamento de Dados ----------

distritos_concelhos = carregar_json('dados/distritos_concelhos.json')
dominios = carregar_json('dados/dominios_email.json')
profissoes = carregar_json('dados/profissoes.json')
estados_civis = carregar_json('dados/estados_civis.json')

# ---------- Configurações ----------

distrito_pesos = {
    'Braga': 0.20, 'Porto': 0.15, 'Viana do Castelo': 0.08, 'Vila Real': 0.06,
    'Aveiro': 0.06, 'Bragança': 0.05, 'Castelo Branco': 0.04, 'Coimbra': 0.05,
    'Évora': 0.03, 'Faro': 0.04, 'Guarda': 0.03, 'Leiria': 0.04, 'Lisboa': 0.05,
    'Portalegre': 0.02, 'Santarém': 0.03, 'Setúbal': 0.04, 'Viseu': 0.04, 'Beja': 0.03
}

distritos = list(distrito_pesos.keys())
fake = Faker('pt_PT')
data_atual = datetime(2025, 4, 12)

# ---------- Geração de Dados ----------

clientes = []
emails_gerados = set()

for _ in range(2000):
    distrito = random.choices(distritos, weights=[distrito_pesos[d] for d in distritos], k=1)[0]
    concelho = random.choice(distritos_concelhos[distrito])
    sexo = random.choice(['Masculino', 'Feminino'])
    nome_completo = fake.name_male() if sexo == 'Masculino' else fake.name_female()
    
    partes_nome = nome_completo.split()
    nome = partes_nome[0].lower()
    sobrenome = partes_nome[-1].lower() if len(partes_nome) > 1 else fake.last_name().lower()
    email = gerar_email(nome, sobrenome, dominios, emails_gerados)
    emails_gerados.add(email)

    profissao = random.choice(profissoes)

    # Regras de idade com base na profissão
    if profissao.lower() == 'estudante':
        if random.random() < 0.95:
            data_nascimento = fake.date_of_birth(minimum_age=16, maximum_age=23)
        else:
            data_nascimento = fake.date_of_birth(minimum_age=24, maximum_age=80)
    elif profissao.lower() == 'aposentado':
        if random.random() < 0.99:
            data_nascimento = fake.date_of_birth(minimum_age=60, maximum_age=80)
        else:
            data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=59)
    else:
        data_nascimento = fake.date_of_birth(minimum_age=20, maximum_age=59)

    # Correlações mais fortes entre variáveis para facilitar clustering
    # Por exemplo, relacionar estado civil com idade
    idade = (data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day)))
    
    if idade >= 65:  # Aposentados
        estado_civil_opcoes = ['Casado', 'Viúvo', 'Divorciado']
        estado_civil_pesos = [0.5, 0.35, 0.15]
    elif idade <= 23:  # Estudantes
        estado_civil_opcoes = ['Solteiro', 'Casado', 'Divorciado']
        estado_civil_pesos = [0.85, 0.1, 0.05]
    else:  # Outros
        estado_civil_opcoes = ['Solteiro', 'Casado', 'Divorciado', 'Viúvo']
        estado_civil_pesos = [0.40, 0.45, 0.10, 0.05]
    
    estado_civil = random.choices(estado_civil_opcoes, weights=estado_civil_pesos, k=1)[0]

    cliente = {
        'Nome': nome_completo,
        'Profissão': profissao,
        'EstadoCivil': estado_civil,
        'Sexo': sexo,
        'Distrito': distrito,
        'Concelho': concelho,
        'Telefone': fake.numerify('9########'),
        'Morada': fake.address(),
        'CódigoPostal': fake.postcode(),
        'DataNascimento': data_nascimento.strftime('%d/%m/%Y'),
        'Email': email
    }

    clientes.append(cliente)


# ---------- Exportação ----------

clientes = inserir_nulls_clientes(clientes, percentual_nulos=0.05)  # 5% de vendas com valores nulos


df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv('clientes.csv', index=False)
clientes_com_vazios = df_clientes[df_clientes.eq('').any(axis=1)]

# Mostrar os clientes com campos vazios
print("Clientes com pelo menos um campo vazio:\n")
print(clientes_com_vazios)
print(f"\nTotal de clientes com campos vazios: {len(clientes_com_vazios)}")
print(df_clientes.head())
print(f"Total de clientes gerados: {len(clientes)}")
