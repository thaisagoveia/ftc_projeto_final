import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title = "Main Page",
    page_icon = "📈", 
    layout='wide')

image_path = 'logo.png'
image=Image.open(image_path)
st.sidebar.image(image, width=120)


# Upload dados


# ===================== Manipulação dos Dados =========================

df = pd.read_csv('zomato.csv')
df1 = df.copy()

# Limpeza dos dados

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

# ============ FUNÇÃO =================
# Função que gera todos os pontos no mapa
def country_maps(df1):
    #df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map(max_bounds=True)
    marker_cluster = MarkerCluster().add_to(map)
    
    for index, location_info in df1.iterrows():
        folium.Marker( [location_info['latitude'],
                location_info['longitude']],
                popup=location_info[['city']]).add_to(marker_cluster)
    

    folium_static(map, width=1024, height=600)
    return None

# função que exporta o dataframe tratado
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


# STREAMLIT
# ========================================
# Barra Lateral
#======================================


st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown("""---""")


st.sidebar.markdown('## Filtro')


country_options = st.sidebar.multiselect( 
    'Escolha os países que deseja visualizar as informações', 
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'], default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])



# -------------------------------
# Botão de download

csv = convert_df(df1)

st.sidebar.download_button(
    label="Download dados",
    data=csv,
    file_name='zomato_df.csv',
    mime='text/csv',)


st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Thaísa R. Govêia')


#filtro de transito
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

# ========================================
# Layout no streamlit
#=======================================


st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar o seu mais novo restaurante favorito!')
st.divider()
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma')

with st.container():
    col1, col2, col3, col4,col5 = st.columns([2,2,2,2,2], gap='small')
    
    with col1:
        col1.metric(label = 'Restaurantes Cadastrados', value = '5.901')
    with col2:
        col2.metric(label = 'Países Cadastrados', value = '15')
    with col3:
        col3.metric(label = 'Cidades Cadastradas', value = '125')
    with col4:
        col4.metric(label = 'Total de Avaliações Feitas', value = '4.638.535')
    with col5:
        col5.metric(label = 'Tipos de Culinária', value = '165')
        
st.divider()
with st.container():
    st.markdown('### Encontre o restaurante mais próximo')
    country_maps(df1)
        

        