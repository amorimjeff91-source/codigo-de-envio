import sqlite3
import datetime
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DO BANCO DE DADOS REAL
# ==========================================
def conectar_e_criar_tabela():
    conexao = sqlite3.connect("robo_industrial.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pecas_industriais (
            codigo TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            vida_util_maxima REAL NOT NULL,
            horas_trabalhadas REAL DEFAULT 0.0,
            data_inicio TEXT NOT NULL,
            porcentagem_desgaste REAL DEFAULT 0.0,
            status TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

conectar_e_criar_tabela()

# ==========================================
# 2. INTERFACE VISUAL DO SITE (STREAMLIT)
# ==========================================
st.set_page_config(page_title="Robô de Gestão Industrial", page_icon="🤖", layout="wide")

st.title("🤖 Robô de Gestão Industrial")
st.subheader("Controle de Horas Trabalhadas e Desgaste de Peças")
st.write("Suporte para: Fábricas de Cimento, Cerâmicas, Engenharia, Supermercados e Serviços.")

# Criando abas no site para organizar as funções
aba_nova, aba_atualizar, aba_relatorio = st.tabs([
    "🆕 Início de Atuação (Peça Nova)", 
    "⏱️ Registrar Horas / Turno", 
    "📊 Painel de Controle e Desgaste"
])

# ----- ABA 1: REGISTRAR PEÇA NOVA -----
with aba_nova:
    st.header("Cadastrar Nova Peça em Operação")
    with st.form("form_nova_peca"):
        codigo = st.text_input("Código Único da Peça (Ex: CIM-101)").strip()
        nome = st.text_input("Nome da Peça / Maquinário (Ex: Correia do Forno)").strip()
        vida_util = st.number_input("Vida Útil Máxima Recomendada (Em Horas)", min_value=1.0, value=1000.0)
        botao_cadastrar = st.form_submit_button("Iniciar Atuação da Peça")
        
        if botao_cadastrar:
            if not codigo or not nome:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                conexao = sqlite3.connect("robo_industrial.db")
                cursor = conexao.cursor()
                data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                try:
                    cursor.execute("""
                        INSERT INTO pecas_industriais (codigo, nome, vida_util_maxima, horas_trabalhadas, data_inicio, porcentagem_desgaste, status)
                        VALUES (?, ?, ?, 0.0, ?, 0.0, 'Nova - Em operação regular')
                    """, (codigo, nome, vida_util, data_atual))
                    conexao.commit()
                    st.success(f"✅ Peça '{nome}' registrada com sucesso! Começou a atuar em: {data_atual}")
                except sqlite3.IntegrityError:
                    st.error(f"❌ Erro: O código '{codigo}' já está cadastrado no sistema.")
                finally:
                    conexao.close()

# ----- ABA 2: REGISTRAR HORAS TRABALHADAS -----
with aba_atualizar:
    st.header("Registrar Horas de Funcionamento do Turno")
    with st.form("form_horas"):
        codigo_busca = st.text_input("Digite o Código da Peça que trabalhou").strip()
        horas_rodadas = st.number_input("Quantas horas essa peça rodou neste turno?", min_value=0.1, value=8.0)
        botao_atualizar = st.form_submit_button("Gravar Horas Trabalhadas")
        
        if botao_atualizar:
            conexao = sqlite3.connect("robo_industrial.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, vida_util_maxima, horas_trabalhadas FROM pecas_industriais WHERE codigo = ?", (codigo_busca,))
            resultado = cursor.fetchone()
            
            if not resultado:
                st.error("❌ Código de peça não encontrado no banco de dados.")
                conexao.close()
            else:
                nome_peca, vida_maxima, horas_atuais = resultado
                novas_horas = horas_atuais + horas_rodadas
                desgaste = round((novas_horas / vida_maxima) * 100, 2)
                
                if desgaste >= 100:
                    status_novo = "🚨 CRÍTICO - Troca Obrigatória Excedida"
                elif desgaste >= 80:
                    status_novo = "⚠️ Atenção - Planejar Próxima Manutenção"
                else:
                    status_novo = "Funcionando perfeitamente"
                
                cursor.execute("""
                    UPDATE pecas_industriais 
                    SET horas_trabalhadas = ?, porcentagem_desgaste = ?, status = ?
                    WHERE codigo = ?
                """, (novas_horas, desgaste, status_novo, codigo_busca))
                conexao.commit()
                conexao.close()
                
                if desgaste >= 100:
                    st.error(f"🚨 ALERTA MÁXIMO: A peça '{nome_peca}' atingiu {desgaste}% de desgaste! Risco de quebra imediata.")
                elif desgaste >= 80:
                    st.warning(f"⚠️ AVISO DO ROBÔ: A peça '{nome_peca}' chegou a {desgaste}% de desgaste. Planeje a troca.")
                else:
                    st.success(f"⚙️ Sucesso! Peça '{nome_peca}' atualizada. Desgaste acumulado em {desgaste}%.")

# ----- ABA 3: RELATÓRIO VISUAL -----
with aba_relatorio:
    st.header("Painel Geral de Monitoramento")
    conexao = sqlite3.connect("robo_industrial.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT codigo, nome, vida_util_maxima, horas_trabalhadas, porcentagem_desgaste, status, data_inicio FROM pecas_industriais")
    linhas = cursor.fetchall()
    conexao.close()
    
    if not linhas:
        st.info("Nenhuma peça cadastrada no sistema até o momento.")
    else:
        for peca in linhas:
            with st.container():
                st.markdown(f"### ⚙️ {peca[1]} (Código: {peca[0]})")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Horas Rodadas", f"{peca[3]} h", f"Meta: {peca[2]} h")
                col2.metric("Desgaste Real", f"{peca[4]} %")
                col3.write(f"*Status:* {peca[5]}")
                col4.write(f"Instalação: {peca[6]}")
                
                progresso = min(float(peca[4]) / 100.0, 1.0)
                st.progress(progresso)
                st.divider()
