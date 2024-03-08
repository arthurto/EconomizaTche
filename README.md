# Economiza Tchê 

Nesse repo existe um script em python que baixa as notas fiscais registradas em seu CPF. 
Para isso você vai precisar da tabela em formato CSV que pode ser obtida no site `https://nfg.sefaz.rs.gov.br/`.
Nele você acessa a aba `Minhas Notas`, escolhe o intervalo de tempo que deseja ter as notas, e baixa em formato CSV. 

Depois de clonar esse repositório, basta executar o programa com o caminho para o arquivo como argumento posicional: 
bash```python main.py --filename '/home/user/Nota Fiscal Gaúcha.csv'```
Caso o argumento opcional não seja fornecido ele vai procurar pelo arquivo `Nota Fiscal Gaúcha.csv` no `cwd`. 

## Pending
- [ ] Requirements
- [ ] Dashboard de visualização de dados
- [ ] Melhorar as tabelas
