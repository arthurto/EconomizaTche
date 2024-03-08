import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from nota_fiscal import *
import argparse
from os import getcwd

def parsing():
    # Parssando os argumentos, tchê!
    parser = argparse.ArgumentParser(
        prog="Economiza, Tchê!",
        description="Importa as notas fiscais a partir do CSV com as chaves"
    )
    
    # Definindo o 'filename' padrão, tchê!
    parser.add_argument(
        '--filename',help="path to file",
        default=f"{getcwd()}/Nota Fiscal Gaúcha.csv")
    return parser.parse_args()

def get_chaves(args):
    # pi pi pi pi pi pi 
    tabela = pd.read_csv(args.filename)
    return tabela["Chave de Acesso"]


def main():

    args = parsing()
    
    chaves = get_chaves(args)

    df = pd.DataFrame(default_datable) # Criando um data frame vazio
    
    for chave in chaves:
        # faz o request
        request = requests.post(url,data=payload(chave),headers=headers)

        # Checa se teve retorno 
        if error_msg in request.text:
            # Se falhar, tenta dnv! 
            request = requests.post(url,data=payload(chave),headers=headers)
            
            if error_msg in request.text: 
                # Já tentou duas vezes, agora desiste.
                 
                df = pd.concat([df,pd.DataFrame({
                                    'NOTA':[None],
                                    'LOJA':[None],
                                    'ENDERECO':[None],
                                    'TOTAL':[None],
                                    'NFe':[None],
                                    'CONSUMIDOR':[None],
                                    'PRODUTOS':[None]
                                })])
                print(f"NFe CHAVE {chave} FALHOU!")
                continue
        print(f"NFe CHAVE {chave} foi obtida!")
        soup = BeautifulSoup(request.text,'html.parser')

        table_nfce = soup.findAll('table')

        # Agora a lógica para organizar os dados 
        # das tabelas para preencher o DataFrame

        loja = extract_table(table_nfce[4])
        pattern = re.compile(r'CNPJ:\s*([\d\.\/\-]+)\s*Inscrição Estadual:\s*(\d+)')
        mtch = pattern.search(loja[2])
        loja = {
                'nome':loja[1],
                'cnpj':mtch.group(1),
                'inscricao_estadual':mtch.group(2),
                }

        endereco = extract_table(table_nfce[5])
        endereco = endereco[0].replace(" ","").replace(",\\n",' ')

        meta_data = extract_table(table_nfce[7])
        meta_data = meta_data[0].split("\n")
        meta_data = {
            'nfe':meta_data[1].strip()[10:],
            'serie':meta_data[2].strip()[7:],
            'datetime':meta_data[3].strip()[17:],
            }
        consumidor = extract_table(table_nfce[8])[1].split('\n')[2].strip()

        produtos = extract_table(table_nfce[9])
        produtos = [produtos[(1+i)*6:(2+i)*6] for i in range(len(produtos)//6-1)]
        produtos = [
            {
                'codigo':produto[0],
                'descricao':produto[1],
                'quantidade':produto[2],
                'unindades':produto[3],
                'valor_unidade':produto[4],
                'valor_total':produto[5],
                }
                for produto in produtos
        ]

        total = extract_table(table_nfce[10])
        total = {
                "valor_total":total[1],
                "desconto":total[3],
                "forma_pagamento":total[6],
                "valor_pago":total[7]
        }

        df = pd.concat([df,pd.DataFrame({
                            'NOTA':[chave],
                            'LOJA':[loja],
                            'ENDERECO':[endereco],
                            'TOTAL':[total],
                            'NFe':[meta_data],
                            'CONSUMIDOR':[consumidor],
                            'PRODUTOS':[produtos]
                        })])
    df.to_csv("data.csv")

if __name__ == "__main__":
    main()