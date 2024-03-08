url = "https://www.sefaz.rs.gov.br/ASP/AAE_ROOT/NFE/SAT-WEB-NFE-NFC_2.asp"

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'ASPSESSIONIDAEBBSQDA=KNCNGPBBJAGLOFHEJBDNENFH; ASPSESSIONIDQEACBQCD=OKMMGNPAIPADLBOFPHCJOMOA; AffinitySefaz=c61190ec9eb1b57a94adfa63e4d1b9a40a8d78d52e453413a24e381e9f07bc6a'
}


default_datable = {
                        'NOTA':[],
                        'LOJA_NOME':[],
                        'LOJA_CNPJ':[],
                        'LOJA_INSC_EST':[],
                        'ENDERECO':[],
                        'TOTAL':[],
                        'TOTAL_DESC':[],
                        'TOTAL_PAGO':[],
                        'TOTAL_PAGAMENTO':[],
                        'NFe':[],
                        'NFe_SERIE':[],
                        'NFe_DATA':[],
                        'CONSUMIDOR':[],
                        # 'PRODUTOS':[],
                    }


error_msg = "Documento Fiscal (NFC-e) inexistente na base de dados da SEFAZ"

def payload(NFe):
    # Aqui o NFe tem que ser uma string
    return f'HML=false&chaveNFe={NFe.replace(" ","")}&Action=Avançar'

def extract_table(table):
    return [tr.text for tr in table.find_all('td')]