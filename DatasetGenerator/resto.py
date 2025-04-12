from faker import Faker
import pandas as pd
import random
import json
from datetime import datetime, timedelta

# Inicializar Faker
fake = Faker('pt_PT')

# Carregar os dados de clientes gerados anteriormente
df_clientes = pd.read_csv('clientes.csv')

# Gerar Tabela de Equivalência de Clientes
equivalencia_clientes = df_clientes[['Nome', 'Profissão', 'EstadoCivil', 'Sexo', 'Distrito', 'Concelho', 'DataNascimento', 'Email']].copy()
equivalencia_clientes['customer_id'] = [f'C{i+100}' for i in range(len(df_clientes))]
equivalencia_clientes.to_csv('equivalencia_clientes.csv', index=False)

# 2. Definir Produtos e Categorias (Expandido com Mais 150 Produtos)
# Produtos para a Loja Física (nomenclatura inconsistente, simulando registos manuais)
produtos_fisicos = [
    # Produtos já existentes
    'Rato Logitech MX Master', 'Logitech Rato MX Anywhere', 'Teclado Mecânico Corsair K70', 'Teclado Gaming Razer BlackWidow',
    'Monitor Dell 24"', 'Monitor 27 Polegadas HP', 'Headset Gamer HyperX Cloud', 'Headset Gaming SteelSeries Arctis',
    'Smartphone Samsung Galaxy S10', 'Smartphone Apple iPhone 11', 'Rato Razer DeathAdder', 'Teclado Logitech G Pro',
    'Monitor 24" Acer', 'Headset Logitech G432', 'Smartphone Xiaomi Redmi Note 9', 'Rato Corsair Dark Core',
    'Teclado Mecânico Ducky One 2', 'Monitor 32" LG', 'Headset Razer Kraken', 'Smartphone Huawei P30',
    'Rato SteelSeries Rival 3', 'Teclado Gaming Keychron K8', 'Monitor 27" ASUS', 'Headset Corsair Void Pro',
    'Smartphone Google Pixel 4', 'Rato HyperX Pulsefire', 'Teclado Logitech MX Keys', 'Monitor Dell UltraSharp 27"',
    'Headset Sennheiser HD 450BT', 'Smartphone Samsung Galaxy A51', 'Rato Logitech G502', 'Teclado Razer Huntsman',
    'Monitor 24 Polegadas Samsung', 'Headset SteelSeries Siberia', 'Smartphone iPhone 12',
    # Novos produtos (150 adicionais)
    'Rato Logitech G203', 'Teclado Corsair K55', 'Monitor 22" AOC', 'Headset JBL Quantum 100', 'Smartphone Samsung Galaxy S20',
    'Rato Razer Viper', 'Teclado Mecânico Redragon K552', 'Monitor 27 Polegadas LG', 'Headset Logitech G Pro X', 'Smartphone iPhone 13',
    'Rato Corsair Harpoon', 'Teclado Gaming SteelSeries Apex 5', 'Monitor 24" BenQ', 'Headset HyperX Cloud Stinger', 'Smartphone Xiaomi 11T',
    'Rato SteelSeries Aerox 3', 'Teclado Logitech K380', 'Monitor 32 Polegadas Dell', 'Headset Razer BlackShark V2', 'Smartphone Huawei Mate 40',
    'Rato HyperX Pulsefire Dart', 'Teclado Ducky Shine 7', 'Monitor 27" Acer Predator', 'Headset Corsair HS60', 'Smartphone Google Pixel 5',
    'Rato Logitech G305', 'Teclado Razer Ornata V2', 'Monitor 24 Polegadas HP', 'Headset Sennheiser GSP 300', 'Smartphone Samsung Galaxy Note 20',
    'Webcam Logitech C920', 'Placa Gráfica NVIDIA RTX 3060', 'SSD Samsung 970 EVO 1TB', 'Impressora HP DeskJet 2720', 'Smartwatch Apple Watch Series 6',
    'Webcam Razer Kiyo', 'Placa Gráfica ASUS RTX 3070', 'SSD Kingston A2000 500GB', 'Impressora Epson EcoTank L3150', 'Smartwatch Samsung Galaxy Watch 4',
    'Rato Microsoft Surface Precision', 'Teclado Mecânico Kinesis Freestyle', 'Monitor 34" LG UltraWide', 'Headset Bose QuietComfort 35', 'Smartphone OnePlus 9',
    'Rato ASUS ROG Chakram', 'Teclado Gaming Cooler Master CK552', 'Monitor 27 Polegadas MSI', 'Headset Sony WH-CH710N', 'Smartphone Oppo Find X3',
    'Webcam Logitech StreamCam', 'Placa Gráfica MSI RTX 3080', 'SSD Crucial MX500 1TB', 'Impressora Canon PIXMA G6020', 'Smartwatch Huawei Watch GT 3',
    'Rato HP Spectre 700', 'Teclado Logitech Craft', 'Monitor 24" Philips', 'Headset JBL Live 650BTNC', 'Smartphone Vivo Y70',
    'Rato Corsair Scimitar', 'Teclado Gaming Anne Pro 2', 'Monitor 32" Samsung Odyssey G5', 'Headset SteelSeries Arctis 9', 'Smartphone Nokia 8.3',
    'Webcam Microsoft LifeCam HD', 'Placa Gráfica Gigabyte RTX 3060 Ti', 'SSD WD Blue SN550 1TB', 'Impressora Brother HL-L2350DW', 'Smartwatch Fitbit Versa 3',
    'Rato Razer Basilisk V3', 'Teclado Corsair K100 RGB', 'Monitor 27" Dell Alienware', 'Headset HyperX Cloud Alpha', 'Smartphone Samsung Galaxy Z Fold 3',
    'Rato Logitech G703', 'Teclado Gaming G.Skill Ripjaws KM570', 'Monitor 24 Polegadas ASUS ROG', 'Headset Razer Barracuda X', 'Smartphone iPhone 14',
    'Webcam Logitech Brio', 'Placa Gráfica NVIDIA GTX 1660 Super', 'SSD Samsung 980 Pro 2TB', 'Impressora HP LaserJet Pro M15w', 'Smartwatch Garmin Forerunner 245',
    'Rato SteelSeries Sensei 310', 'Teclado Ducky One 3', 'Monitor 27 Polegadas AOC Agon', 'Headset Corsair Virtuoso RGB', 'Smartphone Xiaomi 12',
    'Rato HyperX Pulsefire Haste', 'Teclado Logitech G915 TKL', 'Monitor 32" HP Omen', 'Headset Sennheiser Momentum 3', 'Smartphone Google Pixel 6',
    'Rato Corsair Katar Pro', 'Teclado Gaming Razer Cynosa V2', 'Monitor 24" LG UltraGear', 'Headset SteelSeries Arctis 1', 'Smartphone Huawei P40',
    'Webcam Razer Kiyo Pro', 'Placa Gráfica ASUS TUF RTX 3090', 'SSD Kingston NV2 1TB', 'Impressora Epson WorkForce WF-110', 'Smartwatch Apple Watch Series 7',
    'Rato Logitech MX Vertical', 'Teclado Corsair K65 Mini', 'Monitor 27" BenQ Mobiuz', 'Headset JBL Quantum 400', 'Smartphone Samsung Galaxy S21',
    'Rato Razer Naga Pro', 'Teclado Gaming Keychron K4', 'Monitor 32 Polegadas Acer', 'Headset HyperX Cloud Flight', 'Smartphone OnePlus 10 Pro',
    'Rato SteelSeries Prime', 'Teclado Logitech K780', 'Monitor 24 Polegadas Dell UltraSharp', 'Headset Bose SoundLink', 'Smartphone Oppo Reno 6'
]
categorias_fisicas = [
    'Acessórios de Computador', 'Monitores e Ecrãs', 'Smartphones e Tablets', 'Áudio e Headsets', 'Teclados Gaming',
    'Webcams', 'Placas Gráficas', 'Armazenamento SSD', 'Impressoras', 'Smartwatches'
]

# Produtos para a Loja Online (nomenclatura mais padronizada, simulando sistema de e-commerce)
produtos_online = [
    # Produtos já existentes
    'Logitech MX Master 3 Mouse', 'Logitech MX Anywhere 3 Mouse', 'Corsair K70 RGB MK.2 Keyboard', 'Razer BlackWidow V3 Keyboard',
    'Dell S2421HGF 24" Monitor', 'HP 27f 27" Monitor', 'HyperX Cloud II Headset', 'SteelSeries Arctis 7 Headset',
    'Samsung Galaxy S10 Smartphone', 'Apple iPhone 11 Smartphone', 'Razer DeathAdder V2 Mouse', 'Logitech G Pro X Keyboard',
    'Acer Nitro VG240Y 24" Monitor', 'Logitech G432 Gaming Headset', 'Xiaomi Redmi Note 9 Smartphone', 'Corsair Dark Core RGB Mouse',
    'Ducky One 2 Mini Keyboard', 'LG 32UN500 32" Monitor', 'Razer Kraken X Headset', 'Huawei P30 Smartphone',
    'SteelSeries Rival 3 Mouse', 'Keychron K8 Wireless Keyboard', 'ASUS TUF Gaming VG27AQ 27" Monitor', 'Corsair Void Elite RGB Headset',
    'Google Pixel 4 Smartphone', 'HyperX Pulsefire FPS Pro Mouse', 'Logitech MX Keys Advanced Keyboard', 'Dell UltraSharp U2720Q 27" Monitor',
    'Sennheiser HD 450BT Headphones', 'Samsung Galaxy A51 Smartphone', 'Logitech G502 Hero Mouse', 'Razer Huntsman Elite Keyboard',
    'Samsung S24F350 24" Monitor', 'SteelSeries Arctis 5 Headset', 'Apple iPhone 12 Smartphone',
    'Logitech G Pro Wireless Mouse', 'Corsair K95 RGB Platinum Keyboard', 'AOC CQ32G1 32" Monitor', 'Razer Nari Ultimate Headset',
    'Samsung Galaxy S20 Smartphone', 'Apple iPhone 13 Smartphone',
    # Novos produtos (150 adicionais)
    'Logitech G203 Lightsync Mouse', 'Corsair K55 RGB Keyboard', 'AOC 22V2H 22" Monitor', 'JBL Quantum 100 Headset', 'Samsung Galaxy S20 Smartphone',
    'Razer Viper Ultimate Mouse', 'Redragon K552 Kumara Keyboard', 'LG 27QN600 27" Monitor', 'Logitech G Pro X Headset', 'Apple iPhone 13 Smartphone',
    'Corsair Harpoon RGB Mouse', 'SteelSeries Apex 5 Keyboard', 'BenQ Zowie XL2411P 24" Monitor', 'HyperX Cloud Stinger Core Headset', 'Xiaomi 11T Pro Smartphone',
    'SteelSeries Aerox 3 Wireless Mouse', 'Logitech K380 Bluetooth Keyboard', 'Dell P3221D 32" Monitor', 'Razer BlackShark V2 X Headset', 'Huawei Mate 40 Pro Smartphone',
    'HyperX Pulsefire Dart Mouse', 'Ducky Shine 7 Keyboard', 'Acer Predator XB273U 27" Monitor', 'Corsair HS60 Pro Headset', 'Google Pixel 5 Smartphone',
    'Logitech G305 Lightspeed Mouse', 'Razer Ornata V2 Keyboard', 'HP 24mh 24" Monitor', 'Sennheiser GSP 300 Headset', 'Samsung Galaxy Note 20 Ultra Smartphone',
    'Logitech C920 HD Pro Webcam', 'NVIDIA GeForce RTX 3060 Graphics Card', 'Samsung 970 EVO Plus 1TB SSD', 'HP DeskJet 2720 Printer', 'Apple Watch Series 6 Smartwatch',
    'Razer Kiyo Streaming Webcam', 'ASUS ROG Strix RTX 3070 Graphics Card', 'Kingston A2000 500GB SSD', 'Epson EcoTank L3150 Printer', 'Samsung Galaxy Watch 4 Smartwatch',
    'Microsoft Surface Precision Mouse', 'Kinesis Freestyle Edge Keyboard', 'LG 34WN80C 34" UltraWide Monitor', 'Bose QuietComfort 35 II Headphones', 'OnePlus 9 Smartphone',
    'ASUS ROG Chakram Mouse', 'Cooler Master CK552 Keyboard', 'MSI Optix MAG272CQR 27" Monitor', 'Sony WH-CH710N Headphones', 'Oppo Find X3 Pro Smartphone',
    'Logitech StreamCam Webcam', 'MSI GeForce RTX 3080 Graphics Card', 'Crucial MX500 1TB SSD', 'Canon PIXMA G6020 Printer', 'Huawei Watch GT 3 Smartwatch',
    'HP Spectre 700 Mouse', 'Logitech Craft Advanced Keyboard', 'Philips 243V7Q 24" Monitor', 'JBL Live 650BTNC Headphones', 'Vivo Y70 Smartphone',
    'Corsair Scimitar RGB Elite Mouse', 'Anne Pro 2 Keyboard', 'Samsung Odyssey G5 32" Monitor', 'SteelSeries Arctis 9 Wireless Headset', 'Nokia 8.3 5G Smartphone',
    'Microsoft LifeCam HD-3000 Webcam', 'Gigabyte RTX 3060 Ti Graphics Card', 'WD Blue SN550 1TB SSD', 'Brother HL-L2350DW Printer', 'Fitbit Versa 3 Smartwatch',
    'Razer Basilisk V3 Mouse', 'Corsair K100 RGB Optical Keyboard', 'Dell Alienware AW2721D 27" Monitor', 'HyperX Cloud Alpha S Headset', 'Samsung Galaxy Z Fold 3 Smartphone',
    'Logitech G703 Lightspeed Mouse', 'G.Skill Ripjaws KM570 Keyboard', 'ASUS ROG Swift PG259QN 24" Monitor', 'Razer Barracuda X Headset', 'Apple iPhone 14 Smartphone',
    'Logitech Brio Ultra HD Webcam', 'NVIDIA GTX 1660 Super Graphics Card', 'Samsung 980 Pro 2TB SSD', 'HP LaserJet Pro M15w Printer', 'Garmin Forerunner 245 Smartwatch',
    'SteelSeries Sensei 310 Mouse', 'Ducky One 3 Matcha Keyboard', 'AOC Agon AG273QCG 27" Monitor', 'Corsair Virtuoso RGB Wireless Headset', 'Xiaomi 12 Pro Smartphone',
    'HyperX Pulsefire Haste Mouse', 'Logitech G915 TKL Lightspeed Keyboard', 'HP Omen 32" Monitor', 'Sennheiser Momentum 3 Wireless Headphones', 'Google Pixel 6 Pro Smartphone',
    'Corsair Katar Pro XT Mouse', 'Razer Cynosa V2 Keyboard', 'LG UltraGear 24GN600 24" Monitor', 'SteelSeries Arctis 1 Wireless Headset', 'Huawei P40 Pro Smartphone',
    'Razer Kiyo Pro Ultra Webcam', 'ASUS TUF Gaming RTX 3090 Graphics Card', 'Kingston NV2 1TB SSD', 'Epson WorkForce WF-110 Printer', 'Apple Watch Series 7 Smartwatch',
    'Logitech MX Vertical Mouse', 'Corsair K65 RGB Mini Keyboard', 'BenQ Mobiuz EX2710 27" Monitor', 'JBL Quantum 400 Headset', 'Samsung Galaxy S21 Ultra Smartphone',
    'Razer Naga Pro Mouse', 'Keychron K4 Wireless Keyboard', 'Acer 32" Predator XB323U Monitor', 'HyperX Cloud Flight Wireless Headset', 'OnePlus 10 Pro Smartphone',
    'SteelSeries Prime Wireless Mouse', 'Logitech K780 Multi-Device Keyboard', 'Dell UltraSharp U2422H 24" Monitor', 'Bose SoundLink Around-Ear Headphones', 'Oppo Reno 6 Pro Smartphone',
    'Logitech G604 Lightspeed Mouse', 'Corsair Strafe RGB MK.2 Keyboard', 'Samsung Odyssey G7 28" Monitor', 'Razer Hammerhead True Wireless Earbuds', 'Samsung Galaxy S22 Smartphone',
    'Razer Orochi V2 Mouse', 'Ducky Mecha Mini Keyboard', 'AOC 24G2U 24" Monitor', 'Sony WH-1000XM4 Headphones', 'Apple iPhone 14 Pro Smartphone',
    'HyperX Pulsefire Surge Mouse', 'Logitech G613 Wireless Keyboard', 'LG 27GP950 27" Monitor', 'Corsair HS70 Pro Headset', 'Xiaomi 13 Smartphone',
    'SteelSeries Rival 5 Mouse', 'Razer Pro Type Ultra Keyboard', 'ASUS ProArt PA278CV 27" Monitor', 'Sennheiser HD 560S Headphones', 'Google Pixel 7 Smartphone'
]
categorias_online = [
    'Gaming Mice', 'Mechanical Keyboards', 'Gaming Monitors', 'Headsets', 'Smartphones',
    'Webcams', 'Graphics Cards', 'SSDs', 'Printers', 'Smartwatches', 'Wireless Earbuds', 'Professional Monitors'
]

# 3. Gerar Registos da Loja Física (Fonte 1: Excel)
vendas_fisicas = []
for i in range(5000):  # 5.000 transações entre 2010 e 2020
    data = fake.date_between_dates(date_start=datetime(2010, 1, 1), date_end=datetime(2020, 12, 31))
    cliente = equivalencia_clientes.iloc[random.randint(0, len(equivalencia_clientes)-1)]
    venda = {
        'Data_Venda': data.strftime('%d/%m/%Y'),
        'Produto': random.choice(produtos_fisicos),
        'Categoria': random.choice(categorias_fisicas),
        'Quantidade': random.randint(1, 5),
        'Preço': round(random.uniform(20, 1500), 2),  # Aumentei o intervalo para incluir produtos mais caros
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
    venda = {
        'sale_id': f'S{i+1000}',
        'date': data.strftime('%Y-%m-%d'),
        'products': [{
            'product_id': f'P{random.randint(1, 1000)}',
            'name': random.choice(produtos_online),
            'category': random.choice(categorias_online),
            'price': round(random.uniform(20, 1500), 2),
            'quantity': random.randint(1, 5)
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