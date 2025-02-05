import pandas as pd 
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import plotly.express as px
from PIL import Image
import base64

# Elargissement des marges des pages 
st.set_page_config(layout="wide")

# Fonction de la page d'accueil
def accueil():
    st.markdown("""
        <h1 style="text-align: center;">Bienvenue sur votre appli Crypto</h1>
        """, unsafe_allow_html=True)
    st.markdown("""
        <h2 style="text-align: center;">Designed by</h2>
        """, unsafe_allow_html=True)
    image_path = 'Projet3_image_sf.png'
    with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
            <div style="display: flex; justify-content: center">
            <img src="data:image/png;base64,{encoded_string}" style="width: 300px; height: 300px;"/>
            </div>
            """, unsafe_allow_html=True)

    st.write('Top 10 des Crypto-monnaie')
  
# Fonction de la page Details
def details():
    st.write("Vous êtes ici pour plus de détails")
        # Utilisation de l'APi pour un historique sur 365 jours 
    def price_history(coin_id, currency="usd", days=365):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
        "vs_currency": currency,
        "days": days
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            prices = data['prices']
            df = pd.DataFrame(prices, columns=["timestamp", f"{coin_id}_price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
            return df
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None
    
    df = pd.read_csv('histo1_generator.csv')    
    coin_id = st.selectbox("Quelle Crypto veux tu choisir :", df['id'])
    df_hist = price_history(coin_id)    
    st.dataframe(df_hist, use_container_width=True)
    
    col_a,  col_df,  col_b = st.columns(3,vertical_alignment='center')
    with col_a:
        st.write(f"Le prix du {coin_id} est de {df_hist[2:,:365]}")
    with col_df:
        df_hist
    with col_b:
        st.text("")


    fig = px.line(df_hist, x="timestamp", y=f"{coin_id}_price", 
                title=f"Histogramme des prix de {coin_id.capitalize()} de {df_hist['timestamp'][0]} à {df_hist['timestamp'][365]}",
                labels={"timestamp": "Date", f"{coin_id}_price": "Prix"})
    st.plotly_chart(fig, use_container_width=False)
    
# Fonction de historique des crypto sur 5 ans
def histo():
    data = pd.read_csv('historical1_5_years_generator.csv')
    test = st.selectbox("Quelle Crypto veux tu choisir :", data['name'])
    data = data[data['name'] == test]
    return data



# Determination du nombre de page et de la selection 
def page():
    if selection == 'Accueil':
        accueil()
        df_acc = pd.read_csv('histo1_generator.csv')
        df_1 = pd.read_csv('histo1_generator.csv')
        df_1
        df_acc = df_acc[['market_cap_rank','symbol','name','current_price','price_change_percentage_24h','market_cap','total_volume','circulating_supply']]
        st.dataframe(df_acc.iloc[0:10,::], use_container_width=True)

    elif selection == 'Details':
        details()
    elif selection == 'Histo':
        data = histo()
        data
        fig1 = px.line(data, x='date',y='price')
        st.plotly_chart(fig1, use_container_width=True)
with st.sidebar:
    selection = option_menu(
            menu_title=None,
            options = ['Accueil','Details','Histo'])

# Appel de la fonction page
page()
