# Bibliotecas
import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config( 
    page_title = "Cuisines",
    page_icon = "🍽️",
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
st.header('🍽️ Visão Tipos Culinários')
st.divider()

image_path = 'logo.png'
image=Image.open(image_path)
st.sidebar.image(image, width=120)


st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")


st.sidebar.markdown('## Filtros')


country_options = st.sidebar.multiselect( 
    'Escolha os países que deseja visualizar as informações', 
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'], default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])

st.sidebar.markdown("""---""")

qnt_restaurants = st.sidebar.slider(
    'Selecione a quantidade de restaurantes que deseja visualizar',
    value=int(6),
    min_value=int(1),
    max_value=int(20) )

st.sidebar.markdown("""---""")

cuisines = st.sidebar.multiselect(
        "Escolha os Tipos de Culinária", df1.loc[:,"cuisines"].unique(),
    default=[
            "Others",
            "Ramen",
            "Egyptian",
            "Ottoman",
            "Sunda",
            "Fresh Fish",
            "Polish", "Author", "Burmese", "Filipino", "Afghan", "Bengali", "Tea", "Tibetan", "Durban", "Cantonese", "Armenian", "Brazilian"])

st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by Thaísa R. Govêia')


#filtro de países
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]


#filtro de tipos culinários
linhas_selecionadas = df1['cuisines'].isin(cuisines)
df1 = df1.loc[linhas_selecionadas,:]


# ========================================
# Layout no streamlit
#=======================================

with st.container():
    st.markdown("<h3 style='text-align: center; color: white;'> Melhores Restaurantes dos Principais Tipos de Culinária </h3>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1], gap="small")
    
    with col1:
        df_aux = (df1.loc[df1['restaurant_name'] == 'Darshan', ['aggregate_rating', 'restaurant_name', 'country_code', 'city']].groupby('restaurant_name')
                                                                                             .mean()
                                                                                             .reset_index())

        col1.metric(label = 'Indiana: Darshan', value = '4.75/5.0',
                   help = f"""
                   País: India \n
                   Cidade: Pune \n
                   Preço para duas pessoas: 700 (Indian Rupees)""")

    with col2:
        lines = (df1['restaurant_name'] == 'Burger & Lobster' ) & (df1['country_code'] == 'England')
        df1.loc[lines,  ['aggregate_rating', 'restaurant_name']].groupby('restaurant_name').mean()
        col2.metric(label = 'Inglesa: Burguer & Lobster', value = '4.85/5.0',
                   help = f""" 
                   País: Inglaterra \n
                   Cidade: Londres \n
                   Preço para duas pessoas: 45 (Euros)""")
        
    with col3:
        df1.loc[df1['restaurant_name'] == 'Mandi@36', ['aggregate_rating', 'restaurant_name', 'city']].groupby(['restaurant_name', 'city']).mean()
        col3.metric(label = 'Árabe: Mandi@36	', value = '4.7/5.0',
                   help = f""" 
                   País: India \n
                   Cidade: Hyderabad \n
                   Preço para duas pessoas: 600 (Indian Rupees""")
        
    with col4:
        df1.loc[df1['restaurant_name'] == 'Sushi Samba', ['aggregate_rating', 'restaurant_name', 'city']].groupby(['restaurant_name', 'city']).mean()
        col4.metric(label = 'Japonesa: Sushi Samba', value = '4.9/5.0',
                   help = f""" 
                   País: Inglaterra \n
                   Cidade: Londres \n
                   Preço para duas pessoas: Libras(£)""")
        
    with col5:
        col5.metric(label = 'Brasileira: Braseiro da Gávea', value = '4.9/5.0',
                   help = f""" 
                   País: Brasil \n
                   Cidade: Rio de Janeiro \n
                   Preço para duas pessoas: 100(Reais R$)""")
        
st.divider()        
with st.container():
    #st.markdown("<h3 style='text-align: center; color: white;'> Top 20 Restaurantes </h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: white;'> Top {qnt_restaurants} Restaurantes </h3>" , unsafe_allow_html=True)
    df_top = (df1.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes' ]]
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).head(qnt_restaurants))
    st.dataframe(df_top, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns([2,2], gap="medium")
    
    with col1:
        st.markdown(f"<h4 style='text-align: center; color: white;'> Top {qnt_restaurants}  Melhores Tipos de Culinárias </h4>", unsafe_allow_html=True)
        df_aux = df1.loc[:, ['cuisines', 'aggregate_rating',]].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=False).reset_index().head(qnt_restaurants)

        fig = px.bar(df_aux, x='cuisines', y='aggregate_rating', labels={'cuisines': 'Tipo de Culinária', 'aggregate_rating': 'Média de Avaliação'},
               color="cuisines", color_discrete_sequence= px.colors.qualitative.Set3, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"<h4 style='text-align: center; color: white;'> Top {qnt_restaurants}  Piores Tipos de Culinárias </h4>", unsafe_allow_html=True)
        df_aux = df1.loc[:, ['cuisines', 'aggregate_rating',]].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=True).reset_index().head(qnt_restaurants)

        df_aux = df_aux.loc[df_aux['cuisines'] != 'Mineira', :]
        df_aux = df_aux.loc[df_aux['cuisines'] != 'Drinks Only', :]

        fig = px.bar(df_aux, x='cuisines', y='aggregate_rating', labels={'cuisines': 'Tipo de Culinária', 'aggregate_rating': 'Média de Avaliação'},
               color="cuisines", color_discrete_sequence= px.colors.qualitative.Set3, text_auto=True)
        
        st.plotly_chart(fig, use_container_width=True)
    