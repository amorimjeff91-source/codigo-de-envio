import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ==========================================
# CONFIGURAÇÃO E CONEXÃO COM O BANCO DE DADOS
# ==========================================
# Cria o arquivo do banco de dados (se não existir) e conecta
conn = sqlite3.connect("gestao_industrial.db", check_same_thread=False)
cursor = conn.cursor()

# Cria a tabela de peças (se ela não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE,
    horas_trabalhadas REAL,
    desgaste_percentual REAL
)
""")
conn.commit()


# ==========================================
# INTERFACE DO STREAMLIT (SEU MENU LATERAL)
# ==========================================
st.title("🤖 Robô de Gestão Industrial")
st.write("Suporte para: Fábricas de Cimento, Cerâmicas, Engenharia, Supermercados e Serviços.")

# Criando as abas/páginas com base no seu menu
aba_cadastro, aba_painel = st.tabs(["📝 Cadastrar Peça", "📊 Painel de Controle e Desgaste"])


# ==========================================
# 1) OPÇÃO: CADASTRO E VALIDAÇÃO DE PEÇAS
# ==========================================
with aba_cadastro:
    st.subheader("Cadastrar Nova Peça em Operação")
    
    # Campos de entrada para o usuário
    codigo_peca = st.text_input("Código Único da Peça", placeholder="Ex: CIM-101")
    
    # Simulando dados iniciais para a peça nova rodar no gráfico depois
    horas_iniciais = st.number_input("Horas Iniciais de Trabalho", min_value=0.0, value=0.0)
    desgaste_inicial = st.slider("Porcentagem Inicial de Desgaste (%)", min_value=0, max_value=100, value=0)
    
    botao_cadastrar = st.button("Cadastrar Peça")
    
    if botao_cadastrar:
        # Limpa espaços em branco e deixa tudo em letras maiúsculas
        codigo_limpo = codigo_peca.strip().upper()
        
        # Validações de segurança
        if not codigo_limpo:
            st.error("❌ Erro: O campo de código não pode ficar vazio!")
        elif codigo_limpo == "EX: CIM-101":
            st.error("❌ Erro: Digite um código válido, não use o exemplo!")
        else:
            try:
                # Salva os dados de forma limpa no Banco de Dados SQL
                cursor.execute(
                    "INSERT INTO pecas (codigo, horas_trabalhadas, desgaste_percentual) VALUES (?, ?, ?)",
                    (codigo_limpo, horas_iniciais, desgaste_inicial)
                )
                conn.commit()
                st.success(f"✅ Peça '{codigo_limpo}' cadastrada e salva no banco de dados!")
            except sqlite3.IntegrityError:
                # O SQLite avisa se alguém tentar cadastrar o mesmo código duas vezes
                st.error("❌ Erro: Este código de peça já está cadastrado no sistema!")


# ==========================================
# 2) OPÇÃO: PAINEL DE CONTROLE E GRÁFICOS
# ==========================================
with aba_painel:
    st.subheader("Painel de Visualização de Desgaste")
    
    # Busca os dados salvos no banco de dados usando o Pandas
    df = pd.read_sql_query("SELECT * FROM pecas", conn)
    
    if df.empty:
        st.warning("⚠️ Nenhuma peça cadastrada no momento. Vá até a aba de cadastro!")
    else:
        # Mostra a tabela organizada com os dados guardados
        st.write("### Peças Ativas no Sistema")
        st.dataframe(df[["codigo", "horas_trabalhadas", "desgaste_percentual"]], use_container_width=True)
        
        # Cria um gráfico interativo e moderno usando Plotly
        st.write("### Gráfico de Análise de Risco (Desgaste vs Horas)")
        fig = px.bar(
            df, 
            x="codigo", 
            y="desgaste_percentual", 
            color="horas_trabalhadas",
            title="Porcentagem de Desgaste por Peça Industrial",
            labels={"codigo": "Código da Peça", "desgaste_percentual": "Desgaste (%)", "horas_trabalhadas": "Horas de Uso"},
            color_continuous_scale="Reds" # Fica vermelho se tiver muitas horas
        )
        st.plotly_chart(fig, use_container_width=True)
