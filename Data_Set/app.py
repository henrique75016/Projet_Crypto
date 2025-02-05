import pandas as pd 
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import plotly.express as px
from PIL import Image
import base64
import yfinance as yf
from datetime import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import time

# Elargissement des marges des pages 
st.set_page_config(layout="wide")

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

    
    st.markdown("""
    <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
    <u>Qu'est-ce qu'une cryptomonnaie ?</u></span><br>
    C'est de l'argent numérique, sans lien avec les banques traditionnelles, sécurisé par la cryptographie et basé sur une technologie appelée blockchain.<br>
    <br>
    <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
    <u>Blockchain : le grand livre public</u></span><br>
    C'est une chaîne de blocs qui enregistre toutes les transactions de manière transparente et sécurisée. Une fois une transaction enregistrée, elle ne peut plus être modifiée.<br>
    <br>
    <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
    <u>Exemples de cryptomonnaies</u></span><br>
        ▪️ Bitcoin (BTC) : La première et la plus connue. Un or numérique.<br>
        ▪️ Ethereum (ETH) : Permet aussi de créer des applications décentralisées (smart contracts).<br>
        <br>
    <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
    <u>Pourquoi utiliser des cryptomonnaies ?</u></span><br>
        ▪️ Décentralisation : Pas de banque, tout est géré par le réseau.<br>
        ▪️ Sécurité et transparence : Transactions publiques et difficiles à modifier.<br>
        ▪️ Accessibilité mondiale : Tout le monde peut y participer avec une connexion internet.<br>
        <br>
        <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
        <u>Comment acheter des cryptomonnaies ?</u></span><br>
        Passer par des plateformes d’échange (comme Coinbase ou Binance), créer un compte, déposer de l’argent, puis acheter des cryptos (comme le Bitcoin).<br>
        <br>
        <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
        <u>Risques à prendre en compte</u></span><br>
        ▪️ Volatilité : Les prix peuvent monter ou descendre rapidement.<br>
        ▪️ Sécurité : Perdre l’accès à ton portefeuille peut signifier perdre tes cryptos.<br>
        ▪️ Régulation : Les gouvernements surveillent les cryptos, ce qui peut affecter leur usage.<br>
        <br>
        <span style= "font-size : 30px; font-weight: bold;color: goldenrod">
        <u>Le minage</u></span><br>
        C'est le processus de validation des transactions via des ordinateurs puissants. Les mineurs sont récompensés par des cryptomonnaies.<br>
        <br>
        En résumé, les cryptomonnaies sont un moyen d'échange numérique sécurisé, décentralisé et transparent. Elles peuvent être utilisées pour investir, acheter des biens, ou même créer des applications décentralisées. Cependant, elles comportent des risques liés à la sécurité, la volatilité des prix, et la régulation."""
        , unsafe_allow_html=True)
  
# Fonction de la page Details
def details():
    st.image('Projet3_image_sf.png', width=100)
    st.markdown("""
        <h2 style="text-align: center;">La Crypto en détail</h2>
        """, unsafe_allow_html=True)
     
    df = pd.read_csv('histo1_generator.csv')    
    coin_id = st.selectbox("Quelle Crypto veux tu choisir :", df['id'])
    df_hist = price_history(coin_id)    
    #st.dataframe(df_hist, use_container_width=True)
    df_hist
    fig = px.line(df_hist, x="timestamp", y=f"{coin_id}_price", 
                title=f"Histogramme des prix de {coin_id.capitalize()} de {df_hist['timestamp'][0]} à {df_hist['timestamp'][365]}",
                labels={"timestamp": "Date", f"{coin_id}_price": "Prix"})
    fig.update_traces(line=dict(color='yellow'))
    st.plotly_chart(fig, use_container_width=False)
    
# Fonction de historique des crypto sur 5 ans
def histo():
    data = pd.read_csv('historical1_5_years_generator.csv')
    test = st.selectbox("Quelle Crypto veux tu choisir :", data['name'])
    data = data[data['name'] == test]
    return data

def test():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date = d1
    d2 = date.today() - timedelta(days=1500)
    d2 = d2.strftime("%Y-%m-%d")
    start_date = d2

    data = yf.download('BTC-USD', 
                      start=start_date, 
                      end=end_date, 
                      progress=False)
    data["Date"] = data.index
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
    data.reset_index(drop=True, inplace=True)
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    return data


# Determination du nombre de page et de la selection 
def page():
    if selection == 'Accueil':
        accueil()
        

    # Si selection de la page details    
    elif selection == 'Details':
        details()
        st.markdown("""
    <h6 style="text-align: center;">Tableau des différentes cryptomonnaie</h6>
    """, unsafe_allow_html=True)
    
        df_acc = pd.read_csv('histo1_generator.csv')
        df_acc = df_acc[['Rank','symbol','name','current_price','Variation % 24h','market_cap','total_volume','circulating_supply','high_24h','low_24h']]
        st.dataframe(df_acc.iloc[0:10,::], use_container_width=True)

    # Si selection de la page Historique 
    elif selection == 'Histo':
        data = histo()
        data
        fig1 = px.line(data, x='date',y='price')
        st.plotly_chart(fig1, use_container_width=True)
    
    # Si selection de la page ??
    elif selection =='test':
        database = test()

        database['Date'] = pd.to_datetime(database['Date'])
        figure = go.Figure(data=[go.Candlestick(
            x=database['Date'],
            open=database['Open'],
            high=database['High'],
            low=database['Low'],
            close=database['Close'])])

        figure.update_layout(
            title="Bitcoin Price Analysis",
            xaxis_rangeslider_visible=False, 
            xaxis_title="Date",  
            yaxis_title="Price (USD)")
        st.plotly_chart(figure, use_container_width=True)

        st.header("Pourquoi BTC-USD est continu ?")
        st.write("""Les crypto-monnaies comme Bitcoin (BTC-USD) ne sont pas limitées aux horaires de la bourse. Elles s'échangent tout le temps sur diverses plateformes mondiales (Binance, Coinbase, Kraken, etc.).
Ainsi, le graphique de BTC-USD est continu, car il reflète un marché sans interruption.
Pourquoi le graphique "BTC" a des espaces ?
Si "BTC" correspond à un ETF Bitcoin (comme BITO ou BTCC) ou un indice basé sur Bitcoin, alors ce produit est coté sur une bourse traditionnelle (ex : NASDAQ, NYSE).
Ces bourses ont des horaires de trading spécifiques (généralement de 9h30 à 16h00 heure de New York, du lundi au vendredi).
Pendant les week-ends et les jours fériés, aucune transaction n’a lieu, ce qui crée les espaces vides sur le graphique.
Pourquoi la confusion avec le marché du Forex (USD) ?
Le marché du Forex (échange de devises, y compris USD) fonctionne presque 24h/24 en semaine, mais il ferme le week-end.
Cependant, BTC-USD ne dépend pas du Forex, mais du marché crypto global, qui lui ne s’arrête jamais.
Conclusion :
BTC-USD = Bitcoin coté en dollars, échangé en continu 24/7 → Graphique sans trous.
BTC = Un produit financier (ETF, indice) coté en bourse traditionnelle → Graphique avec des espaces car la bourse ferme la nuit et les week-ends""")


# Création du sidebar avec les différentes pages 
with st.sidebar:
    date = datetime.now()
    format_date = date.strftime("%d-%m-%Y")
    format_heure = date.strftime("%H:%M")
    st.write(f"{format_date}")
    st.write(f"{format_heure}")
    
    st.image('Projet3_image_sf.png', width= 250)
    selection = option_menu(
            menu_title=None,
            options = ['Accueil','Details','Histo','test'])
    
# Appel de la fonction page
page()


#image_url = f"https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400"
#if image_url:
#    st.image(image_url, width=200)

