# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import sqlite3 as sqlite

# Carrega o dataset
df_dsa = pd.read_csv('dados/dataset.csv')

# Amostra dos dados
df_dsa.head()

# Colunas do conjunto de dados
df_dsa.columns

# Verificando o tipo de dado de cada coluna
df_dsa.dtypes

# Resumo estatístico da coluna com o valor de venda
df_dsa['Valor_Venda'].describe()

# Verificando se há registros duplicados
df_dsa[df_dsa.duplicated()]

# Verificando de há valores ausentes
df_dsa.isnull().sum()

#PERGUNTAS DE NEGÓCIO
## Pergunta de Negócio 1:

### Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?

agrupado = df_dsa.groupby(['Cidade', 'Categoria'])[['Valor_Venda']].sum().reset_index()
resultado = agrupado[agrupado['Categoria'] == 'Office Supplies']
resultado = resultado.sort_values(by='Valor_Venda',ascending=False)
print(resultado.loc[736])

## Pergunta de Negócio 2:
### Qual o Total de Vendas Por Data do Pedido? Demonstre o resultado através de um gráfico de barras.

df_dsa['Data_Pedido'] = pd.to_datetime(df_dsa['Data_Pedido'], format="%d/%m/%Y")
data_vendas = df_dsa.groupby(['Data_Pedido']).sum()
data_order = data_vendas.sort_values('Data_Pedido')
print(data_order)
plt.figure(figsize=(10, 6))
plt.bar(data_order.index, data_order['Valor_Venda'], color='blue')
plt.xlabel('Data do Pedido')
plt.ylabel('Total de Vendas')
plt.title('Total de Vendas por Data do Pedido')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## Pergunta de Negócio 3:
### Qual o Total de Vendas por Estado? Demonstre o resultado através de um gráfico de barras.

query_2 = df_dsa.groupby(by='Estado').sum()
plt.figure(figsize=(15, 6))
plt.bar(query_2.index, query_2['Valor_Venda'], color = 'red')
plt.title('Total de Vendas por Estado')
plt.ylabel('Vendas')
plt.xticks(rotation=70)
plt.tight_layout()
plt.show()

## Pergunta de Negócio 4:
# ### Quais São as 10 Cidades com Maior Total de Vendas? Demonstre o resultado através de um gráfico de barras.

dados = df_dsa.groupby('Cidade').sum().sort_values(by='Valor_Venda', ascending=False).head(10)
plt.figure(figsize=(10,8))
sns.barplot(data=dados,x='Valor_Venda',y=dados.index).set_title('Venda por Cidade')
sns.set_palette("light:#5A9")
plt.xticks(rotation = 0)
plt.xlabel('Valor Vendido')
plt.show()

## Pergunta de Negócio 5:
# ### Qual Segmento Teve o Maior Total de Vendas? Demonstre o resultado através de um gráfico de pizza.

pizza = df_dsa.groupby(['Segmento']).sum()
plt.figure(figsize=(7,7))
plt.pie(x=pizza['Valor_Venda'],labels=pizza.index, autopct='%1.1f%%')
plt.title('Vendas por Segmento')
plt.legend()

centre_circle = plt.Circle((0, 0), 0.82, fc = 'white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)


plt.annotate(text = 'Total de Vendas: ' + '$ ' + str(int(sum(pizza['Valor_Venda']))), xy = (-0.25, 0))
plt.title('Total de Vendas Por Segmento')
plt.show()

## Pergunta de Negócio 6: 
# ### Qual o Total de Vendas Por Segmento e Por Ano?

df_dsa['Data_Pedido'] = pd.to_datetime(df_dsa['Data_Pedido'], format="%Y-%m-%d")
df_dsa['Ano_Pedido'] = df_dsa['Data_Pedido'].dt.year
p6 = df_dsa.groupby(['Ano_Pedido', 'Segmento']).sum().reset_index()
p6_consumer = p6[p6['Segmento'] == 'Consumer']
p6_corporate = p6[p6['Segmento'] == 'Corporate']
p6_office = p6[p6['Segmento'] == 'Home Office']
plt.figure(figsize=(10,7))
bars1 = plt.bar(p6_consumer['Ano_Pedido'].astype(str), p6_consumer['Valor_Venda'], color = 'indigo', label = 'Consumer')
bars2 = plt.bar(p6_corporate['Ano_Pedido'].astype(str), p6_corporate['Valor_Venda'], color = 'darkviolet', label = 'Corporate')
bars3 = plt.bar(p6_office['Ano_Pedido'].astype(str), p6_office['Valor_Venda'], color = 'violet', label = 'Home Office')
for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom', color='black', fontsize=10)

for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom', color='white', fontsize=10)

for bar in bars3:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}', ha='center', va='bottom', color='white', fontsize=10)
plt.legend()
plt.show()

## Pergunta de Negócio 7:

#Os gestores da empresa estão considerando conceder diferentes faixas de descontos e gostariam de fazer uma simulação com base na regra abaixo:

#- Se o Valor_Venda for maior que 1000 recebe 15% de desconto.
#- Se o Valor_Venda for menor que 1000 recebe 10% de desconto.

### Quantas Vendas Receberiam 15% de Desconto?

df_dsa['Desconto'] = np.where(df_dsa['Valor_Venda'] < 1000, 0.1, 0.15)
df_dsa['Desconto'].value_counts()

## Pergunta de Negócio 8 (Desafio Nível Master):
### Considere Que a Empresa Decida Conceder o Desconto de 15% do Item Anterior. Qual Seria a Média do Valor de Venda Antes e Depois do Desconto?

df_dsa['Valor_Venda_Desconto'] = df_dsa['Valor_Venda'] - (df_dsa['Valor_Venda'] * df_dsa['Desconto'])
filter_b_disc = df_dsa.loc[df_dsa['Desconto'] == 0.15, 'Valor_Venda']
filter_a_disc = df_dsa.loc[df_dsa['Desconto'] == 0.15, 'Valor_Venda_Desconto']

mean_b_disc = filter_b_disc.mean()
mean_a_disc = filter_a_disc.mean()

print('Sales mean after the discount: $ ', round(mean_a_disc, 2))
print('Sales mean before the discount: $ ', round(mean_b_disc,2))
df_dsa

## Pergunta de Negócio 9 (Desafio Nível Master Ninja):
### Qual o Média de Vendas Por Segmento, Por Ano e Por Mês? Demonstre o resultado através de gráfico de linha.

df_dsa['Mes'] = df_dsa['Data_Pedido'].dt.month
df_dsa_p9 = df_dsa.groupby(['Ano_Pedido', 'Mes', 'Segmento'])['Valor_Venda'].agg([np.sum, np.mean, np.median])

year = df_dsa_p9.index.get_level_values(0)
month = df_dsa_p9.index.get_level_values(1)
seg = df_dsa_p9.index.get_level_values(2)

plt.figure(figsize=(12,9))
sns.set()
sns.relplot(data=df_dsa_p9,
            kind='line',
            x=month,
            y='mean',
            hue=seg,
            col=year,
            col_wrap= 4)
plt.show()

## Pergunta de Negócio 10 (Desafio Nível Master Ninja das Galáxias):

### Qual o Total de Vendas Por Categoria e SubCategoria, Considerando Somente as Top 12 SubCategorias? Demonstre tudo através de um único gráfico.

df_dsa_p10 = df_dsa.groupby(['Categoria', 'SubCategoria']).sum(numeric_only=True).sort_values(by='Valor_Venda', ascending=False).head(12)
df_dsa_p10_cat = df_dsa_p10.groupby(['Categoria']).sum(numeric_only=True).reset_index()
df_dsa_p10 = df_dsa_p10[['Valor_Venda']].astype(int).sort_values(by='Categoria').reset_index()

cores_categorias = ['#5d00de',
                    '#0ee84f',
                    '#e80e27']
cores_subcategorias = ['#aa8cd4',
                       '#aa8cd4',
                       '#aa8cd4',
                       '#aa8cd4',
                       '#26c957',
                       '#26c957',
                       '#26c957',
                       '#26c957',
                       '#e65e65',
                       '#e65e65',
                       '#e65e65',
                       '#e65e65']

fig, ax = plt.subplots(figsize = (18,12))
p1 = ax.pie(df_dsa_p10_cat['Valor_Venda'],
              labels=df_dsa_p10_cat['Categoria'],
              radius= 1,
              colors = cores_categorias,
              wedgeprops= dict(edgecolor = 'white'))

p2 = ax.pie(df_dsa_p10['Valor_Venda'],
            radius = 0.9,
            labels = df_dsa_p10['SubCategoria'],
            labeldistance = 0.7,
            autopct='%1.1f%%',
            colors = cores_subcategorias,
            wedgeprops = dict(edgecolor = 'white'), 
            rotatelabels = True)

centre_circle = plt.Circle((0, 0), 0.6, fc = 'white')

fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.annotate(text = 'Total de Vendas: ' + '$ ' + str(int(sum(df_dsa_p10['Valor_Venda']))), xy = (-0.2, 0))
plt.title('Total de Vendas Por Categoria e Top 12 SubCategorias')
plt.show()