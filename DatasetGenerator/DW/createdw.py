import json
import csv
from datetime import datetime

# Função para garantir que não há valores nulos
def remove_null_values(dicionario):
    return {k: v for k, v in dicionario.items() if v not in [None, '', 'null']}

# Função para remover o "C" do ClienteId e o "P" do ProdutoId
def clean_ids(cliente_id, produto_id):
    if cliente_id and cliente_id.startswith("C"):
        cliente_id = cliente_id[1:]  # Remove o "C" do início
    if produto_id and produto_id.startswith("P"):
        produto_id = produto_id[1:]  # Remove o "P" do início
    return cliente_id, produto_id

# Abrir o ficheiro JSON
with open('../vendas_loja_online.json', 'r', encoding='utf-8') as file:
    vendas = json.load(file)

# Usar um dicionário para evitar duplicados
produtos_unicos = {}
produto_counter = 1  # Contador para garantir que os IDs começam em 1

for venda in vendas:
    produtos = venda.get("products")
    if isinstance(produtos, list):  # Verifica se é uma lista antes de iterar
        for produto in produtos:
            produto_id = produto.get("product_id")
            if produto_id and produto_id not in produtos_unicos:
                produto_info = {
                    "ProdutoId": produto_counter,  # Alterado para ProdutoId
                    "Nome": produto.get("name", ""),
                    "Marca": produto.get("brand", ""),
                    "Categoria": produto.get("category", "")
                }
                produtos_unicos[produto_id] = remove_null_values(produto_info)  # Remove nulls
                produto_counter += 1  # Incrementa o contador

# Escrever para o CSV com a ordem especificada
with open('DimProduto.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["ProdutoId", "Nome", "Marca", "Categoria"]  # Alterado para ProdutoId
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for produto in produtos_unicos.values():
        writer.writerow(produto)

print("Ficheiro DimProduto.csv criado com sucesso.")


# Carregar o ficheiro equivalencia_clientes.csv
clientes_info = {}
with open('../equivalencia_clientes.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cliente_id = row["customer_id"]
        clientes_info[cliente_id] = {
            "Nome": row.get("Nome"),
            "Sexo": row.get("Sexo"),
            "EstadoCivil": row.get("EstadoCivil"),
            "Profissão": row.get("Profissão"),
            "DataNascimento": row.get("DataNascimento"),
            "Distrito": row.get("Distrito"),
            "Concelho": row.get("Concelho")
        }

# Função para formatar a data de nascimento no formato YYYY-MM-DD
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')  # Retorna no formato YYYY-MM-DD
    except ValueError:
        return date_str

# Criar dicionário para clientes únicos
clientes_unicos = {}

for venda in vendas:
    cliente_id = venda.get("customer_id")
    distrito = venda.get("district", "")
    
    if cliente_id and cliente_id in clientes_info:
        dados_cliente = clientes_info[cliente_id]
        if cliente_id not in clientes_unicos:
            cliente_id = cliente_id.lstrip("C")  # Remove o "C" do início
            cliente_info = {
                "ClienteId": cliente_id,  # Alterado para ClienteId
                "Nome": dados_cliente["Nome"],
                "Sexo": dados_cliente["Sexo"],
                "EstadoCivil": dados_cliente["EstadoCivil"],
                "Profissão": dados_cliente["Profissão"],
                "DataNascimento": format_date(dados_cliente["DataNascimento"]),
                "Distrito": distrito,
                "Concelho": dados_cliente["Concelho"]
            }
            clientes_unicos[cliente_id] = remove_null_values(cliente_info)  # Remove nulls

# Escrever para DimCliente.csv com a ordem especificada
with open('DimCliente.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        "ClienteId", "Nome", "Sexo", "EstadoCivil", 
        "Profissão", "Concelho", "Distrito", "DataNascimento"  # Alterado para ClienteId
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for cliente in clientes_unicos.values():
        writer.writerow(cliente)

print("Ficheiro DimCliente.csv criado com sucesso.")


tfvenda_data = []

# Criar dicionário para armazenar os dados da dimensão Data
data_unica = {}

for venda in vendas:
    sale_id = venda["sale_id"]
    customer_id = venda.get("customer_id")
    
    if "products" in venda and venda["products"]:
        for produto in venda["products"]:
            product_id = produto.get("product_id")
            nome_produto = produto.get("name", "")
            categoria_produto = produto.get("category", "")
            marca_produto = produto.get("brand", "")
            preco_unitario = produto.get("price")
            quantidade = produto.get("quantity")
            desconto = produto.get("discount")
            data_id = venda.get("date", "")
            canal = venda.get("channel", "")

            # Remover "C" de ClienteId e "P" de ProdutoId
            customer_id, product_id = clean_ids(customer_id, product_id)

            # Verificando se algum campo essencial é nulo
            if None in [customer_id, product_id] or '' in [customer_id, product_id]:
                continue  # Ignora este produto se ClienteId ou ProdutoId forem nulos

            # Verificando se algum campo essencial de produto é nulo
            if None in [preco_unitario, quantidade, desconto, data_id, canal] or '' in [preco_unitario, quantidade, desconto, data_id, canal]:
                continue  # Ignora este produto se algum valor essencial for nulo

            valor_total = preco_unitario * quantidade * (1 - desconto / 100)


            tfvenda_data.append({
                "DataId": data_id,  # Adicionado DataId
                "ClienteId": customer_id,  # Alterado para ClienteId
                "ProdutoId": product_id,  # Alterado para ProdutoId
                "Quantidade": quantidade,
                "PrecoUnitario": preco_unitario,
                "PercentagemDesconto": desconto,
                "ValorTotal": valor_total,
                "Canal": canal,
            })
            


# Escrever para o CSV com a ordem especificada
with open('TFVenda.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        "DataId", "ClienteId", "ProdutoId", "Quantidade", 
        "PrecoUnitario", "PercentagemDesconto", "ValorTotal", "Canal", "Mes"  # Ordem ajustada
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for venda in tfvenda_data:
        writer.writerow(venda)

print("Ficheiro TFVenda.csv criado com sucesso.")

# Carregar o ficheiro de feriados
feriados = set()
with open('../feriados_portugal_2010_2020.csv', 'r', encoding='utf-8') as feriados_file:
    reader = csv.reader(feriados_file)
    next(reader)
    for row in reader:
        feriados.add(row[0].strip())

# Funções auxiliares
def is_weekend(date_obj):
    return date_obj.weekday() >= 5  # 5 = sábado, 6 = domingo

def get_quarter(month):
    if month in [1, 2, 3]:
        return 1
    elif month in [4, 5, 6]:
        return 2
    elif month in [7, 8, 9]:
        return 3
    else:
        return 4

# Extrair datas únicas da TFVenda
datas_unicas = set([v["DataId"] for v in tfvenda_data if v["DataId"]])

dimtempo_data = []

for data in sorted(datas_unicas):
    try:
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        dimtempo_data.append({
            "DataId": data,
            "Mes": data_obj.month,
            "Trimestre": get_quarter(data_obj.month),
            "Ano": data_obj.year,
            "FimDeSemana": "S" if is_weekend(data_obj) else "N",
            "Feriado": "S" if data in feriados else "N"
        })
    except ValueError:
        continue  # Ignora datas mal formatadas

# Escrever DimTempo.csv
with open('DimTempo.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["DataId", "Mes", "Trimestre", "Ano", "FimDeSemana", "Feriado"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for linha in dimtempo_data:
        writer.writerow(linha)

print("Ficheiro DimTempo.csv criado com sucesso.")
