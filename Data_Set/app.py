import pandas as pd 
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import plotly.express as px
from PIL import Image
import base64
import yfinance as yf
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import time
import io

# Mise en page et style 
st.set_page_config(layout="wide") # Elargissement des marges des pages 

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

def evolution():
        #Recuperation du lien Github
        url = "https://raw.githubusercontent.com/henrique75016/Projet_Crypto/main/Data_Set/histo1_generator.csv"
        
        # Creation de la fonction pour chatger automatiquement le dernier lien github 
        def download_file_from_github(url):
            response = requests.get(url)
            if response.status_code == 200:
                return pd.read_csv(io.StringIO(response.text))
            else:
                print(f"Erreur lors du téléchargement du fichier : {response.status_code}")
                return None
            
        # Appel de la fonction 
        df = download_file_from_github(url)
        df_copy = df.copy()
        df_copy = df_copy[['Rank','symbol','name','current_price','Variation % 24h','market_cap','total_volume','circulating_supply','high_24h','low_24h']]
        st.write('Dernière MAJ', df['last_updated'][0])
        
        # Appliquation du dégradé de couleur
        styled_df = df_copy.style.background_gradient(cmap='RdYlGn', subset=['Variation % 24h'])
        st.dataframe(styled_df, use_container_width=True)

        # Choix de la crypto ppur afficher les graphs
        coin_id = st.selectbox("Quelle Crypto veux tu choisir :", df['id'])
        df_hist = price_history(coin_id) 
        coin_symbol = df.loc[df['id'] == coin_id, 'symbol'].values[0]  
        datedeb = df_hist['timestamp'][0].strftime("%Y-%m-%d")
        datefin = df_hist['timestamp'][365]+timedelta(hours=1)

        # Graph sur les 365j
        fig = px.line(df_hist, x="timestamp", y=f"{coin_id}_price", 
                title=f"Variaton des prix de {coin_id.capitalize()} de {datedeb} à {datefin}",
                labels={"timestamp": "Date", f"{coin_id}_price": "Prix"})
        fig.update_traces(line=dict(color='goldenrod'))
        fig.update_layout( title_font=dict(color='goldenrod'))  
        st.plotly_chart(fig, use_container_width=False)
        
        # Recherche du min, max et prix courant 
        maxi = round(df_hist[f'{coin_id}_price'].max(),2)
        mini = round(df_hist[f'{coin_id}_price'].min(),2)
        current = round(df_hist[f'{coin_id}_price'][365],2)
        st.markdown(f"<h2 style='text-align: center;line-height: 0.1'>La valeur sur l'année<br></h2>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3, vertical_alignment='top')
        with col_a:
            st.markdown(f"<h3 style='text-align: center;'>Minimale<br><span style='color: red;font-size : 45px; display: inline-block;'>{ mini}$</span></h3>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<h4 style='text-align: center;;'>Courante<br> <span style='color: goldenrod; font-size : 45px;'>{current}$</span></h4>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<h4 style='text-align: center;'>Maximale<br> <span style='color: green;font-size : 45px;text-align: center;'>{maxi}$</span></h4>", unsafe_allow_html=True)
        
        st.divider()

        # Dataframe pour l'historique des 5 ans 
        data = pd.read_csv('historical1_5_years_generator.csv')
        data = data[data['symbol'] == coin_symbol]
        
        # Graph en fonction de la crypto choisi sur le 1er graph 
        fig1 = px.line(data, x='date',y='price')
        fig1.update_traces(line=dict(color='goldenrod'))
        st.markdown(f"<h5 style='text-align: center;line-height: 0.05'>Historique d'évolution sur les 5 dernières années</h5>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)

# Fonction de Fabrice sur le Web Scarpping 
def BTC_USD():
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
        # Mise en page des titres et du séparateur entre l'en-tête et le reste 
        st.markdown("""
        <h1 style="text-align: center; color: goldenrod; line-height: 0.1">Bienvenue sur votre appli Crypto</h1>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 style="text-align: center; color: goldenrod;line-height: 0.1">Designed by</h4>
        """, unsafe_allow_html=True)
        image_path = 'Projet3_image_sf.png'
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
            <div style="display: flex; justify-content: center;margin-top: -50px;margin-bottom: -50px;margin-left: -31px">
            <img src="data:image/png;base64,{encoded_string}" style="width: 300px; height: 300px"/>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()   
        # Appel de la fonction accueil
        accueil()
        
    # Si selection de la page details    
    elif selection == 'Details':
        col_1, col_2, col3 = st.columns(3, vertical_alignment='center')
        with col_1:
            image_path = 'Projet3_image_sf.png'
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(f"""
            <div style="display: flex; justify-content: center;margin-top: -50px;margin-bottom: -50px;margin-left: -31px">
            <img src="data:image/png;base64,{encoded_string}" style="width: 100px; height: 100px"/>
            </div>
            """, unsafe_allow_html=True)
        
        with col_2:
            st.markdown("""
        <h3 style="text-align: center; color: goldenrod">La Crypto en détail</h3>
        """, unsafe_allow_html=True)
        st.text("")
        st.divider()
        st.markdown("""
        <h6 style="text-align: center;color: goldenrod">Tableau des différentes cryptomonnaies</h6>
        """, unsafe_allow_html=True)
        
        # Appel de la fonction evolution pour afficher les valeurs les les courbes d'évolution
        evolution()
        st.text("")
        st.text("")
    
    # Si selection de la page Historique 
    elif selection == 'Histo': 
        database = BTC_USD()

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

    elif selection == 'test':
        return
 
# Création du sidebar avec les différentes pages 
with st.sidebar:
    date = datetime.now()
    format_date = date.strftime("%d-%m-%Y")
    format_heure = date.strftime("%H:%M")
    st.markdown(f"<h4 style='text-align: center;'>{format_date}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center;'>{format_heure}</h4>", unsafe_allow_html=True)
    st.image('Projet3_image_sf.png', width= 250)
    selection = option_menu(
            menu_title=None,
            options = ['Accueil','Details','Histo', 'test'])
    
# Appel de la fonction page
page()


#image_url = f"https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400"
#if image_url:
#    st.image(image_url, width=200)
