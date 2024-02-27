# Bibliotecas
import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Countries",
    page_icon = "🌎",
    layout='wide')
# Upload dados

df = pd.read_csv('zomato.csv')
df1 = df.copy()

# Limpeza dos dados

# limpeza dos dados

# remover coluna "Switch to order menu" pois só tem um valor - Yes 
df1.drop(columns ='Switch to order menu', inplace=True)

# remover linhas NaN da coluna Cuisines (única coluna que possui NaN)
df1.dropna(inplace=True)

# preenchimento do nome dos países

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

df1['Country Code'] = df1['Country Code'].map(COUNTRIES)
Df1 = df1.rename(columns={'Country Code': 'Country'})

# preenchimento das categorias de preço 

PRICE_TYPE = {
    1: 'cheap',
    2: 'normal',
    3: 'expensive',
    4: 'gourmet'    
}

df1['Price range'] = df1['Price range'].map(PRICE_TYPE)

#preenchimento das categorias de cor

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

df1['Rating color'] = df1['Rating color'].map(COLORS)

# renomeando as colunas do DataFrame

def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

df1 = rename_columns(df1)

# categorizando por apenas um tipo de culinária

df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])




# STREAMLIT
# ========================================
# Barra Lateral
#=======================================
st.header('🌎 Visão Países')

image_path = 'logo.png'
image=Image.open(image_path)
st.sidebar.image(image, width=120)


st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")


st.sidebar.markdown('## Filtro')


country_options = st.sidebar.multiselect( 
    'Escolha os países que deseja visualizar as informações', 
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'], default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada'])

st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by Thaísa R. Govêia')


#filtro de transito
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

# ========================================
# Layout no streamlit
#=======================================

with st.container():
    st.markdown("<h4 style='text-align: center; color: white;'> Quantidade de Restaurantes por País </h4>", unsafe_allow_html=True)
    #st.subheader('Quantidade de Restaurantes por País')
    df_aux = df1.loc[:, ['country_code', 'restaurant_id']].groupby('country_code').nunique().sort_values('restaurant_id', ascending=False).reset_index()
    fig = px.bar(df_aux, x='country_code', y='restaurant_id', labels={'restaurant_id': 'Quantidade de Restaurantes', 'country_code': 'Países'}, 
                 color="country_code", color_discrete_sequence= px.colors.qualitative.Set3, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.markdown("<h4 style='text-align: center; color: white;'> Quantidade de Cidades por País </h4>", unsafe_allow_html=True)
    df_aux = df1.loc[:, ['country_code', 'city']].groupby('country_code').nunique().sort_values('city', ascending=False).reset_index()
    fig = px.bar(df_aux, x='country_code', y='city', labels={'country_code': 'Países', 'city': 'Quantidade de Cidades'}, 
                 color="country_code", color_discrete_sequence= px.colors.qualitative.Set3, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    
    col1, col2 = st.columns([4,4], gap="large")
    
    with col1:
        st.markdown("<h4 style='text-align: center; color: white;'> Média de Avaliações feitas por País </h4>", unsafe_allow_html=True)
        df_aux = df1.loc[:, ['aggregate_rating', 'country_code']].groupby('country_code').mean().sort_values('aggregate_rating', ascending=False).reset_index()
        fig = px.bar(df_aux, x='country_code', y='aggregate_rating', labels={'country_code': 'Países', 'aggregate_rating': 'Média das avaliações'},
                     color="country_code", color_discrete_sequence= px.colors.qualitative.Set3, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("<h4 style='text-align: center; color: white;'> Média de Preço para Duas Pessoas por País </h4>", unsafe_allow_html=True)
        df_aux = (df1.loc[:, ['country_code', 'average_cost_for_two']].groupby('country_code')
                                                              .mean()
                                                              .sort_values('average_cost_for_two', ascending=False)
                                                              .reset_index())
        fig = px.bar(df_aux, x='country_code', y='average_cost_for_two', labels={'country_code': 'Países', 'average_cost_for_two':'Média de Preço prato para duas Pessoas'},
               color="country_code", color_discrete_sequence= px.colors.qualitative.Set3, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
        

            