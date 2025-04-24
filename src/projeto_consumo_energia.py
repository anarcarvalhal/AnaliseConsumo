"""
Projeto: Simulador de Consumo e Energia Solar
Alunos: Ana Ruth e Douglas
Data: 24/04/2025
Descrição: Este programa coleta dados mensais de consumo de energia (kWh e R$) e fornece análises úteis para 
estimar a viabilidade de instalação de um sistema fotovoltaico.
"""
# >> IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS 
import matplotlib.pyplot as plt  # Biblioteca para gerar gráficos
import pandas as pd   # Biblioteca para manipular dados

# =======================================================================================
# CONFIGURAÇÕES DO SISTEMA SOLAR E DE TARIFAS - EDITÁVEL PELO USUÁRIO
# =======================================================================================
area_painel = 10.0       # Área de um painel
quantidade_de_paineis = 1  
area_painel_m2 = area_painel * quantidade_de_paineis   # Área total em m² do(s) painel(is) 

eficiencia_painel = 0.18   # Eficiência dos painéis (em decimal: 18% = 0.18)
perda_sistema = 0.17      # Perdas do sistema (cerca de 17%, ou seja, usa-se 83% de rendimento)

tarifa_te = 0.35921    # Tarifa de Energia (R$/kWh)
tarifa_tusd = 0.76273   # Tarifa de Distribuição (R$/kWh)

# >> CAMINHO DO ARQUIVO EXCEL COM OS DADOS DE IRRADIAÇÃO
caminho_arquivo = "Irradiacao_Itaperuna.xlsx"

# =======================================================================================
# PARÂMETROS AUXILIARES:
# =======================================================================================
# >> Variável global para o custo médio por kWh
custo_medio_kwh = 0.00
# >> Dicionário de dias por mês (para converter Wh/m²/dia para Wh/m²/mês:
dias_por_mes = {
    'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30, 'Jul': 31,
    'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31
}

# =======================================================================================
#                                FUNÇÕES DO PROGRAMA:
# =======================================================================================

def carregar_dados_irrad(caminho_arquivo):
    """
    Lê a planilha de irradiação solar da planilha Excel e retorna a média mensal de 
    irradiação solar (em Wh/m²) da região.

    Supõe-se que a tabela contenha os meses nas colunas:
    JAN, FEB, ..., DEC, e cada linha represente um ponto geográfico diferente da cidade.

    Retorna um dicionário como:
    {'Jan': média_jan, 'Feb': média_feb,... 'Dec': média_dec}
    """
    # Lê o arquivo excel usando pandas
    try:
        df = pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        print(f"ERRO! O arquivo {caminho_arquivo} não foi encontrado.")
        return {}

    # Seleciona as colunas dos meses (em letras maiúsculas conforme a planilha)
    colunas_meses = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    # Calcula a média da irradiação para cada mês, somando todos os pontos da região
    medias = df[colunas_meses].mean()

    # Converte para dicionário, com nome dos meses no formato 'Jan', 'Feb', ...
    medias_formatadas = {mes.capitalize(): float(medias[mes]) for mes in colunas_meses}
    return medias_formatadas

#    >>> FUNÇÃO AUXILIAR:
def validar_entrada_numerica(msg, tipo=float):
    """Loop que valida entradas numéricas positivas."""
    while True:   # Loop infinito até receber um valor válido
        try:
            valor = tipo(input(msg))
            if valor < 0:
                print("Erro: valor não pode ser negativo.")
                continue
            return valor
        except ValueError:    # Se a conversão falhar (ex.: o usuário digita texto)
            print("Erro: digite um número válido (use '.' para decimais).")

def calcular_valor_conta(dados_consumo, tarifa_te, tarifa_tusd):
    """
    Calcula o valor da conta de luz para cada mês com base no consumo (kWh).
    Este valor é uma estimativa baseada nas tarifas TE e TUSD. Impostos como ICMS, PIS e COFINS 
    não estão inclusos, mas podem representar até 30% a mais no valor final da conta. 
    
    Atualiza o valor da conta ('R$') no dicionário de dados_consumo.
    """
    for mes in dados_consumo:  # Para cada mês no dicionário de consumo  
        consumo_kwh = dados_consumo[mes]['kWh']   # Pega o consumo em kWh

        # Calcula o valor da conta: kWh * (Tarifa TE + Tarifa TUSD) 
        valor_calculado = consumo_kwh * (tarifa_te + tarifa_tusd) 

        dados_consumo[mes]['R$'] = valor_calculado    

def coletar_dados_energia():
    """Coleta dados de consumo de energia de cada mês:
    --> Quantidade de energia consumida (kWh)
    --> Valor pago na conta de luz (R$)

    Retona um dicionário no formato:
    {'Mês': {'kWh': valor_consumo, 'R$': valor_pago}}
    """
    # Lista com os meses do ano
    meses = [
      'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho','Julho',
      'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    # Dicionário principal que armazenará os dados de consumo
    dados_consumo = {}
    
    # Interface de entrada para o usuário
    print("\n" + "=" * 50)  # Linha separadora para estética
    print("        ENTRADA DE DADOS DE CONSUMO DE ENERGIA")
    print("\n" + "=" * 50) # Linha separadora para estética
    print("Digite o consumo (kWh) e o valor da conta (R$) para cada mês: \n")

    for mes in meses:
        print(f"      MÊS: {mes.capitalize()}")
    
        consumo = validar_entrada_numerica(f"Consumo de energia (kWh) em {mes}: ")
        print("\n" + "-" * 50)

        # Armazenando dados no dicionário principal
        dados_consumo[mes] = {'kWh': consumo}
    
    return dados_consumo

def analisar_dados(dados_consumo):
    """Analisa os dados de consumo de energia:
    --> Identifica o mês de maior e de menor consumo
    --> Calcula o consumo médio e valor médio da conta
    --> Exibe os resultados ao usuário
    """
    # Permite atualizar a variável global
    global custo_medio_kwh
    # Identifica o mês com o maior e menor consumo
    maior_mes = max(dados_consumo, key=lambda mes: dados_consumo[mes]['kWh'])
    menor_mes = min (dados_consumo, key=lambda mes: dados_consumo[mes]['kWh'])

    # Calcula totais e médias
    consumo_total = sum(dados_consumo[mes]['kWh'] for mes in dados_consumo)
    valor_total = sum(dados_consumo[mes]['R$'] for mes in dados_consumo)
    media_consumo = consumo_total / 12
    media_valor = valor_total / 12

    # Calcula o custo médio por kWh em cada mês
    custo_por_kwh = {
        mes: dados_consumo[mes]['R$'] / dados_consumo[mes]['kWh']
        for mes in dados_consumo
    }

    # Calcula o custo médio de kWh e armazena no escopo global
    custo_medio_kwh = sum(custo_por_kwh.values()) / len(custo_por_kwh)

    # Exibindo os resultados da análise
    print("\n" + "=" * 50)
    print("                ANÁLISE DOS DADOS")
    print("=" * 50)
    print(f"Mês de MAIOR consumo: {maior_mes} ({dados_consumo[maior_mes]['kWh']} kWh)")
    print(f"Mês de MENOR consumo: {menor_mes} ({dados_consumo[menor_mes]['kWh']} kWh)")
    print(f"Consumo médio: {media_consumo:.2f} kWh")
    print(f"Valor MÉDIO da conta: R$ {media_valor:.2f}")
    print(f"> CUSTO MÉDIO por kWh: R$ {custo_medio_kwh:.2f}")

def gerar_grafico(dados_consumo):
    """
    Gera um gráfico de barras com o consumo de energia de cada mês.
    """
    # Cria uma lista com os nomes dos meses a partir das chaves do dicionário
    meses = list(dados_consumo.keys())

    # Cria uma lista com os valores de consumo correspondentes a cada mês
    consumo = [dados_consumo[mes]['kWh'] for mes in meses]

    # Cria o gráfico
    plt.figure(figsize=(12,6))  # Define o tamanho da figura (largura=12, altura=6)
    plt.bar(meses, consumo, color='skyblue')   # Cria o gráfico de barras: eixo x = meses, eixo y = consumo 
    plt.title("Consumo de Energia Mensal (kWh)")  # Título do gráfico
    plt.xlabel("Mês")  # Nome do eixo x
    plt.ylabel("Consumo (kWh)") # Nome do eixo y
    plt.xticks(rotation=45) # Gira os nomes para facilitar a leitura
    plt.grid(axis='y', linestyle='--', alpha=0.5)  # Adiciona uma grade horizontal
    plt.tight_layout()  # Ajusta o layout para não cortar textos
    plt.show()  # Exibe o gráfico em tela
    plt.savefig("grafico_consumo.png", dpi=300)  # Salva a imagem

def simular_geracao_solar(irrad_mes, area_painel_m2, eficiencia_painel, perda_sistema):
    """Calcula a geração mensal estimada de energia solar e compara com o consumo. 
    Exibe a economia estimada e se o sistema cobre a demanda de cada mês.
    
    Parâmetros: 
    - irrad_mes: dicionário com a irradiação solar média por mês (kWh/m²)
    - area_painel_m2: área total dos painéis solares (m²) 
    - eficiencia_painel: eficiência dos painéis
    - perda_sistema: perdas do sistema

    Retorna um dicionário com a energia gerada em kWh por mês.
    """
    rendimento_real = (1 - perda_sistema)  # Calcula o rendimento real, considerando perdas.
    geracao_solar = {}    # Dicionário para guardar a energia gerada em cada mês

    # Mapeia abreviação para nome completo.
    mapa_meses = {
        'Jan': 'Janeiro', 'Feb': 'Fevereiro', 'Mar': 'Março', 'Apr': 'Abril', 'May': 'Maio',
        'Jun': 'Junho', 'Jul': 'Julho', 'Aug': 'Agosto', 'Sep': 'Setembro', 'Oct': 'Outubro',
        'Nov': 'Novembro','Dec': 'Dezembro'
    }

    # Laço for para cada mês na tabela de irradiação:
    for mes_abrev, irrad_diaria in irrad_mes.items():
        # Número de dias no mês
        dias = dias_por_mes.get(mes_abrev, 30) 

        # Irradiação mensal total em Wh/m²
        irrad_mensal_wh = irrad_diaria * dias

        # Energia em Wh/m²: irradiação mensal x área x eficiência x rendimento
        energia_wh = irrad_mensal_wh * area_painel_m2 * eficiencia_painel * rendimento_real

        # Cálculo da energia gerada, passando pra kWh:
        gerado_kwh = energia_wh / 1000

        # Armazena no dicionário com nome completo do mês
        mes_completo = mapa_meses.get(mes_abrev, mes_abrev)
        geracao_solar[mes_completo] = gerado_kwh

    return geracao_solar

def comparar_geracao_consumo(geracao_solar, dados_consumo):
    """Compara geração solar x consumo real de forma resumida:
    - Indica qual mês de maior e qual mês de menor geração solar
    - Calcula a economia anual estimada 
    - Mostra quantos meses o sistema cobre o consumo
    - Conclui se o sistema é vantajoso"""

    mes_mais_gerou = max(geracao_solar, key=geracao_solar.get)
    valor_mais_gerou = geracao_solar[mes_mais_gerou]
    mes_menos_gerou = min(geracao_solar, key=geracao_solar.get)
    valor_menos_gerou = geracao_solar[mes_menos_gerou]

    # Cálculo da economia total e contagem de meses
    economia_total = 0
    meses_insuficientes = 0
    meses_suficientes = 0

    for mes in dados_consumo:
        consumo_kwh = dados_consumo[mes]['kWh']
        gerado_kwh = geracao_solar.get(mes, 0)
        energia_utilizada = min(consumo_kwh, gerado_kwh)

        # Economia calculada pelo custo médio por kWh
        economia_mes = custo_medio_kwh * energia_utilizada
        economia_total += economia_mes
        
        if gerado_kwh >= consumo_kwh:
            meses_suficientes += 1
        else:
            meses_insuficientes += 1
        
    print("\n" + "=" * 60)
    print("            SIMULAÇÃO SOLAR:")
    print("=" * 60)
    print(f"Mês de maior geração solar: {mes_mais_gerou} --> {valor_mais_gerou:.1f} kWh:")
    print(f"Mês de menor geração solar: {mes_menos_gerou} --> {valor_menos_gerou:.1f} kWh")
    print(f"     Economia anual estimada: R$ {economia_total:.2f}")
    print(f" Meses cobertos:  {meses_suficientes}")
    print(f" Meses não cobertos:  {meses_insuficientes}")
    print("-" * 60)

    if meses_suficientes > meses_insuficientes:
        print("\n>> CONCLUSÃO: ✅ Energia Solar, nessas condições, será vantajosa para você!")
    elif meses_suficientes == meses_insuficientes:
        print("\n>> CONCLUSÃO: ⚠️ A Energia Solar pode ser vantajosa, mas varia bastante entre os meses. Avalie com cuidado.")
    else:
        print("\n>> CONCLUSÃO: ❌ Sistema atual não é vantajoso - Considere ajustes.")

# =======================================================================================
# FUNÇÃO PRINCIPAL: INÍCIO DO PROGRAMA
# =======================================================================================
def main():
    # Carrega os dados de irradiação solar
    dados_irrad = carregar_dados_irrad(caminho_arquivo)

    dados_consumo = coletar_dados_energia()
    calcular_valor_conta(dados_consumo, tarifa_te, tarifa_tusd)  # Isso vai adicionar os valores R$

    analisar_dados(dados_consumo)
   
    # Simula geração solar
    geracao_solar = simular_geracao_solar(
        dados_irrad, 
        area_painel_m2, 
        eficiencia_painel, 
        perda_sistema
    )
  
    comparar_geracao_consumo(geracao_solar, dados_consumo)

    gerar_grafico(dados_consumo)
   
# Executa o programa
if __name__ == "__main__":
    main()
