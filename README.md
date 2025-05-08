# Dados de Remuneração de Docentes - Tratamento para N8N

Este repositório contém os scripts e arquivos necessários para o tratamento dos dados de remuneração de docentes do Nordeste em 2020, preparando-os para uso pelo agente N8N.

## Estrutura do Repositório

- **datasets/**: Pasta contendo os arquivos de dados originais e processados

  - `Remuneracao_docentes_Nordeste_2020_Att.xlsx`: Arquivo original com os dados brutos
  - `dados_remuneracao_tratados.xlsx`: Arquivo processado com múltiplas abas para diferentes visões dos dados

- **tratamento_dados.py**: Script Python para processamento dos dados em linha de comando
- **tratamento_dados.ipynb**: Notebook Jupyter com o mesmo processamento, incluindo visualizações e análises
- **requirements.txt**: Lista de dependências necessárias para executar os scripts

## Executando o Processamento

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Execução do Script

Para executar o script de processamento em linha de comando:

```bash
python tratamento_dados.py
```

Para utilizar o notebook e visualizar as análises:

```bash
jupyter notebook tratamento_dados.ipynb
```

## Estrutura dos Dados Processados

O arquivo `dados_remuneracao_tratados.xlsx` contém as seguintes abas:

1. **Dados_Completos**: Todos os dados tratados com todas as colunas
2. **Resumo_Regiao**: Dados agregados por região do Brasil
3. **Resumo_UF**: Dados agregados por unidade federativa
4. **Resumo_Tipo_Rede**: Dados agregados por tipo de rede (pública e privada)
5. **Resumo_Escolaridade**: Dados agregados por nível de escolaridade dos docentes
6. **Diferenca_Salarial**: Análise da diferença salarial entre docentes com e sem ensino superior
7. **Metadados**: Descrição detalhada de cada coluna do dataset

## Colunas dos Dados Tratados

Os dados foram tratados e renomeados para facilitar a compreensão:

| Coluna Original | Nova Coluna                   | Descrição                                                          |
| --------------- | ----------------------------- | ------------------------------------------------------------------ |
| NU_ANO_CENSO    | ANO_CENSO                     | Ano de referência do Censo Escolar                                 |
| NO_REGIAO       | REGIAO                        | Região do Brasil                                                   |
| SG_UF           | UF                            | Unidade Federativa                                                 |
| NO_DEPENDENCIA  | DEPENDENCIA                   | Dependência administrativa (Estadual, Municipal, Federal, Privada) |
| NO_CATEGORIA    | CATEGORIA                     | Categoria dos docentes (Total, Com Superior, Sem Superior)         |
| ED_BAS_CAT_1    | NUMERO_DOCENTES               | Número total de docentes                                           |
| ED_BAS_CAT_2    | PERCENTUAL_DOC_TEMPO_INTEGRAL | Percentual de docentes em tempo integral                           |
| ED_BAS_CAT_3    | REMUNERACAO_MINIMA            | Valor mínimo da remuneração dos docentes                           |
| ED_BAS_CAT_4    | REMUNERACAO_MEDIANA           | Valor mediano da remuneração dos docentes                          |
| ED_BAS_CAT_5    | REMUNERACAO_MEDIA             | Valor médio da remuneração dos docentes                            |
| ED_BAS_CAT_6    | REMUNERACAO_75_PERCENTIL      | Valor do 75º percentil da remuneração dos docentes                 |
| ED_BAS_CAT_7    | DESVIO_PADRAO_REMUNERACAO     | Desvio padrão da remuneração dos docentes                          |
| ED_BAS_CAT_8    | COEF_VARIACAO_PERC            | Coeficiente de variação da remuneração em percentual               |
| ED_BAS_CAT_9    | REMUNERACAO_MEDIA_40H         | Remuneração média para jornada de 40 horas semanais                |

Além dessas, foram adicionadas duas novas colunas:

- **TIPO_REDE**: Indica se a dependência administrativa é pública ou privada
- **DIFERENCA_SALARIAL**: Diferença salarial entre docentes com e sem ensino superior

## Orientações para Integração com N8N

Para integrar esses dados com um agente no N8N, siga estas orientações:

1. **Escolha da planilha**: Utilize o arquivo `dados_remuneracao_tratados.xlsx` como fonte de dados para o agente
2. **Configuração de webhook**: Configure um webhook no N8N que receberá perguntas dos usuários e buscará as respostas nos dados tratados
3. **Mapeamento de perguntas comuns**:

   - "Qual a remuneração média dos professores na região X?" → Consultar aba `Resumo_Regiao`
   - "Qual estado tem a maior remuneração para professores?" → Consultar aba `Resumo_UF` e ordenar por `REMUNERACAO_MEDIA`
   - "Qual a diferença salarial entre professores com e sem ensino superior?" → Consultar aba `Diferenca_Salarial`
   - "Qual o salário médio de professores na rede privada vs. pública?" → Consultar aba `Resumo_Tipo_Rede`

4. **Exemplo de consulta SQL**:
   Se estiver utilizando um banco de dados SQL com os dados importados, pode usar consultas como:

   ```sql
   -- Consulta para remuneração média por região
   SELECT REGIAO, AVG(REMUNERACAO_MEDIA) as MEDIA_REGIONAL
   FROM dados_completos
   WHERE CATEGORIA = 'Total'
   GROUP BY REGIAO
   ORDER BY MEDIA_REGIONAL DESC;
   ```

5. **Atualização periódica**: Defina um processo para atualizar os dados quando novas versões do censo estiverem disponíveis, executando novamente os scripts de processamento

## Possíveis Perguntas para o Agente

O agente N8N deve ser capaz de responder perguntas como:

- Qual a remuneração média dos professores no Nordeste?
- Qual estado possui a maior diferença salarial entre professores com e sem ensino superior?
- Como a remuneração dos professores da rede pública se compara com a rede privada?
- Qual o percentual médio de professores em tempo integral por região?
- Qual a remuneração mediana dos professores em cada estado?
- Qual a proporção de professores com ensino superior em cada região?
- Como a variação salarial (coeficiente de variação) se compara entre diferentes estados?

## Limitações e Considerações

- Os dados são referentes ao ano de 2020, portanto não refletem mudanças posteriores
- Alguns registros podem ter sido removidos durante o tratamento por falta de informações essenciais
- As estatísticas agregadas (médias, medianas) podem ocultar disparidades importantes dentro dos grupos
