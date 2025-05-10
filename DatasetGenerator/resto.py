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

def get_brand(prod_name):
    brands = [
    "Logitech", "Razer", "Corsair", "SteelSeries", "HyperX", "Ducky", "Keychron",
    "Redragon", "Cooler Master", "G.Skill", "Microsoft", "Kinesis", "ASUS",
    "Anne Pro", "HP", "AOC", "Philips", "Dell", "Acer", "LG", "BenQ", "MSI",
    "Samsung", "Sennheiser", "JBL", "Bose", "Sony", "Apple", "Xiaomi", "Huawei",
    "Google (Pixel)", "OnePlus", "Oppo", "Nokia", "Vivo", "NVIDIA", "Gigabyte",
    "Kingston", "Crucial", "WD (Western Digital)", "Epson", "Canon", "Brother",
    "Fitbit", "Garmin"]
    
    # search for the brand in the product name
    for brand in brands:
        if brand.lower() in prod_name.lower():
            return brand

  
import numpy as np
def fator_sazonal(data):
    # Obtém o mês da data
    mes = data.month
    
    # Fatores sazonais base (mais altos em dezembro, mais baixos no verão)
    fatores_sazonais = {
        1: 0.8,   # Janeiro (queda pós-festas)
        2: 0.7,   # Fevereiro
        3: 0.8,   # Março 
        4: 0.9,   # Abril
        5: 1.0,   # Maio
        6: 0.9,   # Junho
        7: 0.8,   # Julho (férias de verão)
        8: 0.7,   # Agosto (férias de verão)
        9: 1.1,   # Setembro (regresso às aulas)
        10: 1.0,  # Outubro
        11: 1.2,  # Novembro (Black Friday)
        12: 1.5   # Dezembro (época festiva)
    }
    
    # Adiciona algum ruído aleatório ao fator
    factor = fatores_sazonais[mes] * random.uniform(0.9, 1.1)
    return factor

def gerar_afinidade_categorias(cliente_id):
    # Usa o ID do cliente como seed para consistência
    random.seed(hash(cliente_id))
    
    categorias = ["Teclados", "Mouses", "Monitores", "Smartphones", "Acessórios", 
                 "Áudio", "Impressoras", "Componentes", "Notebooks"]
    
    # Gera um dicionário com pontuações de afinidade para cada categoria
    afinidades = {}
    for categoria in categorias:
        # Distribuição tipo Dirichlet - algumas categorias serão favorecidas
        if random.random() < 0.3:  # 30% de chance de alta afinidade
            afinidades[categoria] = random.uniform(0.7, 1.0)
        else:
            afinidades[categoria] = random.uniform(0.1, 0.5)
    
    # Resetar a seed aleatória
    random.seed()
    return afinidades

def fator_demografico(cliente):
    # Calcular idade aproximada
    try:
        data_nascimento = pd.to_datetime(cliente['DataNascimento'], format='%d/%m/%Y')
        idade = datetime.now().year - data_nascimento.year
    except:
        idade = random.randint(18, 70)  # Default em caso de erro
    
    # Profissões de alta renda vs. baixa renda
    profissoes_alta_renda = ["Médico", "Advogado", "Engenheiro", "Gestor", "Diretor"]
    
    # Calculando fator demográfico
    fator_base = 1.0
    
    # Ajuste por idade
    if idade < 25:
        fator_base *= 0.85  # Jovens tendem a gastar menos por item
    elif idade > 50:
        fator_base *= 1.2   # Pessoas mais velhas podem gastar mais
        
    # Ajuste por profissão
    if cliente['Profissão'] in profissoes_alta_renda:
        fator_base *= 1.3
        
    # Ajuste por estado civil
    if cliente['EstadoCivil'] == "Casado":
        fator_base *= 1.1
        
    return fator_base

def selecionar_produto_com_bias(cliente, produtos, afinidade_categorias):
    # Bias geográfico implícito
    distritos_urbanos = ["Lisboa", "Porto", "Braga"]
    distritos_costeiros = ["Faro", "Setúbal", "Aveiro"]
    
    distrito = cliente.get('Distrito', '')
    
    # Lista base de todas as categorias
    categorias = list(afinidade_categorias.keys())
    pesos = list(afinidade_categorias.values())
    
    # Modificar pesos baseado em localização
    if distrito in distritos_urbanos:
        # Áreas urbanas - mais smartphones, notebooks
        for i, cat in enumerate(categorias):
            if cat in ["Smartphones", "Notebooks"]:
                pesos[i] *= 1.5
    
    elif distrito in distritos_costeiros:
        # Áreas costeiras - mais acessórios
        for i, cat in enumerate(categorias):
            if cat in ["Acessórios", "Áudio"]:
                pesos[i] *= 1.3
    
    # Normalizar pesos
    soma = sum(pesos)
    pesos = [p/soma for p in pesos]
    
    # Selecionar categoria com base nos pesos modificados
    categoria_escolhida = random.choices(categorias, weights=pesos, k=1)[0]
    
    # Filtrar produtos pela categoria escolhida
    produtos_categoria = [p for p in produtos['produtos_categorizados'] 
                         if p['categoria'] == categoria_escolhida]
    
    # Se não houver produtos na categoria, escolha qualquer produto
    if not produtos_categoria:
        return random.choice(produtos['produtos_categorizados'])
    
    return random.choice(produtos_categoria)

def gerar_preco_lognormal(produto, cliente, data_venda):
    # Parâmetros base
    mu = 4.5  # Média do logaritmo do preço
    sigma = 1.2  # Desvio padrão do logaritmo do preço
    
    # Ajuste sazonal
    fator_sazonalidade = fator_sazonal(data_venda)
    
    # Ajuste demográfico
    fator_demo = fator_demografico(cliente)
    
    # Gerar preço base
    preco_base = np.random.lognormal(mu, sigma)
    
    # Aplicar ajustes (sutilmente)
    preco_ajustado = preco_base * (1 + (fator_sazonalidade - 1) * 0.3) * (1 + (fator_demo - 1) * 0.2)
    
    # Limitar preço
    preco_final = np.clip(preco_ajustado, 50, 3000)
    
    return round(preco_final, 2)

def gerar_quantidade_poisson(cliente, produto, data_venda, media_quantidade=2):
    # Ajuste sazonal
    fator_sazonalidade = fator_sazonal(data_venda)
    
    # Ajustar a média da distribuição Poisson baseado em fatores
    media_ajustada = media_quantidade * fator_sazonalidade
    
    # Gerar quantidade
    quantidade = np.random.poisson(media_ajustada)
    
    return max(quantidade, 1)  # Garantir pelo menos 1


# ---------- Função para Gerar Vendas ----------

def gerar_vendas(cliente, num_vendas_cliente, produtos, tipo_loja, data_inicio, data_fim, canal):
    vendas = []
    
    # Gerar características do cliente uma vez (para consistência)
    afinidade_categorias = gerar_afinidade_categorias(cliente['customer_id'])
    
    # Distribuir as vendas ao longo do período de tempo
    # (criando implicitamente padrões temporais sem adicionar novos atributos)
    datas_vendas = []
    periodo_total = (data_fim - data_inicio).days
    
    for _ in range(num_vendas_cliente):
        # Gerar datas com tendência para clusters temporais
        if random.random() < 0.3:  # 30% das compras tendem a agrupar-se
            if datas_vendas:  # Se já existem datas de compra
                # Agrupar próximo a uma data existente (7 dias antes ou depois)
                data_base = random.choice(datas_vendas)
                dias_offset = random.randint(-7, 7)
                nova_data = data_base + timedelta(days=dias_offset)
                # Garantir que está dentro do intervalo
                if data_inicio <= nova_data <= data_fim:
                    datas_vendas.append(nova_data)
                else:
                    # Fallback para data aleatória
                    dias_aleatorios = random.randint(0, periodo_total)
                    datas_vendas.append(data_inicio + timedelta(days=dias_aleatorios))
            else:
                # Primeira compra - data aleatória
                dias_aleatorios = random.randint(0, periodo_total)
                datas_vendas.append(data_inicio + timedelta(days=dias_aleatorios))
        else:
            # Compra com data aleatória
            dias_aleatorios = random.randint(0, periodo_total)
            datas_vendas.append(data_inicio + timedelta(days=dias_aleatorios))
    
    # Ordenar as datas
    datas_vendas.sort()
    
    for i, data in enumerate(datas_vendas):
        # Selecionar produto com viés
        produto = selecionar_produto_com_bias(cliente, produtos, afinidade_categorias)
        
        # Gerar preço com distribuições que criam padrões
        preco = gerar_preco_lognormal(produto, cliente, data)
        
        # Gerar quantidade com distribuições que criam padrões
        quantidade = gerar_quantidade_poisson(cliente, produto, data)
        
        # Gerar desconto (com tendência para valores específicos)
        # Criar clusters de descontos em valores de marketing: 0%, 10%, 25%, 50%
        pontos_desconto = [0, 10, 25, 50]
        probs_desconto = [0.4, 0.3, 0.2, 0.1]  # Probabilidades decrescentes
        desconto_base = random.choices(pontos_desconto, weights=probs_desconto, k=1)[0]
        
        # Adicionar uma pequena variação para alguns casos
        if random.random() < 0.3:  # 30% das vezes
            desconto_base += random.randint(-5, 5)
            desconto_base = max(0, min(50, desconto_base))  # Limitar entre 0-50
        
        if tipo_loja == 'Online':
            product_id = next((p['ProductID'] for p in equivalencia_produtos if p['Nome_JSON'] == produto['nome']), None)
            venda = {
                'sale_id': f'S{cliente["customer_id"]}_{i+1}',
                'date': data.strftime('%Y-%m-%d'),
                'products': [{
                    'product_id': product_id,
                    'name': produto['nome'],
                    'category': produto['categoria'],
                    'brand': get_brand(produto['nome']),
                    'price': preco,
                    'quantity': quantidade,
                    'discount': desconto_base,
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
                'Marca': get_brand(produto['nome']),
                'Quantidade': quantidade,
                'Preço': preco,
                'Percentagem_Desconto': desconto_base,
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
