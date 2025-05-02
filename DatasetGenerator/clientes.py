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

# ---------- Carregamento de Dados ----------

distritos_concelhos = carregar_json('dados/distritos_concelhos.json')
dominios = carregar_json('dados/dominios_email.json')
profissoes = carregar_json('dados/profissoes.json')
estados_civis = carregar_json('dados/estados_civis.json')

# ---------- Configurações ----------

distrito_pesos = {
    'Braga': 0.40, 'Porto': 0.15, 'Viana do Castelo': 0.10, 'Vila Real': 0.08,
    'Aveiro': 0.05, 'Bragança': 0.03, 'Castelo Branco': 0.02, 'Coimbra': 0.03,
    'Évora': 0.01, 'Faro': 0.01, 'Guarda': 0.02, 'Leiria': 0.02, 'Lisboa': 0.05,
    'Portalegre': 0.01, 'Santarém': 0.02, 'Setúbal': 0.03, 'Viseu': 0.03, 'Beja': 0.01
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

    cliente = {
        'Nome': nome_completo,
        'Profissão': profissao,
        'EstadoCivil': random.choice(estados_civis),
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


# ---------- Introduzir valores vazios aleatórios entre 4 e 6 clientes ----------

num_clientes_com_vazios = random.randint(4, 6)
indices_afetados = random.sample(range(len(clientes)), num_clientes_com_vazios)

campos_proibidos = ['Nome', 'Email', 'DataNascimento']  # Campos que nunca queremos deixar vazios

for idx in indices_afetados:
    campos_possiveis = [campo for campo in clientes[idx].keys() if campo not in campos_proibidos]
    num_campos_a_vaziar = random.randint(1, 3)
    campos_a_vaziar = random.sample(campos_possiveis, num_campos_a_vaziar)
    for campo in campos_a_vaziar:
        clientes[idx][campo] = ""  # String vazia para representar valor em branco


# ---------- Exportação ----------

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv('clientes.csv', index=False)
clientes_com_vazios = df_clientes[df_clientes.eq('').any(axis=1)]

# Mostrar os clientes com campos vazios
print("Clientes com pelo menos um campo vazio:\n")
print(clientes_com_vazios)
print(f"\nTotal de clientes com campos vazios: {len(clientes_com_vazios)}")
print(df_clientes.head())
print(f"Total de clientes gerados: {len(clientes)}")
