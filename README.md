# AnaliseConsumo
Ferramenta Python para análise de viabilidade energética, cruzando dados de irradiação solar e consumo elétrico. Gera projeções de economia para sistemas fotovoltaicos residenciais/comerciais.

PROJETO: CONSUMO e ENERGIA SOLAR
Data de criação: 24/02/2025

Os dados de irradiação solar são extraídos da planilha 'global_horizontal_means_RJ.csv' da LABREN, na qual filtrei 21 IDs correspondentes ao município de Itaperuna, localizado no Noroeste Fluminense. 
Calculamos a média diária mensal sobre esses 21 pontos para obter um valor representativo da região.

# Funcionalidades Principais:
- Leitura de Irradiação Solar
  Carrega média mensal de irradiação (Wh/m²) a partir de uma planilha do excel.

- Coleta de Dados de Consumo
  Interface interativa para entrada de consumo (kWh) e valor da conta (R$) para cada mês.

- Cálculo do Valor da Conta
  Estima o valor da fatura mensal média com base nas tarifas TE e TUSD.

- Análise de Consumo
  Identifica meses de maior e de menor consumo, calculaa consumo médio e valor médio de conta.

- Simulação de Geração Solar
  Calcula geração mensal de energia solar realista considerando a área de painéis, eficiência e perdas do sistema.
  Compara geração com consumo, conta meses cobertos e estima economia anual.

- Visualização Gráfica
  Gera e salva gráfico de barras do consumo mensal (kWh)

# Pré-requisitos
Python 3.7+
Bibliotecas Python: pandas, matplotlib
