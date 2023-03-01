# 03/01/2023 - Lucas Garzuze Cordeiro
import re
# Extrai os dados do Registro Digital de Urna (RDV) da sessão em que voto, para
# fazer análises. zona: 003, seção 0683

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

pattern = re.compile(pattern="\[(.*?)\]")

votes = []

for line in contents:
    if 'branco' in line:
        votes.append({'voto': 'branco', 'quantidade': 1})
    if 'nulo' in line:
        votes.append({'voto': 'nulo', 'quantidade': 1})
    if 'nominal' in line:
        vote = re.findall(pattern=pattern, string=line)[0]
        votes.append({'voto': f"{vote}", 'quantidade': 1})

for vote in votes:
    print(vote)