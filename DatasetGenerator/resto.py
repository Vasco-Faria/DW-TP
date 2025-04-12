from faker import Faker
import pandas as pd
import random
import json
from datetime import datetime, timedelta



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
produtos_categorizados_fisicos = carregar_json('dados/produtoscat_fisicos.json')
produtos_categorizados_online = carregar_json('dados/produtoscat_online.json')


# Inicializar Faker
fake = Faker('pt_PT')

# Carregar os dados de clientes gerados anteriormente
df_clientes = pd.read_csv('clientes.csv')

# Gerar Tabela de Equivalência de Clientes
equivalencia_clientes = df_clientes[['Nome', 'Profissão', 'EstadoCivil', 'Sexo', 'Distrito', 'Concelho', 'DataNascimento', 'Email']].copy()
equivalencia_clientes['customer_id'] = [f'C{i+100}' for i in range(len(df_clientes))]
equivalencia_clientes.to_csv('equivalencia_clientes.csv', index=False)


# 3. Gerar Registos da Loja Física (Fonte 1: Excel)
vendas_fisicas = []
for i in range(5000):
    data = fake.date_between_dates(date_start=datetime(2010, 1, 1), date_end=datetime(2020, 12, 31))
    cliente = equivalencia_clientes.iloc[random.randint(0, len(equivalencia_clientes)-1)]  # Obtendo um cliente aleatório
    produto = random.choice(produtos_categorizados_fisicos['produtos_categorizados'])  # Selecionando um produto aleatório
    venda = {
        'Data_Venda': data.strftime('%d/%m/%Y'),
        'Produto': produto['nome'],  # Nome do produto
        'Categoria': produto['categoria'],  # Categoria do produto
        'Quantidade': random.randint(1, 5),
        'Preço': round(random.uniform(20, 1500), 2),
        'Percentagem_Desconto': random.randint(0, 50),
        'Cliente_Nome': cliente['Nome'],
        'Concelho': cliente['Concelho'],
        'Canal': 'Loja Física'
    }
    vendas_fisicas.append(venda)

df_vendas_fisicas = pd.DataFrame(vendas_fisicas)
df_vendas_fisicas.to_excel('vendas_loja_fisica.xlsx', index=False)

# 4. Gerar Registos da Loja Online (Fonte 2: JSON)
vendas_online = []
for i in range(3000):  # 3.000 transações entre 2021 e 2025
    data = fake.date_between_dates(date_start=datetime(2021, 1, 1), date_end=datetime(2025, 4, 12))
    cliente = equivalencia_clientes.iloc[random.randint(0, len(equivalencia_clientes)-1)]
    produto = random.choice(produtos_categorizados_online['produtos_categorizados'])  # Selecionando um produto aleatório
    venda = {
        'sale_id': f'S{i+1000}',
        'date': data.strftime('%Y-%m-%d'),
        'products': [{
            'product_id': f'P{random.randint(1, 1000)}',
            'name': produto['nome'],  # Access the list
            'category': produto['categoria'],  # Access the list	
            'price': round(random.uniform(20, 1500), 2),
            'quantity': random.randint(1, 5),
            'discount': random.randint(0, 50),
        }],
        'customer_id': cliente['customer_id'],
        'email': cliente['Email'],
        'district': cliente['Distrito'],
        'channel': 'Online'
    }
    vendas_online.append(venda)

with open('vendas_loja_online.json', 'w') as f:
    json.dump(vendas_online, f, indent=4)

# 5. Gerar Tabela de Equivalência de Produtos (Atualizada com Todos os Produtos)
equivalencia_produtos = [
    {'Nome_Excel': 'Rato Logitech MX Master', 'Nome_JSON': 'Logitech MX Master 3 Mouse', 'ProductID': 'P001'},
    {'Nome_Excel': 'Logitech Rato MX Anywhere', 'Nome_JSON': 'Logitech MX Anywhere 3 Mouse', 'ProductID': 'P002'},
    {'Nome_Excel': 'Teclado Mecânico Corsair K70', 'Nome_JSON': 'Corsair K70 RGB MK.2 Keyboard', 'ProductID': 'P003'},
    {'Nome_Excel': 'Teclado Gaming Razer BlackWidow', 'Nome_JSON': 'Razer BlackWidow V3 Keyboard', 'ProductID': 'P004'},
    {'Nome_Excel': 'Monitor Dell 24"', 'Nome_JSON': 'Dell S2421HGF 24" Monitor', 'ProductID': 'P005'},
    {'Nome_Excel': 'Monitor 27 Polegadas HP', 'Nome_JSON': 'HP 27f 27" Monitor', 'ProductID': 'P006'},
    {'Nome_Excel': 'Headset Gamer HyperX Cloud', 'Nome_JSON': 'HyperX Cloud II Headset', 'ProductID': 'P007'},
    {'Nome_Excel': 'Headset Gaming SteelSeries Arctis', 'Nome_JSON': 'SteelSeries Arctis 7 Headset', 'ProductID': 'P008'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy S10', 'Nome_JSON': 'Samsung Galaxy S10 Smartphone', 'ProductID': 'P009'},
    {'Nome_Excel': 'Smartphone Apple iPhone 11', 'Nome_JSON': 'Apple iPhone 11 Smartphone', 'ProductID': 'P010'},
    {'Nome_Excel': 'Rato Razer DeathAdder', 'Nome_JSON': 'Razer DeathAdder V2 Mouse', 'ProductID': 'P011'},
    {'Nome_Excel': 'Teclado Logitech G Pro', 'Nome_JSON': 'Logitech G Pro X Keyboard', 'ProductID': 'P012'},
    {'Nome_Excel': 'Monitor 24" Acer', 'Nome_JSON': 'Acer Nitro VG240Y 24" Monitor', 'ProductID': 'P013'},
    {'Nome_Excel': 'Headset Logitech G432', 'Nome_JSON': 'Logitech G432 Gaming Headset', 'ProductID': 'P014'},
    {'Nome_Excel': 'Smartphone Xiaomi Redmi Note 9', 'Nome_JSON': 'Xiaomi Redmi Note 9 Smartphone', 'ProductID': 'P015'},
    {'Nome_Excel': 'Rato Corsair Dark Core', 'Nome_JSON': 'Corsair Dark Core RGB Mouse', 'ProductID': 'P016'},
    {'Nome_Excel': 'Teclado Mecânico Ducky One 2', 'Nome_JSON': 'Ducky One 2 Mini Keyboard', 'ProductID': 'P017'},
    {'Nome_Excel': 'Monitor 32" LG', 'Nome_JSON': 'LG 32UN500 32" Monitor', 'ProductID': 'P018'},
    {'Nome_Excel': 'Headset Razer Kraken', 'Nome_JSON': 'Razer Kraken X Headset', 'ProductID': 'P019'},
    {'Nome_Excel': 'Smartphone Huawei P30', 'Nome_JSON': 'Huawei P30 Smartphone', 'ProductID': 'P020'},
    {'Nome_Excel': 'Rato SteelSeries Rival 3', 'Nome_JSON': 'SteelSeries Rival 3 Mouse', 'ProductID': 'P021'},
    {'Nome_Excel': 'Teclado Gaming Keychron K8', 'Nome_JSON': 'Keychron K8 Wireless Keyboard', 'ProductID': 'P022'},
    {'Nome_Excel': 'Monitor 27" ASUS', 'Nome_JSON': 'ASUS TUF Gaming VG27AQ 27" Monitor', 'ProductID': 'P023'},
    {'Nome_Excel': 'Headset Corsair Void Pro', 'Nome_JSON': 'Corsair Void Elite RGB Headset', 'ProductID': 'P024'},
    {'Nome_Excel': 'Smartphone Google Pixel 4', 'Nome_JSON': 'Google Pixel 4 Smartphone', 'ProductID': 'P025'},
    {'Nome_Excel': 'Rato HyperX Pulsefire', 'Nome_JSON': 'HyperX Pulsefire FPS Pro Mouse', 'ProductID': 'P026'},
    {'Nome_Excel': 'Teclado Logitech MX Keys', 'Nome_JSON': 'Logitech MX Keys Advanced Keyboard', 'ProductID': 'P027'},
    {'Nome_Excel': 'Monitor Dell UltraSharp 27"', 'Nome_JSON': 'Dell UltraSharp U2720Q 27" Monitor', 'ProductID': 'P028'},
    {'Nome_Excel': 'Headset Sennheiser HD 450BT', 'Nome_JSON': 'Sennheiser HD 450BT Headphones', 'ProductID': 'P029'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy A51', 'Nome_JSON': 'Samsung Galaxy A51 Smartphone', 'ProductID': 'P030'},
    {'Nome_Excel': 'Rato Logitech G502', 'Nome_JSON': 'Logitech G502 Hero Mouse', 'ProductID': 'P031'},
    {'Nome_Excel': 'Teclado Razer Huntsman', 'Nome_JSON': 'Razer Huntsman Elite Keyboard', 'ProductID': 'P032'},
    {'Nome_Excel': 'Monitor 24 Polegadas Samsung', 'Nome_JSON': 'Samsung S24F350 24" Monitor', 'ProductID': 'P033'},
    {'Nome_Excel': 'Headset SteelSeries Siberia', 'Nome_JSON': 'SteelSeries Arctis 5 Headset', 'ProductID': 'P034'},
    {'Nome_Excel': 'Smartphone iPhone 12', 'Nome_JSON': 'Apple iPhone 12 Smartphone', 'ProductID': 'P035'},
    # Novos produtos (150 adicionais)
    {'Nome_Excel': 'Rato Logitech G203', 'Nome_JSON': 'Logitech G203 Lightsync Mouse', 'ProductID': 'P036'},
    {'Nome_Excel': 'Teclado Corsair K55', 'Nome_JSON': 'Corsair K55 RGB Keyboard', 'ProductID': 'P037'},
    {'Nome_Excel': 'Monitor 22" AOC', 'Nome_JSON': 'AOC 22V2H 22" Monitor', 'ProductID': 'P038'},
    {'Nome_Excel': 'Headset JBL Quantum 100', 'Nome_JSON': 'JBL Quantum 100 Headset', 'ProductID': 'P039'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy S20', 'Nome_JSON': 'Samsung Galaxy S20 Smartphone', 'ProductID': 'P040'},
    {'Nome_Excel': 'Rato Razer Viper', 'Nome_JSON': 'Razer Viper Ultimate Mouse', 'ProductID': 'P041'},
    {'Nome_Excel': 'Teclado Mecânico Redragon K552', 'Nome_JSON': 'Redragon K552 Kumara Keyboard', 'ProductID': 'P042'},
    {'Nome_Excel': 'Monitor 27 Polegadas LG', 'Nome_JSON': 'LG 27QN600 27" Monitor', 'ProductID': 'P043'},
    {'Nome_Excel': 'Headset Logitech G Pro X', 'Nome_JSON': 'Logitech G Pro X Headset', 'ProductID': 'P044'},
    {'Nome_Excel': 'Smartphone iPhone 13', 'Nome_JSON': 'Apple iPhone 13 Smartphone', 'ProductID': 'P045'},
    {'Nome_Excel': 'Rato Corsair Harpoon', 'Nome_JSON': 'Corsair Harpoon RGB Mouse', 'ProductID': 'P046'},
    {'Nome_Excel': 'Teclado Gaming SteelSeries Apex 5', 'Nome_JSON': 'SteelSeries Apex 5 Keyboard', 'ProductID': 'P047'},
    {'Nome_Excel': 'Monitor 24" BenQ', 'Nome_JSON': 'BenQ Zowie XL2411P 24" Monitor', 'ProductID': 'P048'},
    {'Nome_Excel': 'Headset HyperX Cloud Stinger', 'Nome_JSON': 'HyperX Cloud Stinger Core Headset', 'ProductID': 'P049'},
    {'Nome_Excel': 'Smartphone Xiaomi 11T', 'Nome_JSON': 'Xiaomi 11T Pro Smartphone', 'ProductID': 'P050'},
    {'Nome_Excel': 'Rato SteelSeries Aerox 3', 'Nome_JSON': 'SteelSeries Aerox 3 Wireless Mouse', 'ProductID': 'P051'},
    {'Nome_Excel': 'Teclado Logitech K380', 'Nome_JSON': 'Logitech K380 Bluetooth Keyboard', 'ProductID': 'P052'},
    {'Nome_Excel': 'Monitor 32 Polegadas Dell', 'Nome_JSON': 'Dell P3221D 32" Monitor', 'ProductID': 'P053'},
    {'Nome_Excel': 'Headset Razer BlackShark V2', 'Nome_JSON': 'Razer BlackShark V2 X Headset', 'ProductID': 'P054'},
    {'Nome_Excel': 'Smartphone Huawei Mate 40', 'Nome_JSON': 'Huawei Mate 40 Pro Smartphone', 'ProductID': 'P055'},
    {'Nome_Excel': 'Rato HyperX Pulsefire Dart', 'Nome_JSON': 'HyperX Pulsefire Dart Mouse', 'ProductID': 'P056'},
    {'Nome_Excel': 'Teclado Ducky Shine 7', 'Nome_JSON': 'Ducky Shine 7 Keyboard', 'ProductID': 'P057'},
    {'Nome_Excel': 'Monitor 27" Acer Predator', 'Nome_JSON': 'Acer Predator XB273U 27" Monitor', 'ProductID': 'P058'},
    {'Nome_Excel': 'Headset Corsair HS60', 'Nome_JSON': 'Corsair HS60 Pro Headset', 'ProductID': 'P059'},
    {'Nome_Excel': 'Smartphone Google Pixel 5', 'Nome_JSON': 'Google Pixel 5 Smartphone', 'ProductID': 'P060'},
    {'Nome_Excel': 'Rato Logitech G305', 'Nome_JSON': 'Logitech G305 Lightspeed Mouse', 'ProductID': 'P061'},
    {'Nome_Excel': 'Teclado Razer Ornata V2', 'Nome_JSON': 'Razer Ornata V2 Keyboard', 'ProductID': 'P062'},
    {'Nome_Excel': 'Monitor 24 Polegadas HP', 'Nome_JSON': 'HP 24mh 24" Monitor', 'ProductID': 'P063'},
    {'Nome_Excel': 'Headset Sennheiser GSP 300', 'Nome_JSON': 'Sennheiser GSP 300 Headset', 'ProductID': 'P064'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy Note 20', 'Nome_JSON': 'Samsung Galaxy Note 20 Ultra Smartphone', 'ProductID': 'P065'},
    {'Nome_Excel': 'Webcam Logitech C920', 'Nome_JSON': 'Logitech C920 HD Pro Webcam', 'ProductID': 'P066'},
    {'Nome_Excel': 'Placa Gráfica NVIDIA RTX 3060', 'Nome_JSON': 'NVIDIA GeForce RTX 3060 Graphics Card', 'ProductID': 'P067'},
    {'Nome_Excel': 'SSD Samsung 970 EVO 1TB', 'Nome_JSON': 'Samsung 970 EVO Plus 1TB SSD', 'ProductID': 'P068'},
    {'Nome_Excel': 'Impressora HP DeskJet 2720', 'Nome_JSON': 'HP DeskJet 2720 Printer', 'ProductID': 'P069'},
    {'Nome_Excel': 'Smartwatch Apple Watch Series 6', 'Nome_JSON': 'Apple Watch Series 6 Smartwatch', 'ProductID': 'P070'},
    {'Nome_Excel': 'Webcam Razer Kiyo', 'Nome_JSON': 'Razer Kiyo Streaming Webcam', 'ProductID': 'P071'},
    {'Nome_Excel': 'Placa Gráfica ASUS RTX 3070', 'Nome_JSON': 'ASUS ROG Strix RTX 3070 Graphics Card', 'ProductID': 'P072'},
    {'Nome_Excel': 'SSD Kingston A2000 500GB', 'Nome_JSON': 'Kingston A2000 500GB SSD', 'ProductID': 'P073'},
    {'Nome_Excel': 'Impressora Epson EcoTank L3150', 'Nome_JSON': 'Epson EcoTank L3150 Printer', 'ProductID': 'P074'},
    {'Nome_Excel': 'Smartwatch Samsung Galaxy Watch 4', 'Nome_JSON': 'Samsung Galaxy Watch 4 Smartwatch', 'ProductID': 'P075'},
    {'Nome_Excel': 'Rato Microsoft Surface Precision', 'Nome_JSON': 'Microsoft Surface Precision Mouse', 'ProductID': 'P076'},
    {'Nome_Excel': 'Teclado Mecânico Kinesis Freestyle', 'Nome_JSON': 'Kinesis Freestyle Edge Keyboard', 'ProductID': 'P077'},
    {'Nome_Excel': 'Monitor 34" LG UltraWide', 'Nome_JSON': 'LG 34WN80C 34" UltraWide Monitor', 'ProductID': 'P078'},
    {'Nome_Excel': 'Headset Bose QuietComfort 35', 'Nome_JSON': 'Bose QuietComfort 35 II Headphones', 'ProductID': 'P079'},
    {'Nome_Excel': 'Smartphone OnePlus 9', 'Nome_JSON': 'OnePlus 9 Smartphone', 'ProductID': 'P080'},
    {'Nome_Excel': 'Rato ASUS ROG Chakram', 'Nome_JSON': 'ASUS ROG Chakram Mouse', 'ProductID': 'P081'},
    {'Nome_Excel': 'Teclado Gaming Cooler Master CK552', 'Nome_JSON': 'Cooler Master CK552 Keyboard', 'ProductID': 'P082'},
    {'Nome_Excel': 'Monitor 27 Polegadas MSI', 'Nome_JSON': 'MSI Optix MAG272CQR 27" Monitor', 'ProductID': 'P083'},
    {'Nome_Excel': 'Headset Sony WH-CH710N', 'Nome_JSON': 'Sony WH-CH710N Headphones', 'ProductID': 'P084'},
    {'Nome_Excel': 'Smartphone Oppo Find X3', 'Nome_JSON': 'Oppo Find X3 Pro Smartphone', 'ProductID': 'P085'},
    {'Nome_Excel': 'Webcam Logitech StreamCam', 'Nome_JSON': 'Logitech StreamCam Webcam', 'ProductID': 'P086'},
    {'Nome_Excel': 'Placa Gráfica MSI RTX 3080', 'Nome_JSON': 'MSI GeForce RTX 3080 Graphics Card', 'ProductID': 'P087'},
    {'Nome_Excel': 'SSD Crucial MX500 1TB', 'Nome_JSON': 'Crucial MX500 1TB SSD', 'ProductID': 'P088'},
    {'Nome_Excel': 'Impressora Canon PIXMA G6020', 'Nome_JSON': 'Canon PIXMA G6020 Printer', 'ProductID': 'P089'},
    {'Nome_Excel': 'Smartwatch Huawei Watch GT 3', 'Nome_JSON': 'Huawei Watch GT 3 Smartwatch', 'ProductID': 'P090'},
    {'Nome_Excel': 'Rato HP Spectre 700', 'Nome_JSON': 'HP Spectre 700 Mouse', 'ProductID': 'P091'},
    {'Nome_Excel': 'Teclado Logitech Craft', 'Nome_JSON': 'Logitech Craft Advanced Keyboard', 'ProductID': 'P092'},
    {'Nome_Excel': 'Monitor 24" Philips', 'Nome_JSON': 'Philips 243V7Q 24" Monitor', 'ProductID': 'P093'},
    {'Nome_Excel': 'Headset JBL Live 650BTNC', 'Nome_JSON': 'JBL Live 650BTNC Headphones', 'ProductID': 'P094'},
    {'Nome_Excel': 'Smartphone Vivo Y70', 'Nome_JSON': 'Vivo Y70 Smartphone', 'ProductID': 'P095'},
    {'Nome_Excel': 'Rato Corsair Scimitar', 'Nome_JSON': 'Corsair Scimitar RGB Elite Mouse', 'ProductID': 'P096'},
    {'Nome_Excel': 'Teclado Gaming Anne Pro 2', 'Nome_JSON': 'Anne Pro 2 Keyboard', 'ProductID': 'P097'},
    {'Nome_Excel': 'Monitor 32" Samsung Odyssey G5', 'Nome_JSON': 'Samsung Odyssey G5 32" Monitor', 'ProductID': 'P098'},
    {'Nome_Excel': 'Headset SteelSeries Arctis 9', 'Nome_JSON': 'SteelSeries Arctis 9 Wireless Headset', 'ProductID': 'P099'},
    {'Nome_Excel': 'Smartphone Nokia 8.3', 'Nome_JSON': 'Nokia 8.3 5G Smartphone', 'ProductID': 'P100'},
    {'Nome_Excel': 'Webcam Microsoft LifeCam HD', 'Nome_JSON': 'Microsoft LifeCam HD-3000 Webcam', 'ProductID': 'P101'},
    {'Nome_Excel': 'Placa Gráfica Gigabyte RTX 3060 Ti', 'Nome_JSON': 'Gigabyte RTX 3060 Ti Graphics Card', 'ProductID': 'P102'},
    {'Nome_Excel': 'SSD WD Blue SN550 1TB', 'Nome_JSON': 'WD Blue SN550 1TB SSD', 'ProductID': 'P103'},
    {'Nome_Excel': 'Impressora Brother HL-L2350DW', 'Nome_JSON': 'Brother HL-L2350DW Printer', 'ProductID': 'P104'},
    {'Nome_Excel': 'Smartwatch Fitbit Versa 3', 'Nome_JSON': 'Fitbit Versa 3 Smartwatch', 'ProductID': 'P105'},
    {'Nome_Excel': 'Rato Razer Basilisk V3', 'Nome_JSON': 'Razer Basilisk V3 Mouse', 'ProductID': 'P106'},
    {'Nome_Excel': 'Teclado Corsair K100 RGB', 'Nome_JSON': 'Corsair K100 RGB Optical Keyboard', 'ProductID': 'P107'},
    {'Nome_Excel': 'Monitor 27" Dell Alienware', 'Nome_JSON': 'Dell Alienware AW2721D 27" Monitor', 'ProductID': 'P108'},
    {'Nome_Excel': 'Headset HyperX Cloud Alpha', 'Nome_JSON': 'HyperX Cloud Alpha S Headset', 'ProductID': 'P109'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy Z Fold 3', 'Nome_JSON': 'Samsung Galaxy Z Fold 3 Smartphone', 'ProductID': 'P110'},
    {'Nome_Excel': 'Rato Logitech G703', 'Nome_JSON': 'Logitech G703 Lightspeed Mouse', 'ProductID': 'P111'},
    {'Nome_Excel': 'Teclado Gaming G.Skill Ripjaws KM570', 'Nome_JSON': 'G.Skill Ripjaws KM570 Keyboard', 'ProductID': 'P112'},
    {'Nome_Excel': 'Monitor 24 Polegadas ASUS ROG', 'Nome_JSON': 'ASUS ROG Swift PG259QN 24" Monitor', 'ProductID': 'P113'},
    {'Nome_Excel': 'Headset Razer Barracuda X', 'Nome_JSON': 'Razer Barracuda X Headset', 'ProductID': 'P114'},
    {'Nome_Excel': 'Smartphone iPhone 14', 'Nome_JSON': 'Apple iPhone 14 Smartphone', 'ProductID': 'P115'},
    {'Nome_Excel': 'Webcam Logitech Brio', 'Nome_JSON': 'Logitech Brio Ultra HD Webcam', 'ProductID': 'P116'},
    {'Nome_Excel': 'Placa Gráfica NVIDIA GTX 1660 Super', 'Nome_JSON': 'NVIDIA GTX 1660 Super Graphics Card', 'ProductID': 'P117'},
    {'Nome_Excel': 'SSD Samsung 980 Pro 2TB', 'Nome_JSON': 'Samsung 980 Pro 2TB SSD', 'ProductID': 'P118'},
    {'Nome_Excel': 'Impressora HP LaserJet Pro M15w', 'Nome_JSON': 'HP LaserJet Pro M15w Printer', 'ProductID': 'P119'},
    {'Nome_Excel': 'Smartwatch Garmin Forerunner 245', 'Nome_JSON': 'Garmin Forerunner 245 Smartwatch', 'ProductID': 'P120'},
    {'Nome_Excel': 'Rato SteelSeries Sensei 310', 'Nome_JSON': 'SteelSeries Sensei 310 Mouse', 'ProductID': 'P121'},
    {'Nome_Excel': 'Teclado Ducky One 3', 'Nome_JSON': 'Ducky One 3 Matcha Keyboard', 'ProductID': 'P122'},
    {'Nome_Excel': 'Monitor 27 Polegadas AOC Agon', 'Nome_JSON': 'AOC Agon AG273QCG 27" Monitor', 'ProductID': 'P123'},
    {'Nome_Excel': 'Headset Corsair Virtuoso RGB', 'Nome_JSON': 'Corsair Virtuoso RGB Wireless Headset', 'ProductID': 'P124'},
    {'Nome_Excel': 'Smartphone Xiaomi 12', 'Nome_JSON': 'Xiaomi 12 Pro Smartphone', 'ProductID': 'P125'},
    {'Nome_Excel': 'Rato HyperX Pulsefire Haste', 'Nome_JSON': 'HyperX Pulsefire Haste Mouse', 'ProductID': 'P126'},
    {'Nome_Excel': 'Teclado Logitech G915 TKL', 'Nome_JSON': 'Logitech G915 TKL Lightspeed Keyboard', 'ProductID': 'P127'},
    {'Nome_Excel': 'Monitor 32" HP Omen', 'Nome_JSON': 'HP Omen 32" Monitor', 'ProductID': 'P128'},
    {'Nome_Excel': 'Headset Sennheiser Momentum 3', 'Nome_JSON': 'Sennheiser Momentum 3 Wireless Headphones', 'ProductID': 'P129'},
    {'Nome_Excel': 'Smartphone Google Pixel 6', 'Nome_JSON': 'Google Pixel 6 Pro Smartphone', 'ProductID': 'P130'},
    {'Nome_Excel': 'Rato Corsair Katar Pro', 'Nome_JSON': 'Corsair Katar Pro XT Mouse', 'ProductID': 'P131'},
    {'Nome_Excel': 'Teclado Gaming Razer Cynosa V2', 'Nome_JSON': 'Razer Cynosa V2 Keyboard', 'ProductID': 'P132'},
    {'Nome_Excel': 'Monitor 24" LG UltraGear', 'Nome_JSON': 'LG UltraGear 24GN600 24" Monitor', 'ProductID': 'P133'},
    {'Nome_Excel': 'Headset SteelSeries Arctis 1', 'Nome_JSON': 'SteelSeries Arctis 1 Wireless Headset', 'ProductID': 'P134'},
    {'Nome_Excel': 'Smartphone Huawei P40', 'Nome_JSON': 'Huawei P40 Pro Smartphone', 'ProductID': 'P135'},
    {'Nome_Excel': 'Webcam Razer Kiyo Pro', 'Nome_JSON': 'Razer Kiyo Pro Ultra Webcam', 'ProductID': 'P136'},
    {'Nome_Excel': 'Placa Gráfica ASUS TUF RTX 3090', 'Nome_JSON': 'ASUS TUF Gaming RTX 3090 Graphics Card', 'ProductID': 'P137'},
    {'Nome_Excel': 'SSD Kingston NV2 1TB', 'Nome_JSON': 'Kingston NV2 1TB SSD', 'ProductID': 'P138'},
    {'Nome_Excel': 'Impressora Epson WorkForce WF-110', 'Nome_JSON': 'Epson WorkForce WF-110 Printer', 'ProductID': 'P139'},
    {'Nome_Excel': 'Smartwatch Apple Watch Series 7', 'Nome_JSON': 'Apple Watch Series 7 Smartwatch', 'ProductID': 'P140'},
    {'Nome_Excel': 'Rato Logitech MX Vertical', 'Nome_JSON': 'Logitech MX Vertical Mouse', 'ProductID': 'P141'},
    {'Nome_Excel': 'Teclado Corsair K65 Mini', 'Nome_JSON': 'Corsair K65 RGB Mini Keyboard', 'ProductID': 'P142'},
    {'Nome_Excel': 'Monitor 27" BenQ Mobiuz', 'Nome_JSON': 'BenQ Mobiuz EX2710 27" Monitor', 'ProductID': 'P143'},
    {'Nome_Excel': 'Headset JBL Quantum 400', 'Nome_JSON': 'JBL Quantum 400 Headset', 'ProductID': 'P144'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy S21', 'Nome_JSON': 'Samsung Galaxy S21 Ultra Smartphone', 'ProductID': 'P145'},
    {'Nome_Excel': 'Rato Razer Naga Pro', 'Nome_JSON': 'Razer Naga Pro Mouse', 'ProductID': 'P146'},
    {'Nome_Excel': 'Teclado Gaming Keychron K4', 'Nome_JSON': 'Keychron K4 Wireless Keyboard', 'ProductID': 'P147'},
    {'Nome_Excel': 'Monitor 32 Polegadas Acer', 'Nome_JSON': 'Acer 32" Predator XB323U Monitor', 'ProductID': 'P148'},
    {'Nome_Excel': 'Headset HyperX Cloud Flight', 'Nome_JSON': 'HyperX Cloud Flight Wireless Headset', 'ProductID': 'P149'},
    {'Nome_Excel': 'Smartphone OnePlus 10 Pro', 'Nome_JSON': 'OnePlus 10 Pro Smartphone', 'ProductID': 'P150'},
    {'Nome_Excel': 'Rato SteelSeries Prime', 'Nome_JSON': 'SteelSeries Prime Wireless Mouse', 'ProductID': 'P151'},
    {'Nome_Excel': 'Teclado Logitech K780', 'Nome_JSON': 'Logitech K780 Multi-Device Keyboard', 'ProductID': 'P152'},
    {'Nome_Excel': 'Monitor 24 Polegadas Dell UltraSharp', 'Nome_JSON': 'Dell UltraSharp U2422H 24" Monitor', 'ProductID': 'P153'},
    {'Nome_Excel': 'Headset Bose SoundLink', 'Nome_JSON': 'Bose SoundLink Around-Ear Headphones', 'ProductID': 'P154'},
    {'Nome_Excel': 'Smartphone Oppo Reno 6', 'Nome_JSON': 'Oppo Reno 6 Pro Smartphone', 'ProductID': 'P155'},
    {'Nome_Excel': 'Rato Logitech G604', 'Nome_JSON': 'Logitech G604 Lightspeed Mouse', 'ProductID': 'P156'},
    {'Nome_Excel': 'Teclado Corsair Strafe RGB', 'Nome_JSON': 'Corsair Strafe RGB MK.2 Keyboard', 'ProductID': 'P157'},
    {'Nome_Excel': 'Monitor 28" Samsung Odyssey G7', 'Nome_JSON': 'Samsung Odyssey G7 28" Monitor', 'ProductID': 'P158'},
    {'Nome_Excel': 'Headset Razer Hammerhead', 'Nome_JSON': 'Razer Hammerhead True Wireless Earbuds', 'ProductID': 'P159'},
    {'Nome_Excel': 'Smartphone Samsung Galaxy S22', 'Nome_JSON': 'Samsung Galaxy S22 Smartphone', 'ProductID': 'P160'},
    {'Nome_Excel': 'Rato Razer Orochi V2', 'Nome_JSON': 'Razer Orochi V2 Mouse', 'ProductID': 'P161'},
    {'Nome_Excel': 'Teclado Ducky Mecha Mini', 'Nome_JSON': 'Ducky Mecha Mini Keyboard', 'ProductID': 'P162'},
    {'Nome_Excel': 'Monitor 24" AOC Gaming', 'Nome_JSON': 'AOC 24G2U 24" Monitor', 'ProductID': 'P163'},
    {'Nome_Excel': 'Headset Sony WH-1000XM4', 'Nome_JSON': 'Sony WH-1000XM4 Headphones', 'ProductID': 'P164'},
    {'Nome_Excel': 'Smartphone iPhone 14 Pro', 'Nome_JSON': 'Apple iPhone 14 Pro Smartphone', 'ProductID': 'P165'},
    {'Nome_Excel': 'Rato HyperX Pulsefire Surge', 'Nome_JSON': 'HyperX Pulsefire Surge Mouse', 'ProductID': 'P166'},
    {'Nome_Excel': 'Teclado Logitech G613', 'Nome_JSON': 'Logitech G613 Wireless Keyboard', 'ProductID': 'P167'},
    {'Nome_Excel': 'Monitor 27" LG UltraFine', 'Nome_JSON': 'LG 27GP950 27" Monitor', 'ProductID': 'P168'},
    {'Nome_Excel': 'Headset Corsair HS70', 'Nome_JSON': 'Corsair HS70 Pro Headset', 'ProductID': 'P169'},
    {'Nome_Excel': 'Smartphone Xiaomi 13', 'Nome_JSON': 'Xiaomi 13 Smartphone', 'ProductID': 'P170'},
    {'Nome_Excel': 'Rato SteelSeries Rival 5', 'Nome_JSON': 'SteelSeries Rival 5 Mouse', 'ProductID': 'P171'},
    {'Nome_Excel': 'Teclado Razer Pro Type', 'Nome_JSON': 'Razer Pro Type Ultra Keyboard', 'ProductID': 'P172'},
    {'Nome_Excel': 'Monitor 27" ASUS ProArt', 'Nome_JSON': 'ASUS ProArt PA278CV 27" Monitor', 'ProductID': 'P173'},
    {'Nome_Excel': 'Headset Sennheiser HD 560S', 'Nome_JSON': 'Sennheiser HD 560S Headphones', 'ProductID': 'P174'},
    {'Nome_Excel': 'Smartphone Google Pixel 7', 'Nome_JSON': 'Google Pixel 7 Smartphone', 'ProductID': 'P175'}
]
pd.DataFrame(equivalencia_produtos).to_csv('equivalencia_produtos.csv', index=False)