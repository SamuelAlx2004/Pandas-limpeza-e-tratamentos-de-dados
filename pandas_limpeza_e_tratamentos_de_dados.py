# -*- coding: utf-8 -*-
"""Pandas: limpeza e tratamentos de dados

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Oxzmwzc4J6Ih3jQ6qqkxBxvaUawWMCga
"""

import pandas as pd

dados = pd.read_json('/content/dataset-telecon.json')

dados.head()

import json

with open('dataset-telecon.json') as f:
  json_bruto = json.load(f)

json_normalizado = pd.json_normalize(json_bruto)

json_normalizado.head()

json_normalizado.info()

json_normalizado[json_normalizado['conta.cobranca.Total'] == ' '].head()

json_normalizado[json_normalizado['conta.cobranca.Total'] == ' '][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]

idx = json_normalizado[json_normalizado['conta.cobranca.Total'] == ' '].index

json_normalizado.loc[idx, "conta.cobranca.Total"] = json_normalizado.loc[idx, "conta.cobranca.mensal"] * 24

json_normalizado.loc[idx, "cliente.tempo_servico"] = 24

json_normalizado.loc[idx][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]

json_normalizado['conta.cobranca.Total'] = json_normalizado['conta.cobranca.Total'].astype(float)

json_normalizado.info()

for col in json_normalizado.columns:
    print(f"Coluna: {col}")
    print(json_normalizado[col].unique())
    print("-" * 30)

json_normalizado.query("Churn == ''")

dados_sem_vazio = json_normalizado[json_normalizado['Churn'] != ''].copy()

dados_sem_vazio.info()

dados_sem_vazio.reset_index(drop=True, inplace=True)

dados_sem_vazio

dados_sem_vazio.duplicated()

dados_sem_vazio.duplicated().sum()

filtro_duplicado = dados_sem_vazio.duplicated()

dados_sem_vazio[filtro_duplicado]

dados_sem_vazio.drop_duplicates(inplace=True)

dados_sem_vazio.duplicated().sum()

dados_sem_vazio.isna()

dados_sem_vazio.isna().sum()

dados_sem_vazio.isna().sum().sum()

dados_sem_vazio[dados_sem_vazio.isna().any(axis=1)]

filtro = dados_sem_vazio['cliente.tempo_servico'].isna()

dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

import numpy as np

np.ceil(5957.90/90.45)

dados_sem_vazio['cliente.tempo_servico'].fillna(
    np.ceil(
        dados_sem_vazio['conta.cobranca.Total'] / dados_sem_vazio['conta.cobranca.mensal']
    ), inplace=True
)

dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

dados_sem_vazio.isna().sum()

dados_sem_vazio['conta.contrato'].value_counts()

colunas_dropar = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']

dados_sem_vazio[colunas_dropar].isna().any(axis=1).sum()

df_sem_nulo = dados_sem_vazio.dropna(subset=colunas_dropar).copy()
df_sem_nulo.head()

df_sem_nulo.reset_index(drop=True, inplace=True)

df_sem_nulo.isna().sum()

df_sem_nulo.describe()

import seaborn as sns

sns.boxplot(x=df_sem_nulo['cliente.tempo_servico'])

Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulo['cliente.tempo_servico'].quantile(.75)
IQR = Q3-Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

outliers_flitro = (df_sem_nulo['cliente.tempo_servico'] < limite_inferior) | (df_sem_nulo['cliente.tempo_servico'] > limite_superior)

df_sem_nulo[outliers_flitro]['cliente.tempo_servico']

df_sem_out= df_sem_nulo.copy()

df_sem_out[outliers_flitro]['cliente.tempo_servico']

df_sem_out.loc[outliers_flitro, 'cliente.tempo_servico'] = np.ceil(
    df_sem_out.loc[outliers_flitro, 'conta.cobranca.Total'] /
    df_sem_out.loc[outliers_flitro, 'conta.cobranca.mensal']
)

sns.boxplot(x=df_sem_out['cliente.tempo_servico'])

df_sem_out [outliers_flitro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

Q1 = df_sem_out['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_out['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

outliers_index = (df_sem_out['cliente.tempo_servico'] < limite_inferior) | (df_sem_out['cliente.tempo_servico'] > limite_superior)
outliers_index

df_sem_out[outliers_index]

df_sem_out=df_sem_out[~outliers_index]
df_sem_out

sns.boxplot(x=df_sem_out['cliente.tempo_servico'])

df_sem_out.reset_index(drop=True, inplace=True)

