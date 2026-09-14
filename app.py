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
CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE TECNOLOGIA1. AS PARTESCONTRATANTE: [Nome do Dono do Comércio], CPF [000.000.000-00], proprietário(a) da empresa [Nome da Loja/Salão], localizada em Indiara - GO.CONTRATADO: [Seu Nome Completo], CPF [000.000.000-00], representante do MEI [Nome do seu MEI se tiver ou Razão Social], CNPJ [00.000.000/0001-00].2. O SERVIÇOO CONTRATADO disponibilizará o acesso à página web do Robô de Lembretes automatizados via WhatsApp para uso diário do CONTRATANTE, com o objetivo de reduzir faltas de clientes e otimizar a agenda do comércio local.3. VALORES E PAGAMENTOPelo uso do sistema, o CONTRATANTE pagará o valor mensal de R$ 49,90 (quarenta e nove reais e noventa centavos).O pagamento deverá ser realizado todo dia [Escolha o dia, ex: 10] de cada mês, via PIX ou boleto bancário fornecido pelo CONTRATADO.4. DURAÇÃO E CANCELAMENTOEste contrato tem validade mensal e é renovado automaticamente a cada pagamento.O CONTRATANTE pode cancelar o serviço a qualquer momento, sem qualquer tipo de multa ou taxa de fidelidade, bastando apenas avisar com 5 dias de antecedência do próximo vencimento.5. SUPORTE E MANUTENÇÃOO CONTRATADO garante o funcionamento do link na internet e se compromete a prestar suporte em até 24 horas caso ocorra qualquer instabilidade no sistema.Por estarem de pleno acordo com as regras simples deste documento, as partes assinam de forma digital ou física.Indiara - GO, [Dia] de setembro de 2026.[Seu Nome] - Prestador (MEI)[Nome do Cliente] - Contratante💡
