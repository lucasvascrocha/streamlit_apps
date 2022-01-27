import streamlit as st

#import plotly.graph_objects as go
#from plotly.subplots import make_subplots

def kpis(df):
    """
    Mostra os KPIS padrões
    """   
    #variáveis clientes atuais
    uf_more_freq = df.groupby(['uf']).count()['cnpj'].sort_values(ascending=False).head(1).index[0]
    porte_mean = round(df['porte_empresa'].mean())
    idade_mean = round(df['idade_anos'].mean())
    ativ_more_comon = df.groupby(['nm_secao']).count()['cnpj'].sort_values(ascending=False).head(1).index[0]

    col1, col2, col3  = st.columns(3)
    col1.metric("UF mais frequente", uf_more_freq)
    col2.metric("Porte médio", porte_mean)
    col3.metric("Idade média", idade_mean)

    st.metric('Atividade macro mais comum', ativ_more_comon, delta=None, delta_color='normal')

def graphics(df):
    """
    Mostra os gráficos padrões
    """
    #variaveis
    top_5_macro = df.groupby(['nm_secao']).count()['cnpj'].sort_values(ascending=False).head(5)
    top_5_micro = df.groupby(['nm_cnae']).count()['cnpj'].sort_values(ascending=False).head(5)

    st.subheader('Distribuições')

    fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "bar"}, {"type": "bar"}]],
    subplot_titles=("Idade","Porte")
    )
    fig.add_trace(go.Histogram(x =df['idade_anos']), row=1, col=1)
    fig.add_trace(go.Histogram(x =df['porte_empresa']) , row=1, col=2)
    fig.update_layout(height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig)

    st.subheader('Top 5 macro atividades')
    st.table(top_5_macro)

    st.subheader('Top 5 micro atividades')
    st.table(top_5_micro)






