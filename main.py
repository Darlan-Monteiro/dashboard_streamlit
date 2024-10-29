import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

@st.cache_data
def carregar_dados(empresas):
  texto_tickers = " ".join(empresas)
  dados_acao = yf.Tickers(texto_tickers)
  cotacoes_acao = dados_acao.history(period='1d', start='2010-01-01', end='2024-07-01')
  print(cotacoes_acao)
  cotacoes_acao = cotacoes_acao['Close']
  return cotacoes_acao

def carregar_tickets():
  base_tickers = pd.read_csv("c:/Users/SAMSUNG/OneDrive/Área de Trabalho/Documentos/Portfólio PYTHON/apps_e_sites_streamlit/ibov.csv", sep=";")
  tickers = list(base_tickers['Código'])
  tickers = [item + '.SA' for item in tickers]
  return tickers

acoes = carregar_tickets()
dados = carregar_dados(acoes)


st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
         """)

st.sidebar.header("Filtros")

lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar:", dados.columns)
if lista_acoes:
    dados=dados[lista_acoes]
    if len(lista_acoes) == 1:
      acao_unica = lista_acoes[0]
      dados = dados.rename(columns={acao_unica:"Close"})
      
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_datas = st.sidebar.slider('Selecione o período', min_value=data_inicial, max_value=data_final, value=(data_inicial,data_final), step=timedelta(days=1))

dados = dados.loc[intervalo_datas[0]:intervalo_datas[1]]

st.line_chart(dados)

texto_performance_ativos = ''

if len(lista_acoes)==0:
  lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
  dados = dados.rename(columns={'Close':acao_unica})
  
carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

for i,acao in enumerate(lista_acoes):
  performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0]  - 1
  performance_ativo = float(performance_ativo)
  
  carteira[i] = carteira[i]*(1 + performance_ativo)
  
  if performance_ativo > 0:
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{performance_ativo:.1%}]"
  elif performance_ativo < 0:
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
  else:
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"
    
tot_final_carteira = sum(carteira)
performance_carteira = tot_final_carteira / total_inicial_carteira
    
if performance_ativo > 0:
  texto_performance_carteira = f"Performance da carteira com todos os ativos: :green[{performance_ativo:.1%}]"
elif performance_ativo < 0:
  texto_performance_carteira = f"Performance da carteira com todos os ativos: :red[{performance_ativo:.1%}]"
else:
  texto_performance_carteira = f"Performance da carteira com todos os ativos:{performance_ativo:.1%}"

st.write(f"""
### Performace dos Ativos
Essa foi a perfomace de cada ativo no período selecionado:
{texto_performance_ativos}

{texto_performance_carteira}
         """)