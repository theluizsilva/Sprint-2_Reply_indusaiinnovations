import pandas as pd
import matplotlib.pyplot as plt
import os
import io

# Define o caminho para o arquivo CSV de dados.
# Certifique-se que este caminho está correto em relação onde você vai rodar o script.
csv_file_path = '../data/processed/dados_temperatura_simulacao.csv'

# Verifica se o arquivo CSV existe e o carrega.
# Se não for encontrado, um erro será impresso e o script pode falhar.
# Certifique-se que o arquivo CSV da Parte 1 está na pasta correta.
if not os.path.exists(csv_file_path):
    print(f"ERRO: Arquivo CSV não encontrado em {csv_file_path}")
    print("Por favor, verifique se você salvou 'dados_temperatura_simulacao.csv' corretamente na pasta 'data/processed/'.")
    # Para que você possa testar o script mesmo sem o CSV no lugar, podemos adicionar um fallback,
    # mas para a entrega, o arquivo REAL deve estar lá.
    print("\n--- ATENÇÃO: Usando dados de exemplo para demonstração. O arquivo real deve ser gerado no Passo 4. ---")
    dados_simulados_str_fallback = """
    Valor ADC,Resistencia Calculada,Temperatura Calculada
    2047,10000.00,25.00
    1950,11025.64,22.45
    2200,8846.15,28.12
    2500,7000.00,32.50
    1800,12500.00,19.80
    1700,13500.00,17.50
    2600,6500.00,34.00
    2700,6000.00,35.50
    2100,9500.00,26.50
    2000,10500.00,23.80
    1600,14500.00,15.00
    2800,5500.00,37.00
    2900,5000.00,38.50
    2300,8000.00,30.00
    2400,7500.00,31.20
    """
    df = pd.read_csv(io.StringIO(dados_simulados_str_fallback))
    print("Continuando com dados de fallback. Por favor, corrija o caminho do CSV para a entrega final.")
else:
    df = pd.read_csv(csv_file_path)
    print(f"Dados lidos com sucesso de: {csv_file_path}")

# Adicionar uma coluna de tempo/índice para o gráfico de linha
df['Tempo (s)'] = df.index # O índice do DataFrame serve como tempo, pois as leituras são sequenciais

# --- Gerar Gráficos ---

# Cria a pasta 'plots' dentro de 'data_analysis' se ela não existir
output_plot_dir = 'plots'
if not os.path.exists(output_plot_dir):
    os.makedirs(output_plot_dir)
    print(f"Pasta '{output_plot_dir}' criada para salvar os gráficos.")

# Gráfico de linha da temperatura ao longo do tempo
plt.figure(figsize=(12, 6))
plt.plot(df['Tempo (s)'], df['Temperatura Calculada'], marker='o', linestyle='-', markersize=4)
plt.title('Simulação de Leitura de Temperatura ao Longo do Tempo', fontsize=16)
plt.xlabel('Tempo (segundos)', fontsize=12)
plt.ylabel('Temperatura (°C)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout() # Ajusta o layout para não cortar elementos
plt.savefig(os.path.join(output_plot_dir, 'temperatura_linha.png')) # Salva o gráfico na pasta 'plots'
plt.show() # Exibe o gráfico na tela

# Histograma da distribuição das temperaturas
plt.figure(figsize=(10, 6))
plt.hist(df['Temperatura Calculada'], bins=7, edgecolor='black', alpha=0.8) # Ajuste bins conforme seus dados
plt.title('Distribuição das Temperaturas Calculadas Simuladas', fontsize=16)
plt.xlabel('Temperatura (°C)', fontsize=12)
plt.ylabel('Frequência', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_plot_dir, 'temperatura_histograma.png')) # Salva o gráfico na pasta 'plots'
plt.show() # Exibe o gráfico na tela

# --- Estatísticas Simples ---
print("\n--- Estatísticas Descritivas da Temperatura Calculada ---")
desc_stats = df['Temperatura Calculada'].describe()
print(desc_stats)

print("\n--- Cinco Primeiras Leituras ---")
print(df.head())

print("\n--- Cinco Últimas Leituras ---")
print(df.tail())

# --- Insights Iniciais ---
print("\n--- Insights Iniciais dos Dados Simulados ---")
min_temp = df['Temperatura Calculada'].min()
max_temp = df['Temperatura Calculada'].max()
mean_temp = df['Temperatura Calculada'].mean()
print(f"A temperatura simulada variou de {min_temp:.2f}°C a {max_temp:.2f}°C.")
print(f"A média das temperaturas registradas foi de {mean_temp:.2f}°C.")
print("O gráfico de linha mostra a flutuação da temperatura ao longo do tempo, simulando variações em um ambiente industrial.")
print("Os picos de temperatura observados, como em leituras acima de 30°C, poderiam indicar em um cenário real")
print("um possível superaquecimento de equipamentos, o que é um foco para a detecção preditiva de falhas da IndusAI Innovations.")
print("A distribuição (histograma) indica as faixas de temperatura mais frequentes durante a simulação.")