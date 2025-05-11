# Análise de Remuneração de Docentes por Regiões do Brasil

Este repositório contém uma análise detalhada da remuneração de docentes no Brasil, organizada por região, rede de ensino e formação, com base em dados do ano de 2020.

## Análise `analise_regioes.ipynb`

Este notebook realiza uma análise exploratória detalhada sobre remuneração docente no Brasil, identificando disparidades regionais importantes. O estudo começa com a leitura e preparação dos dados, seguido por análises comparativas entre regiões, redes de ensino (pública x privada) e níveis de formação dos docentes.

As visualizações incluem gráficos comparativos de remuneração média por região, análises do impacto da rede de ensino nas diferentes regiões do país, e a influência do nível de formação dos docentes na remuneração. O notebook também examina o coeficiente de variação (CV) como medida de dispersão salarial.

O estudo culmina com a exportação dos dados tratados para arquivos Excel, facilitando análises posteriores e compartilhamento dos resultados. Os principais insights obtidos apontam para significativas disparidades regionais na remuneração docente, com as regiões Sudeste e Sul apresentando maiores valores médios, além de evidenciar o impacto positivo da formação superior na remuneração em todas as regiões do país.

1. **Carregamento e Tratamento dos Dados**:

   - Leitura do arquivo Excel com dados de remuneração
   - Tratamento e renomeação das colunas
   - Verificação da integridade dos dados

2. **Análise por Região**:

   - Comparação da remuneração média de docentes entre as regiões do Brasil
   - Visualização da distribuição salarial por região em gráficos de barras
   - Análise estatística descritiva dos dados regionais

3. **Análise por Rede de Ensino**:

   - Comparação entre redes públicas (estadual e municipal) e privadas
   - Visualização de remuneração por tipo de rede
   - Análise das diferenças salariais entre redes

4. **Análise por Formação**:

   - Comparação entre docentes com e sem ensino superior
   - Impacto da formação na remuneração por região e rede de ensino

5. **Visualizações**:

   - Gráficos de barras para comparações diretas
   - Heatmaps para análise de correlações entre variáveis
   - Boxplots para visualização da distribuição e outliers

6. **Exportação de Dados Tratados**:
   - Criação de arquivos Excel com dados consolidados
   - Dados agrupados por região, rede de ensino e formação
   - Comparativos entre UFs organizados por região

## Principais Conclusões

- Existem diferenças significativas na remuneração de docentes entre as regiões do Brasil
- A região Sudeste e Sul apresentam as maiores médias salariais para docentes
- Docentes com ensino superior recebem remuneração consideravelmente maior
- A rede privada apresenta padrões salariais distintos das redes públicas
- O coeficiente de variação indica diferentes níveis de dispersão salarial entre as regiões

## Utilização

Para explorar esta análise:

1. Clone o repositório
2. Certifique-se de ter o Jupyter Notebook e as dependências instaladas:
   ```
   pip install pandas numpy matplotlib seaborn
   ```
3. Abra o notebook `analise_regioes.ipynb` e execute as células

## Exportação dos Dados

A análise permite exportar os resultados em formato Excel para uso posterior, com diferentes abas:

- Dados por região
- Dados por região e rede de ensino
- Dados por região e formação
- Dados por UF

Estes dados processados podem ser utilizados para alimentar dashboards, relatórios ou outras análises específicas.

## Requisitos

- Python 3.6+
- pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
