import json
import pandas as pd
import os
import streamlit as st
from google import genai
from dotenv import load_dotenv



# ========== CONFIGURAÇÃO ==========
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
MODELO = "gemini-3.5-flash"

# ========== CARREGAR DADOS ==========
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ========== MONTAR CONTEXTO ==========
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ========== SYSTEM PROMPT ==========
SYSTEM_PROMPT = """Você é o Edu, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos específicos - apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais.
  Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""

# ========== CHAMAR O AGENTE ==========
def perguntar(msg):
  prompt = f"""
  {SYSTEM_PROMPT}

  CONTEXTO DO CLIENTE:
  {contexto}

  Pergunta: {msg}"""
  response = client.models.generate_content(
        model=MODELO,
        contents=prompt
    )

  return response.text

# ========== INTERFACE ==========
st.title("🎓 Edu, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
  st.chat_message("user").write(pergunta)
  with st.spinner("..."):
    st.chat_message("assistant").write(perguntar(pergunta))