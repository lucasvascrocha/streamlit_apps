from os import sep
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import datetime as dt 
import base64
from io import BytesIO

#from google.cloud import bigquery, storage
#from google.oauth2 import service_account
import warnings
warnings.filterwarnings('ignore')

import dashs as dashs

credentials = service_account.Credentials.from_service_account_file(
'bix-tecnologia-dev-16a40ea724a6.json')
project_id = 'bix-tecnologia-dev'
bigquery_client = bigquery.Client(credentials= credentials,project=project_id)


def recomender():
    '''
    Menu de opções de testar a ferramenta com dados fake ou com dados prórpios
    '''
    st.title('')               
    st.title('Recomendação de Leads')
    st.subheader('Encontre leads para o seu negócio!')
    
    image = Image.open('images/dash.png')
    st.image(image, use_column_width=True)

    st.write('Entre com os dados do cnpj de seus clientes através de um excel para recomendarmos os leads mais quentes!')

    menu = ["Escolha uma opção","Testar com nossos dados!","Usar os CNPJs de meus clientes"]
    choice = st.selectbox("Menu",menu)

    if choice == "Testar com nossos dados!":
        nossos_dados()

    if choice == "Usar os CNPJs de meus clientes":
        seus_dados()


def nossos_dados():
    '''
    Exemplo da ferramenta com dados fake 
    '''
    st.subheader('Usaremos CNPJs de clientes fictícios para simular a utilização da aplicação')
    df_concorrentes = pd.read_csv('df_concorrentes.csv',sep=',',decimal='.' )
    df_clientes_atuais = pd.read_csv('df_clientes_atuais.csv',sep=',',decimal='.' )
    df_clientes_recomendados = pd.read_csv('df_clientes_recomendados.csv',sep=',',decimal='.' )
    show_results(df_concorrentes, df_clientes_atuais, df_clientes_recomendados)

def seus_dados():
    '''
    Entrada dos dados lead em sistema de login
    '''
    st.subheader('Faça upload de uma planilha do excel com os CNPJs dos seus clientes')
    st.write('Faremos uma análise dos seus clientes atuais buscando padrões para recomendar clientes similares')

    with st.expander("Fazer cadastro"):
        #salvar dados lead em dataframe
        name = st.text_input("Nome")
        cargo = st.text_input("Cargo")
        empresa = st.text_input("Empresa")
        email = st.text_input("E-mail")
        cnpj_empresa_lead = st.number_input("CNPJ da sua empresa (somente números)",step = 1)
        dia = dt.datetime.today().strftime(format='20%y%m%d%H%M')

        df_dados_lead = pd.DataFrame({"id":[dia],  "name": [name], "cargo": [cargo], "empresa": [empresa], "email": [email], "cnpj":[cnpj_empresa_lead] })
        
        if st.checkbox('Aceito receber e-mails da Bix-tecnologia') and name:
            st.write('Usuário: ', name)
            st.write('Senha: contateste')

    st.subheader("Login")
    username = st.text_input("User Name")
    password = st.text_input("Password",type='password')

    if password == 'contateste':
        st.title('Login autorizado')
        #aqui inicializa o código de recomendação
        save_data_lead(df_dados_lead)
        input_table_cnpj(name,empresa,cnpj_empresa_lead)
        
                

def input_table_cnpj(name,empresa,cnpj_empresa_lead):
    '''
    Início da coleta dos dados de cnpj do lead
    '''
    with st.expander("Modelo de planilha"):
        st.write('Crie uma planilha com a primeira coluna A1 com título "cnpj" e cole nas células abaixo os cnpjs dos clientes atuais de sua empresa')
        st.write('O cnpj pode ser escrito com os separadores " .  /  - " ou somente os números')
        st.write('Exemplo:')
        image = Image.open('images/exemplo_cnpj_entrada.png')
        st.image(image, use_column_width=True)
        st.write('salve a planilha no formato excel e faça o upload')

    st.write(name, 'Faça upload dos CNPJs que já são clientes da ', empresa)
    file  = st.file_uploader('planilha excel com CNPJs (.xlsx)', type = 'xlsx')

    if file:
        cnpjs_clientes = pd.read_excel(file)
        cnpjs_clientes.columns = ['cnpj']
        cnpjs_clientes['cnpj'] = cnpjs_clientes['cnpj'].str.replace('.','').str.replace('/','').str.replace('-','')
        cnpj_empresa_lead = int(cnpj_empresa_lead)
        df_concorrentes, df_clientes_atuais, df_clientes_recomendados = make_recomendation(cnpjs_clientes, cnpj_empresa_lead)

        show_results(df_concorrentes, df_clientes_atuais, df_clientes_recomendados)

def show_results(df_concorrentes, df_clientes_atuais, df_clientes_recomendados):
    """
    De posse das recomendações é mostrado dashboards e relatórios com as informações recomendadas assim como s liberação os dados para download
    
    """
    try:
        st.title("")
        col1, col2, col3 = st.columns([1,6,1])
        with col1:
            st.write("")
        with col2:
            st.title("Clientes atuais")
        with col3:
            st.write("")

        dashs.kpis(df_clientes_atuais)
        dashs.graphics(df_clientes_atuais)
        st.write('Donwload dos informações dos clientes atuais')
        df_clientes_atuais = df_clientes_atuais.drop(['CENTROID_ID','distance_from_closest_centroid'],axis=1)
        st.markdown(get_table_download_link2(df_clientes_atuais,'clientes atuais'), unsafe_allow_html=True)
    except:
        exit

    try:
        st.title("")
        col1, col2, col3 = st.columns([1,6,1])
        with col1:
            st.write("")
        with col2:
            st.title("Concorrentes")
        with col3:
            st.write("")

        dashs.kpis(df_concorrentes)
        dashs.graphics(df_concorrentes)
        st.write('Donwload dos concorrentes identificados')
        df_concorrentes = df_concorrentes.drop(['CENTROID_ID','distance_from_closest_centroid','CENTROID_ID_1','distance_from_closest_centroid_1'],axis=1)
        st.markdown(get_table_download_link2(df_concorrentes,'concorrentes'), unsafe_allow_html=True)
    except:
        exit

    try:
        st.title("")
        col1, col2, col3 = st.columns([1,6,1])
        with col1:
            st.write("")
        with col2:
            st.title("Clientes Recomendados")
        with col3:
            st.write("")

        dashs.kpis(df_clientes_recomendados)
        dashs.graphics(df_clientes_recomendados)
        st.write('Donwload dos Leads recomendados')
        df_clientes_recomendados = df_clientes_recomendados.drop(['CENTROID_ID','distance_from_closest_centroid','CENTROID_ID_1','distance_from_closest_centroid_1'],axis=1)
        st.markdown(get_table_download_link2(df_clientes_recomendados,'Leads recomendados'), unsafe_allow_html=True)
    except:
        exit

    st.title('')
    st.title('Que tal receber as recomendações de forma personalizada?')
    st.subheader('Este algoritimo foi desenvolvido de forma genérica, mas é possível adaptá-lo a sua realidade!')
    st.write('Um algoritimo desenvolvido sob medida pode entregar uma recomendação ainda mais precisa.')
    st.write('As variáveis utilizadas para o desenvolvimento funcionam ainda melhor se forem direcionadas a realidade específica de cada cliente.')
    st.write('A Bix-tecnologia possui um time treinado para desenvolver esse tipo de solução e está aguardando o seu contato.')
    st.write('Entre em contato conosco para saber mais sobre como gerar Leads personalizados, atuamos em toda a cadeia de dados, desde a coleta e estruturação dos dados, disponibilização de dados em BI, data science e sistemas.')
    st.write('Saiba mais na aba "sobre" ou entre em contato conosco.')
    st.write('Telefone: (48) 99659 5490 / (47) 99981 0094')
    st.write('Email : contato@bixtecnologia.com.br')

def save_data_lead(df_dados_lead):
    '''
    Salvar os dados do lead em uma tabela no bigquery
    '''
    #salvando dados leads bigquery
    credentials = service_account.Credentials.from_service_account_file(
    'bix-tecnologia-dev-16a40ea724a6.json')
    project_id = 'bix-tecnologia-dev'
    bigquery_client = bigquery.Client(credentials= credentials,project=project_id)
    table_id = 'bix-tecnologia-dev.cnpj.cadastro'
    job = bigquery_client.load_table_from_dataframe(df_dados_lead, table_id ) 


def make_recomendation(cnpjs_clientes,cnpj_empresa_lead):
    '''
    De posse dos dados faz a recomendação (a recomendação é feita buscando os cnpjs passados em uma tabela do BQ)
    Esta tabela do BQ já está com grupos formados e as respectivas distâncias intercluster de cada CNPJ
    A recomendação funciona da seguinte forma:
    Para cada CNPJ de cliente atual do lead:
    Trazemos os dados da empresa necessários para rodar o modelo, que se encontra no BQ (de para por cnpj)
    Rodamos o predict do modelo que está no BQ usando BQML
    Pegamos o grupo em que este cnpjfoi previsto, depois recomendamos os x cnpjs com distância intercluster mais próxima
    Da mesma forma para os concorrentes
    '''

    ###############################################CONCORRENTES#################################################

    QUERY = f"""

    WITH aprox as (

    SELECT 
        CENTROID_ID,
        round(distance_from_closest_centroid,3) as 	distance_from_closest_centroid
    FROM `bix-tecnologia-dev.cnpj.predicted_full_adress_100`
    WHERE cnpj =  {cnpj_empresa_lead} ),

    filtrar as (
    SELECT 
        cnpj, razao_social, nome_fantasia, municipio, ddd_telefone_1, ddd_telefone_2, correio_eletronico, CENTROID_ID, porte_empresa, idade_anos, capital_social_empresa, uf, nm_natureza_juridica, nm_subclass_natureza_juridica, nm_secao, nm_divisao, nm_grupo, nm_classe, nm_cnae,
        round(distance_from_closest_centroid,3) as distance_from_closest_centroid
    FROM `bix-tecnologia-dev.cnpj.predicted_full_adress_100`
        )
    SELECT * FROM aprox 
        LEFT JOIN filtrar ON aprox.CENTROID_ID = filtrar.CENTROID_ID AND aprox.distance_from_closest_centroid = filtrar.distance_from_closest_centroid 
        WHERE cnpj not in(20230253000169)
        """

    Query_Results = bigquery_client.query(QUERY)
    df_concorrentes = Query_Results.to_dataframe()
    #View top few rows of result
    #st.write('Concorrentes')
    #st.dataframe(df_concorrentes.head())
  
    ###############################################CLIENTES ATUAIS#################################################
    
    QUERY = f"""

    SELECT * FROM `bix-tecnologia-dev.cnpj.predicted_full_adress_100` 
    WHERE cnpj  IN {tuple(np.int64(cnpjs_clientes['cnpj']))}

    """
    Query_Results = bigquery_client.query(QUERY)
    df_clientes_atuais = Query_Results.to_dataframe()
    #View top few rows of result
    #st.write('Clientes atuais')
    #st.dataframe(df_clientes_atuais.head())

    ###############################################RECOMENDAÇÃO#################################################
  
    QUERY = f"""

    WITH all_results AS (
  SELECT
    *
  FROM
    ML.PREDICT(MODEL `bix-tecnologia-dev.cnpj.kmeans100`,
      (
      #buscando features de entrada
      SELECT * FROM `bix-tecnologia-dev.cnpj.cnpj_full_sem_mei_ativo` 
      WHERE cnpj IN {tuple(np.int64(cnpjs_clientes['cnpj']))}
      )) ),
      
#unnest para trazer distancia

  distance AS (
  SELECT
    cnpj,    MIN(NEAREST_CENTROIDS_DISTANCE.DISTANCE) AS distance_from_closest_centroid,    porte_empresa,
    idade_anos,    capital_social_empresa,    uf,    nm_natureza_juridica,    nm_subclass_natureza_juridica,
    nm_secao,    nm_divisao,    nm_grupo,    nm_classe,    nm_cnae
  FROM
    all_results
  CROSS JOIN
    UNNEST(NEAREST_CENTROIDS_DISTANCE) AS NEAREST_CENTROIDS_DISTANCE
  GROUP BY
    cnpj,    porte_empresa,    idade_anos,    capital_social_empresa,   uf,    nm_natureza_juridica,    nm_subclass_natureza_juridica,
    nm_secao,    nm_divisao,    nm_grupo,    nm_classe,    nm_cnae ),

  clusteres AS (
  SELECT
    cnpj,
    CENTROID_ID
  FROM
    all_results ),

    joined as (
SELECT
  *
FROM clusteres 
LEFT JOIN   distance USING ( cnpj) ),
    
    #criando campo de distancia aproximada
    
    aprox as (

    SELECT 
        CENTROID_ID,  round(distance_from_closest_centroid,4) as 	distance_from_closest_centroid
    FROM joined
    #WHERE CENTROID_ID != 41
    ),

#trazendo dados com todos os cnpjs com valores de centroid e distancia após predição de toda a base

    filtrar as (
SELECT 
    cnpj, razao_social, nome_fantasia, municipio, ddd_telefone_1, ddd_telefone_2, correio_eletronico, CENTROID_ID, porte_empresa, idade_anos, capital_social_empresa, uf, nm_natureza_juridica, nm_subclass_natureza_juridica, nm_secao, nm_divisao, nm_grupo, nm_classe, nm_cnae,
    round(distance_from_closest_centroid,4) as distance_from_closest_centroid
 FROM `bix-tecnologia-dev.cnpj.predicted_full_adress_100` )
    
    #fazendo join dos preditos com a base pelo centroid e distancia

    SELECT * 
    FROM aprox
    LEFT JOIN filtrar ON aprox.CENTROID_ID = filtrar.CENTROID_ID AND aprox.distance_from_closest_centroid = filtrar.distance_from_closest_centroid 

#não mostrar empresas que já são clientes

    WHERE cnpj not in {tuple(np.int64(cnpjs_clientes['cnpj']))}
;
    """
    Query_Results = bigquery_client.query(QUERY)
    df_clientes_recomendados = Query_Results.to_dataframe()
    #View top few rows of result
    #st.write('Clientes recomendados')
    #st.dataframe(df_clientes_recomendados.head())

    return df_concorrentes, df_clientes_atuais, df_clientes_recomendados
  

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    for excel files
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download file</a>' # decode b'abc' => abc

def get_table_download_link2(df,name):
    """
    For csv files
    """
    csv = df.to_csv(index=False, sep=';',encoding='latin1')
    b64 = base64.b64encode(csv.encode('latin1')).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{name}.csv">{name}</a>'
    return href


