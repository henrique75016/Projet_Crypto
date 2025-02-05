import pandas as pd 
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import plotly.express as px

# Fonction de la page d'accueil
def accueil():
    st.subheader("Bienvenue sur l'application Datanova - Crypto")
    st.text("")
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
    df_hist
    
    
    fig = px.line(df_hist, x="timestamp", y=f"{coin_id}_price", 
                title=f"Histogramme des prix de {coin_id.capitalize()} sur {len(df_hist)} jours",
                labels={"timestamp": "Date", f"{coin_id}_price": "Prix"})
    st.plotly_chart(fig, use_container_width=False)
    
    
    df = pd.read_csv('histo1_generator.csv')
    recherche = st.selectbox("Quelle Crypto veux tu choisir :", df['id'])

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
        df_acc.iloc[0:10,2:]

    elif selection == 'Details':
        details()
    elif selection == 'Histo':
        data = histo()
        data
        fig1 = px.line(data, x='date',y='price')
        st.plotly_chart(fig1, use_container_width=False)
with st.sidebar:
    selection = option_menu(
            menu_title=None,
            options = ['Accueil','Details','Histo'])

# Appel de la fonction page
page()
