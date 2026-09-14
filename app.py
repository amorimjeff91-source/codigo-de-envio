import streamlit as st
import urllib.parse

# Configuração da página do robô com o nome do seu MEI
st.set_page_config(page_title="Robô de Mensagens", page_icon="🤖")

st.title("🤖 Painel do Robô de Lembretes")
st.write("Preencha os dados para gerar o link de envio para o seu cliente.")

st.markdown("---")

# Caixas para o comerciante preencher na tela
nome_cliente = st.text_input("Nome do Cliente:", placeholder="Ex: João Silva")
telefone = st.text_input("Telefone com DDD (Apenas números):", placeholder="Ex: 64999991111")
horario = st.text_input("Horário Agendado:", placeholder="Ex: 14:30")
servico = st.text_input("Serviço:", placeholder="Ex: Corte de Cabelo")

if st.button("🚀 Gerar Link do WhatsApp"):
    if nome_cliente and telefone and horario and servico:
        # Mensagem padrão profissional
        mensagem = f"Olá, {nome_cliente}! Passando para lembrar do seu horário hoje às {horario} para o serviço de {servico}. Se precisar remarcar, por favor avise aqui. Até logo!"
        
        msg_codificada = urllib.parse.quote(mensagem)
        link_final = f"https://whatsapp.com{telefone}&text={msg_codificada}"
        
        st.success("✅ Link gerado!")
        
        # Cria o botão verde de envio
        st.markdown(f'<a href="{link_final}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer;">📲 Enviar via WhatsApp</button></a>', unsafe_allow_html=True)
    else:
        st.error("⚠️ Por favor, preencha todos os campos!")
