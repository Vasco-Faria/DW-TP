# Sistema de Suporte à Decisão - Perifericum 🛠️📊

Este repositório contém os principais artefatos desenvolvidos no âmbito do projeto de Data Warehouse para a loja de eletrónica **Perifericum**, realizado no contexto do perfil de **Sistemas de Armazéns de Dados** do Mestrado em Engenharia Informática da Universidade do Minho.

---

## 📈 Avaliação por Componentes

| Componente                                                             | Nota      |
|-----------------------------------------------------------------------|-----------|
| Conceção e Implementação de Armazéns de Dados                         | **18 valores** |
| Sistemas de Extração, Transformação e Carregamento de Dados (ETL)     | **17 valores** |
| Aquisição de Conhecimento em Armazéns de Dados                        | *Por atribuir* |

---

## 📌 Objetivo

Desenvolver um sistema de suporte à decisão com foco na **caracterização de perfis de clientes** e **personalização de ofertas**, utilizando um **Data Warehouse** baseado na metodologia **Kimball** e integrando ferramentas como **Apache NiFi**, **MySQL**, **Power BI**, **Pandas** e **Scikit-learn**.

---

## 🔄 Pipeline ETL

O processo de integração de dados foi realizado com o **Apache NiFi**, permitindo a ingestão de dados de múltiplas fontes:

- 📁 Excel: vendas físicas (2010–2020)
- 🧾 JSON: vendas online (2021–2025), catálogo de produtos
- 🗃️ MySQL: base de clientes

O ficheiro `Projeto_SDW_nifi.json` contém a pipeline completa para:

- Extração e limpeza de dados
- Mapeamento por tabelas de equivalência
- Carregamento incremental no DW (modelo em estrela)
  
---

## 🧠 Análise de Dados

A pasta `analysis/` inclui:

- Segmentação de clientes com **K-Means**
- Análise RFM
- Visualização da distribuição de clusters
- Identificação de perfis de cliente (leal, ocasional, em risco)


---

## 👥 Equipa

- António Silva — PG57867  
- David Teixeira — PG55929  
- Duarte Leitão — PG57872  
- João Pedro Pastore — PG55963  
- Vasco Faria — PG57905  

---

## 📌 Notas Finais

Este projeto foi desenvolvido com fins académicos e demonstra uma solução completa de integração, análise e visualização de dados para apoio à decisão estratégica num contexto de retalho tecnológico.
