# 03/01/2023 - Lucas Garzuze Cordeiro

import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Extrai os dados do Registro Digital de Urna (RDV) da sessão em que voto, para
# criar gráficos com o resultado. Zona: 003, seção 0683

# Códigos usados no terminal para descriptografar o arquivo
# curl https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/developnotebooks/2022_11_29/rdv.py -o rdv.py
# pip install asn1crypto==1.5.1
# python rdv.py -r o00407-7535300030683.rdv > rdv.txt

# Limpeza dos dados

contents = []

with open(file='rdv.txt', mode='r') as fp:
    for line in fp.readlines():
        if "Governador" in line:
            break # Vou pegar apenas os votos para presidente
        else:
            contents.append(line)

# Extração dos dados

# Criando pattern no regex para filtrar os votos para cada candidato
pattern = re.compile(pattern="\[(.*?)\]")

votes = []

# Definindo o que fazer dependendo da linha
for line in contents:
    if 'branco' in line:
        votes.append({'voto': 'branco', 'quantidade': 1})
    if 'nulo' in line:
        votes.append({'voto': 'nulo', 'quantidade': 1})
    if 'nominal' in line:
        # Acha qual o número que está dentro dos colchetes
        vote = re.findall(pattern=pattern, string=line)[0]
        votes.append({'voto': f"{vote}", 'quantidade': 1})

 
# Processamento

# Criando DataFrame com o Pandas
votes_table = pd.DataFrame(votes)
votes_table.to_csv("rdv.csv", header=True, index=False)

# Agregação

# Criando uma tabela agregada que faz uma soma dos votos de cada candidato
votes_table_agg = votes_table.groupby('voto').agg('sum').reset_index()

# Organizando os votos por ordem decrescente
votes_table_agg = votes_table_agg.sort_values(by='quantidade', ascending=False)

# Criando uma coluna com o percentual de cada candidato
# Pegamos a quantidade de voto para cada candidato e dividimos pela soma de
# todos os votos, depois multiplicamos esse valor por 100.
votes_table_agg['percentual'] = round(100*(votes_table_agg['quantidade'] /
                                        votes_table_agg['quantidade'].sum()), 2)


# Visualização

def create_plot(y_column='quantidade', y_label='Quantidade'):
    """
    Cria o gráfico de barras com o resultado da urna
    Pode ser tanto com a coluna y sendo valores absolutos quanto percentuais    
    """

    URNA = "Curitiba/PR - zona: 003 - seção 0683"

    title = f"Votação para presidente - Segundo turno 2022 - {URNA}"
    x_label = 'Voto'
    x_column = 'voto'

    with sns.axes_style('whitegrid'):
        chart = sns.barplot(data=votes_table_agg, x=x_column, y=y_column)
        chart.set(title=title, xlabel=x_label, ylabel=y_label)

    plt.show()

while True:
    option = int(input("Bem vindo a visualização de dados da urna! Digite:\n"
                        "1 para verificar os dados absolutos\n"
                        "2 para verificar os dados percentuais\n"
                        "0 para sair: "))
    
    if option == 1:
        create_plot()
    elif option == 2:
        create_plot(y_column='percentual', y_label='Quantidade percentual')
    elif option == 0:
        break
