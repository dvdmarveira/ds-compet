import pandas as pd
import os
import numpy as np

def carregar_dados():
    print("Carregando dados da planilha...")
    # Carregando o arquivo Excel
    caminho_arquivo = os.path.join('datasets', 'Remuneracao_docentes_Nordeste_2020_Att.xlsx')
    
    # Como a primeira linha já contém os valores, precisamos definir os nomes das colunas manualmente
    nomes_colunas = [
        'Indice', 'ANO_CENSO', 'REGIAO', 'UF', 'DEPENDENCIA', 'CATEGORIA', 
        'NUMERO_DOCENTES', 'PERCENTUAL_DOC_TEMPO_INTEGRAL', 'REMUNERACAO_MINIMA', 
        'REMUNERACAO_MEDIANA', 'REMUNERACAO_MEDIA', 'REMUNERACAO_75_PERCENTIL', 
        'DESVIO_PADRAO_REMUNERACAO', 'COEF_VARIACAO_PERC', 'REMUNERACAO_MEDIA_40H'
    ]
    
    # Lendo o arquivo com os nomes de colunas corretos
    df = pd.read_excel(caminho_arquivo, skiprows=8, header=None, names=nomes_colunas)
    
    print(f"Dados carregados com sucesso! Total de registros: {len(df)}")
    return df

def tratar_dados(df):
    print("Tratando os dados...")
    
    # 1. Removendo linhas com NaN em várias colunas (linhas de notas e fontes)
    df = df.dropna(subset=['REGIAO', 'UF', 'DEPENDENCIA', 'CATEGORIA'], how='any')
    
    # 2. As colunas já estão com nomes compreensíveis, pois definimos no carregamento
    
    # 3. Convertendo colunas numéricas para o formato correto
    colunas_numericas = ['NUMERO_DOCENTES', 'PERCENTUAL_DOC_TEMPO_INTEGRAL', 'REMUNERACAO_MINIMA', 
                         'REMUNERACAO_MEDIANA', 'REMUNERACAO_MEDIA', 'REMUNERACAO_75_PERCENTIL',
                         'DESVIO_PADRAO_REMUNERACAO', 'COEF_VARIACAO_PERC', 'REMUNERACAO_MEDIA_40H']
    
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    
    # 4. Arredondando valores para 2 casas decimais
    for coluna in colunas_numericas[1:]:  # Todas exceto NUMERO_DOCENTES que deve ser inteiro
        df[coluna] = df[coluna].round(2)
    
    # 5. Convertendo NUMERO_DOCENTES para inteiro
    df['NUMERO_DOCENTES'] = df['NUMERO_DOCENTES'].fillna(0).astype(int)
    
    # 6. Ordenando o DataFrame por região e UF
    df = df.sort_values(by=['REGIAO', 'UF', 'DEPENDENCIA', 'CATEGORIA'])
    
    # 7. Adicionando informações adicionais úteis
    # Criando uma coluna para indicar se é rede pública ou privada
    df['TIPO_REDE'] = df['DEPENDENCIA'].apply(lambda x: 'Privada' if x == 'Privada' else 'Pública')
    
    # 8. Calculando a diferença salarial entre docentes com e sem ensino superior
    # Criando um pivot temporário
    pivot_temp = df.pivot_table(
        index=['REGIAO', 'UF', 'DEPENDENCIA'],
        columns='CATEGORIA',
        values='REMUNERACAO_MEDIA'
    ).reset_index()
    
    # Se existirem as categorias esperadas, calcular a diferença
    if 'Com Superior' in pivot_temp.columns and 'Sem Superior' in pivot_temp.columns:
        pivot_temp['DIFERENCA_SALARIAL'] = pivot_temp['Com Superior'] - pivot_temp['Sem Superior']
        
        # Mesclando de volta ao DataFrame original
        df = df.merge(
            pivot_temp[['REGIAO', 'UF', 'DEPENDENCIA', 'DIFERENCA_SALARIAL']],
            on=['REGIAO', 'UF', 'DEPENDENCIA'],
            how='left'
        )
        
        # Arredondando o valor da diferença salarial
        df['DIFERENCA_SALARIAL'] = df['DIFERENCA_SALARIAL'].round(2)
    
    print("Tratamento de dados concluído com sucesso!")
    return df

def salvar_dados_tratados(df, nome_arquivo='dados_remuneracao_tratados_v2.xlsx'):
    print(f"Salvando dados tratados em {nome_arquivo}...")
    
    # Criando um novo arquivo Excel com os dados tratados
    caminho_saida = os.path.join('datasets', nome_arquivo)
    
    # Criando um objeto ExcelWriter
    with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
        # Salvando o DataFrame completo
        df.to_excel(writer, sheet_name='Dados_Completos', index=False)
        
        # Criando abas adicionais com visões específicas
        # Visão por Região
        pivot_regiao = df.pivot_table(
            index='REGIAO',
            values=['REMUNERACAO_MEDIA', 'REMUNERACAO_MINIMA', 'REMUNERACAO_MEDIANA', 'NUMERO_DOCENTES'],
            aggfunc={'REMUNERACAO_MEDIA': 'mean', 'REMUNERACAO_MINIMA': 'min', 
                    'REMUNERACAO_MEDIANA': 'median', 'NUMERO_DOCENTES': 'sum'}
        ).reset_index()
        pivot_regiao.to_excel(writer, sheet_name='Resumo_Regiao', index=False)
        
        # Visão por UF
        pivot_uf = df.pivot_table(
            index=['REGIAO', 'UF'],
            values=['REMUNERACAO_MEDIA', 'REMUNERACAO_MINIMA', 'REMUNERACAO_MEDIANA', 'NUMERO_DOCENTES'],
            aggfunc={'REMUNERACAO_MEDIA': 'mean', 'REMUNERACAO_MINIMA': 'min', 
                    'REMUNERACAO_MEDIANA': 'median', 'NUMERO_DOCENTES': 'sum'}
        ).reset_index()
        pivot_uf.to_excel(writer, sheet_name='Resumo_UF', index=False)
        
        # Visão por Tipo de Rede (Pública x Privada)
        pivot_rede = df.pivot_table(
            index=['TIPO_REDE', 'DEPENDENCIA'],
            values=['REMUNERACAO_MEDIA', 'REMUNERACAO_MINIMA', 'REMUNERACAO_MEDIANA', 'NUMERO_DOCENTES'],
            aggfunc={'REMUNERACAO_MEDIA': 'mean', 'REMUNERACAO_MINIMA': 'min', 
                    'REMUNERACAO_MEDIANA': 'median', 'NUMERO_DOCENTES': 'sum'}
        ).reset_index()
        pivot_rede.to_excel(writer, sheet_name='Resumo_Tipo_Rede', index=False)
        
        # Visão por Escolaridade (Com Superior x Sem Superior)
        pivot_escolaridade = df[df['CATEGORIA'] != 'Total'].pivot_table(
            index='CATEGORIA',
            values=['REMUNERACAO_MEDIA', 'REMUNERACAO_MINIMA', 'REMUNERACAO_MEDIANA', 'NUMERO_DOCENTES'],
            aggfunc={'REMUNERACAO_MEDIA': 'mean', 'REMUNERACAO_MINIMA': 'min', 
                    'REMUNERACAO_MEDIANA': 'median', 'NUMERO_DOCENTES': 'sum'}
        ).reset_index()
        pivot_escolaridade.to_excel(writer, sheet_name='Resumo_Escolaridade', index=False)
        
        # Adicionando uma aba específica para análise de diferença salarial
        if 'DIFERENCA_SALARIAL' in df.columns:
            pivot_dif_salarial = df[df['CATEGORIA'] == 'Total'].pivot_table(
                index=['REGIAO', 'UF', 'DEPENDENCIA'],
                values=['DIFERENCA_SALARIAL'],
                aggfunc={'DIFERENCA_SALARIAL': 'mean'}
            ).reset_index()
            pivot_dif_salarial = pivot_dif_salarial.sort_values('DIFERENCA_SALARIAL', ascending=False)
            pivot_dif_salarial.to_excel(writer, sheet_name='Diferenca_Salarial', index=False)
    
    print(f"Dados salvos com sucesso em {caminho_saida}!")
    return caminho_saida

def criar_dicionario_metadados(df):
    """Cria um dicionário com informações dos metadados das colunas para facilitar a compreensão dos dados"""
    metadados = {
        'ANO_CENSO': 'Ano de referência do Censo Escolar',
        'REGIAO': 'Região do Brasil',
        'UF': 'Unidade Federativa',
        'DEPENDENCIA': 'Dependência administrativa (Estadual, Municipal, Federal, Privada)',
        'CATEGORIA': 'Categoria dos docentes (Total, Com Superior, Sem Superior)',
        'NUMERO_DOCENTES': 'Número total de docentes',
        'PERCENTUAL_DOC_TEMPO_INTEGRAL': 'Percentual de docentes em tempo integral',
        'REMUNERACAO_MINIMA': 'Valor mínimo da remuneração dos docentes',
        'REMUNERACAO_MEDIANA': 'Valor mediano da remuneração dos docentes',
        'REMUNERACAO_MEDIA': 'Valor médio da remuneração dos docentes',
        'REMUNERACAO_75_PERCENTIL': 'Valor do 75º percentil da remuneração dos docentes',
        'DESVIO_PADRAO_REMUNERACAO': 'Desvio padrão da remuneração dos docentes',
        'COEF_VARIACAO_PERC': 'Coeficiente de variação da remuneração em percentual',
        'REMUNERACAO_MEDIA_40H': 'Remuneração média para jornada de 40 horas semanais',
        'TIPO_REDE': 'Tipo de rede de ensino (Pública ou Privada)',
        'DIFERENCA_SALARIAL': 'Diferença salarial entre docentes com e sem ensino superior'
    }
    
    # Salvando metadados como um DataFrame
    metadados_df = pd.DataFrame(list(metadados.items()), columns=['Coluna', 'Descrição'])
    return metadados_df

def main():
    # Carregando os dados
    df_original = carregar_dados()
    
    # Tratando os dados
    df_tratado = tratar_dados(df_original)
    
    # Criando metadados
    metadados = criar_dicionario_metadados(df_tratado)
    
    # Salvando os dados tratados
    caminho_saida = salvar_dados_tratados(df_tratado)
    
    # Salvando os metadados
    with pd.ExcelWriter(caminho_saida, engine='openpyxl', mode='a') as writer:
        metadados.to_excel(writer, sheet_name='Metadados', index=False)
    
    print(f"""
    ========================================================
    Processamento concluído com sucesso!
    
    Total de registros tratados: {len(df_tratado)}
    Arquivo salvo em: {caminho_saida}
    
    O arquivo contém as seguintes abas:
    - Dados_Completos: Todos os dados tratados
    - Resumo_Regiao: Dados agregados por região
    - Resumo_UF: Dados agregados por UF
    - Resumo_Tipo_Rede: Dados agregados por tipo de rede
    - Resumo_Escolaridade: Dados agregados por escolaridade
    - Diferenca_Salarial: Análise da diferença salarial entre docentes com e sem ensino superior
    - Metadados: Descrição das colunas
    ========================================================
    """)

if __name__ == "__main__":
    main() 