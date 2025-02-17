from datetime import datetime
import json
import os
from random import random
from sys import argv
import time

import pandas as pd 
import requests
import seaborn as sns

# # URL da API do BC para taxa CDI 
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Extrair taxa CDI 
def extrair_taxa_cdi(): 
    try: 
        response = requests.get(url=URL)
        response.raise_for_status()
    except requests.HTTPError as exc: 
        print('Dado não encontrado.')
        return None
    except Exception as exc: 
        print('Erro')
        raise exc 
    else: 
        return json.loads(response.text)[-1]['valor']
    
# Gerar e salvar CSV com dados da CDI 
def gerar_csv(): 
    dado = extrair_taxa_cdi()

    for _ in range(0,100): 
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        cdi = float(dado) + (random() - 0.5)

        if not os.path.exists('./taxa-cdi.csv'): 
            with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp: 
                fp.write('data,hora,taxa\n')

        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp: 
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(0.1)
    
    print('CSV gerado.')

def gerar_grafico(nome_grafico): 
    df = pd.read_csv('./taxa-cdi.csv')

    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_grafico}.png")
    print('Sucesso')

def main(): 
    if len(argv) < 2: 
        print('Insira um nome para o grafico')
        return 
    
    nome_grafico = argv[1] 

    gerar_csv()
    gerar_grafico(nome_grafico)

if __name__ == '__main__': 
    main()