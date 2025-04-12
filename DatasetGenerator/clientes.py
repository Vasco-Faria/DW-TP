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

    data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)

    cliente = {
        'Nome': nome_completo,
        'Profissão': random.choice(profissoes),
        'EstadoCivil': random.choice(estados_civis),
        'Sexo': sexo,
        'Distrito': distrito,
        'Concelho': concelho,
        'DataNascimento': data_nascimento.strftime('%d/%m/%Y'),
        'Email': email
    }

    clientes.append(cliente)

# ---------- Exportação ----------

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv('clientes.csv', index=False)
print(df_clientes.head())
print(f"Total de clientes gerados: {len(clientes)}")