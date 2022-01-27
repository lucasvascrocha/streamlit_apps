import streamlit as st
from PIL import Image

def home():
    st.title('')               
    st.title('Recomendação de Leads')
    st.subheader('Encontre leads para o seu negócio!')
    image = Image.open('images/home.png')
    st.image(image, use_column_width=True)

    st.subheader('Que tal receber uma lista de clientes qualificados de acordo com a realidade do seu negócio?')
    st.write('Através do uso de inteligência artificial desenvolvemos um algoritimo capaz de fazer uma recomendação de leads personalizada para cada empresa específica!')
    st.write('O algoritimo analisa cerca de 20 milhões de cnpjs de empresas recomendando as mais aderentes as personas identificadas em seus clietnes fidelizados.')

    st.title('')
    st.subheader('Como é possível?')
    st.write('O algoritimo identifica as diversas personas de seus clientes fidelizados através de seus cnpjs.')
    st.write('As personas de seus clientes são identificadas através de padrões detectados nas características destas empresas.')
    st.write('Algumas das características que o algoritimo utiliza para realizar a recomendação são: porte, idade da empresa, localidade, capital, tipos de atividades macro e micro, dentre outros.')

    st.title('')
    st.subheader('Os cnpjs recomendados terão características similares a de seus clientes já fidelizados.')
    st.write('O que aumenta a probabilidade de se tornarem seus novos clientes!')
    image = Image.open('images/ima.png')
    st.image(image, use_column_width=True)

    st.subheader('Ainda tem mais!')
    st.write('De brinde o algoritimo entrega um dashboard com os principais pontos encontrados nos seus clientes fidelizados, nos Leads recomendados e nos seus CONCORRENTES.')
    st.write('Isso mesmo, o algoritimo é capaz de levantar uma lista com empresas de ação similar à sua.')
    st.write('Todas as informações geradas nos dashboards também são liberadas para download')

    st.subheader('Experimente, é gratuito!')
    st.write('Vá até a aba "Recomendador de Leads" e faça um teste com nossos dados ou entre com os cnpjs de seus clientes e receba as recomendações agora mesmo!')

        
        
        
        #col1, col2, col3 = st.columns([1,6,1])

        #with col1:
        #    st.write("")

        #with col2:
        #    st.image('https://media.giphy.com/media/rM0wxzvwsv5g4/giphy.gif', width=400)

        #with col3:
        #    st.write("")
        
        #st.image('https://media.giphy.com/media/rM0wxzvwsv5g4/giphy.gif', width=400)    
        #image = Image.open('imagens/logo.jpg')



        #st.write('Este explorador funciona melhor para ações, porém também suporta alguns fundos imobiliários')    
        #st.write('Os parâmetros utilizados em grande maioria foram seguindo as teorias de Benjamin Graham')