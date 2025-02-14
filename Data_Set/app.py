import pandas as pd 
import streamlit as st
import numpy as np
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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

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

# Fonction pour récupérer les logos du Dataframe
def get_crypto_logo(crypto_id):
    df = pd.read_csv('histo1_generator.csv')
    image_url = df.loc[df['id'] == crypto_id, 'image'].values
    if len(image_url) > 0:
        return image_url[0]
    else:
        return None

# Creation de la fonction pour chatger automatiquement le dernier lien github 
def download_file_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.text))
    else:
        print(f"Erreur lors du téléchargement du fichier : {response.status_code}")
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
        Passer par des plateformes d’échange (comme Coinbase ou Binance, Kraken), créer un compte, déposer de l’argent, puis acheter des cryptos (comme le Bitcoin).<br>
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
            
        # Appel de la fonction 
        df = download_file_from_github(url)
        df_copy = df.copy()
        df_copy = df_copy[['Rank','symbol','name','current_price','Variation % 24h','market_cap','total_volume','circulating_supply','high_24h','low_24h']]

        # Appliquation du dégradé de couleur
        styled_df = df_copy.style.background_gradient(cmap='RdYlGn', subset=['Variation % 24h'],vmin=-5,vmax=5)
        st.markdown("""
        <h3 style="text-align: center;color: goldenrod">Tableau des différentes cryptomonnaies</h3>
        """, unsafe_allow_html=True)
        st.write('Dernière MAJ', df['last_updated'][0])
        st.dataframe(styled_df, use_container_width=True)

        st.divider()
        # Choix de la crypto ppur afficher les graphs
        col_1, col_2, col_3 = st.columns(3,vertical_alignment='center')
        st.markdown(""" <style>.selectbox-label {
            line-height: 0.8px;
            font-size: 30px;
            color: white;
            margin-bottom : 10px;
            margin-top : 30px; } </style> """, unsafe_allow_html=True)

        with col_1:
            st.markdown('<p class="selectbox-label">Quelle Crypto veux-tu choisir :</p>', unsafe_allow_html=True)
            coin_id = st.selectbox("", df['id'])
            
        df_hist = price_history(coin_id) 
        coin_symbol = df.loc[df['id'] == coin_id, 'symbol'].values[0]  
        datedeb = df_hist['timestamp'][0].strftime("%Y-%m-%d")
        datefin = df_hist['timestamp'].iloc[-1]+timedelta(hours=1)

        with col_2:
            logo_url = get_crypto_logo(coin_id)
            if logo_url:
                st.markdown(f"<div style='text-align: center;margin-top: -40px;margin-bottom: -70px;margin-right: -100px'><img src='{logo_url}' width='100'></div>", unsafe_allow_html=True)
            else:
                st.write("Logo non disponible pour cette crypto.")
        with col_3:
            variation = df.loc[df['id'] == coin_id, 'Variation % 24h'].values[0]
            color = 'green' if variation > 0 else 'red'
            st.markdown(f"""
    <h3 style='text-align: center;'>Dernière variation : {coin_id.capitalize()}<br>
    <span style='color: {color}; font-size: 40px; display: block; text-align: center;'>{variation} %</span></h3>
""", unsafe_allow_html=True)

        st.text("")
        st.text("")
        st.markdown(f"<h3 style='text-align: center;color: goldenrod'>{coin_id.capitalize()} : Variaton des prix de {datedeb} à {datefin}</h3>",unsafe_allow_html=True)
        # Graph sur les 365j
        fig = px.line(df_hist, x="timestamp", y=f"{coin_id}_price", 
                labels={"timestamp": "Date", f"{coin_id}_price": "Prix"})
        fig.update_traces(line=dict(color='goldenrod'))
        #fig.update_layout( title_font=dict(color='goldenrod'))  
        st.plotly_chart(fig, use_container_width=False)
        
        # Recherche du min, max et prix courant 
        maxi = round(df_hist[f'{coin_id}_price'].max(),2)
        mini = round(df_hist[f'{coin_id}_price'].min(),2)
        current = round(df_hist[f'{coin_id}_price'].iloc[-1],2)
        st.markdown(f"<h2 style='text-align: center;line-height: 0.1'>La valeur sur l'année<br></h2>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3, vertical_alignment='top')
        with col_a:
            st.markdown(f"<h4 style='text-align: center;'>Minimale<br><span style='color: red;font-size : 45px; display: inline-block;'>{ mini}$</span></h4>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<h4 style='text-align: center;;'>Courante<br> <span style='color: goldenrod; font-size : 45px;'>{current}$</span></h4>", unsafe_allow_html=True)
        with col_c:
            st.markdown(f"<h4 style='text-align: center;'>Maximale<br> <span style='color: green;font-size : 45px;text-align: center;'>{maxi}$</span></h4>", unsafe_allow_html=True)
        
        st.divider()

        # Dataframe pour l'historique des 5 ans 
        data = pd.read_csv('historical1_5_years_generator.csv')
        data = data[data['symbol'] == coin_symbol]
        
        # Graph en fonction de la crypto choisi sur le 1er graph 
        fig1 = px.line(data, x='date',y='price',
                       labels={"date": "Date", 'price': "Prix"})
        fig1.update_traces(line=dict(color='goldenrod'))
        st.markdown(f"<h3 style='text-align: center;line-height: 0.05;color: goldenrod'>Historique d'évolution sur les 5 dernières années</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)


        st.divider()

        # Machine learning 
        crypto_search = f'{coin_symbol}-USD' # Variable du symbole de la crypto à chercher
        def prediction(crypto_search):
            today = date.today()
            d1 = today.strftime("%Y-%m-%d")
            end_date = d1
            periode = 1000 # Variable du nombre de jours a prendre en historique
            d2 = date.today() - timedelta(days=periode) #periode de reference pour l'historique
            d2 = d2.strftime("%Y-%m-%d")
            start_date = d2
            data = yf.download(crypto_search, start=start_date, end=end_date, progress=False)
            data["Date"] = data.index
            data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
            data.reset_index(drop=True, inplace=True)
            return data
        data = prediction(crypto_search)
        #data
                # Réinitialiser l'index pour convertir la colonne 'Date' en une colonne normale
        data.reset_index(inplace=True)

        # Aplatir les noms des colonnes
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

        # Calcul des indicateurs techniques
        #Moyenne mobile simple (SMA) à 50 jours (SMA_50) :
        #La moyenne mobile simple est une moyenne des prix de clôture sur les 50 derniers jours.
        #Elle permet de lisser les fluctuations des prix sur une période courte pour observer les tendances.
        #SMA200 pour calculer la moyenne mobile sur plus long terme
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()

        #Relative Strength Index (RSI) :
        #Le RSI est un indicateur technique qui mesure la vitesse et le changement des mouvements de prix.
        #Il varie entre 0 et 100 et est souvent utilisé pour détecter des conditions de surachat (RSI > 70)
        #ou de survente (RSI < 30)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        perte = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / perte
        data['RSI'] = 100 - (100 / (1 + rs))

        #Bandes de Bollinger :
        #Les bandes de Bollinger sont un indicateur qui consiste en trois lignes :
        #La moyenne mobile à 50 jours (SMA_50),
        #La bande supérieure (SMA_50 + 2 fois l'écart-type sur 50 jours),
        #La bande inférieure (SMA_50 - 2 fois l'écart-type sur 50 jours)."""
        rolling_std = data['Close'].rolling(window=50).std()
        data['Upper_BB'] = data['SMA_50'] + 2 * data['Close'].rolling(window=50).std()
        data['Lower_BB'] = data['SMA_200'] - 2 * data['Close'].rolling(window=50).std()

        # Préparation des données
        data.dropna(inplace=True)

        X = data[['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'Upper_BB', 'Lower_BB']]
        y = data['Close']

        #normalisation - SUPPRIMEE POUR REDUIRE OVERFITTING, TEST SET TROP PRET DU TRAIN SET
        #scaler = StandardScaler()
        #X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns) #scaler.fit_transform(X)
        #X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, shuffle=False, random_state=42)
        # Création et entraînement du modèle
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Évaluation du modèle
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        print("Coefficient de détermination R2: ", r2)
        print('Précision sur le train set : ', round(model.score(X_train, y_train), 3))
        print('Précision sur le test set :', round(model.score(X_test, y_test), 3))

        # Fonction pour créer les caractéristiques du jour suivant
        def create_next_day_features(last_row, predictions, data):
            next_day = last_row.copy()
            next_day['Open'] = predictions[-1] if len(predictions) > 0 else next_day['Close']
            next_day['Close'] = np.nan  # À prédire
            next_day['High'] = next_day['Open']
            next_day['Low'] = next_day['Open']
            next_day['Volume'] = next_day['Volume']
            next_day['Date'] = next_day['Date'] + pd.Timedelta(days=1)

            next_day['SMA_50'] = (data['Close'].iloc[-49:].sum() + next_day['Open']) / 50
            next_day['SMA_200'] = (data['Close'].iloc[-199:].sum() + next_day['Open']) / 200
            next_day['RSI'] = next_day['RSI']

            std_50 = data['Close'].iloc[-50:].std()
            next_day['Upper_BB'] = next_day['SMA_50'] + 2 * std_50
            next_day['Lower_BB'] = next_day['SMA_50'] - 2 * std_50

            return next_day

        # Prédiction pour les X prochains jours
        future_days = 15 # variable de jours de prédiction
        future_predictions = []
        last_row = data.iloc[-1]
        future_data = data.copy()

        for i in range(future_days):
            next_day = create_next_day_features(last_row, future_predictions, future_data)
            X_next = pd.DataFrame([next_day[['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'Upper_BB', 'Lower_BB']]])
            # SUPPRESSION DE LA NORMALISATION
            #X_next_scaled = pd.DataFrame(scaler.transform(X_next), columns=X_next.columns)
            #prediction = max(0, model.predict(X_next_scaled)[0])
            prediction = max(0, model.predict(X_next)[0])

            #X_next = next_day[['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'Upper_BB', 'Lower_BB']].values.reshape(1, -1)
            #X_next_scaled = scaler.transform(X_next)
            #prediction = max(0, model.predict(X_next_scaled)[0])  # Assure une prédiction positive
            future_predictions.append(prediction)
            next_day['Close'] = prediction
            future_data = pd.concat([future_data, pd.DataFrame([next_day])], ignore_index=True)
            last_row = next_day

        # Création du DataFrame avec les prédictions
        future_dates = pd.date_range(start=data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=future_days)
        prediction_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Close': future_predictions
        })

        

                # Créer une figure Plotly
        fig = go.Figure()

        # Ajouter les données historiques
        fig.add_trace(go.Scatter(x=data['Date'][-30:], y=data['Close'][-30:],
                                mode='lines',
                                name='Données historiques'))

        # Ajouter les prédictions
        fig.add_trace(go.Scatter(x=prediction_df['Date'], y=prediction_df['Predicted_Close'],
                                mode='lines',
                                name='Prédictions',
                                line=dict(dash='dash')))

        # Mise en page du graphique
        st.markdown(f"<h3 style='text-align: center;line-height: 0.05;color: goldenrod'>Prix historique et prédictions du {crypto_search.upper()}</h3>", unsafe_allow_html=True)
        fig.update_layout(xaxis_title='Date',
                          yaxis_title='Prix (USD)',
                          legend_title='Légende',
                           hovermode='x')

        # Afficher le graphique
        st.plotly_chart(fig)

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

def plateforme():
    st.markdown("""
        <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
        <u>Coinbase</u></span><br>
        
        <h5>Points Positifs :</h5>
        <span style= "font-size : 20px";
           ▪️ Facilité d'utilisation : L'interface est conviviale et adaptée aux débutants. L'inscription et l'achat de cryptomonnaies sont simples.<br>
           ▪️ Sécurité : Coinbase propose des mesures de sécurité robustes, telles que l'authentification à deux facteurs (2FA) et une couverture d'assurance en cas de piratage.<br>
           ▪️ Régulation : Très régulé, particulièrement en Europe et aux États-Unis, ce qui inspire confiance aux utilisateurs.<br>
           ▪️ Support client : Bonne qualité du service client, avec un support disponible via chat ou email.<br>
           ▪️ Disponibilité de cryptomonnaies : Propose une sélection large et bien choisie de cryptomonnaies populaires.</span><br>
        <br>
        <h5>Points Négatifs :</h5>
        <span style= "font-size : 20px";
           ▪️ Frais élevés : Les frais de transaction et de retrait sont relativement élevés par rapport à d'autres plateformes.<br>
           ▪️ Options limitées pour les traders avancés : Coinbase est plus destiné aux débutants qu'aux traders expérimentés, avec moins d'outils avancés.<br>
           ▪️ Retraits limités : Les options de retrait de fonds peuvent être limitées et prendre plus de temps.<br>
           ▪️ Frais de conversion : Des frais supplémentaires peuvent s'appliquer pour les conversions entre certaines cryptomonnaies.</span>
        <br><br>
        <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
        <u>Binance</u></span><br>        
        
        <h5>Points Positifs :</h5>
        <span style= "font-size : 20px";
            ▪️ Frais compétitifs : Binance est connue pour ses faibles frais de transaction, qui peuvent être réduits en utilisant son token natif, le BNB.<br>
            ▪️ Large choix de cryptomonnaies : Offre un très grand nombre de cryptomonnaies à échanger, incluant des altcoins peu connus.<br>
            ▪️ Outils avancés pour traders : Très adapté aux traders expérimentés, avec des options telles que le trading de marge, des futurs, des options et des outils d’analyse.<br>
            ▪️ Liquidité élevée : Binance est l'une des plateformes les plus liquides, ce qui permet des transactions rapides et à des prix proches du marché.<br>
            ▪️ Accessibilité globale : Disponible dans de nombreux pays, avec des supports pour plusieurs devises locales.</span><br>
        <br>
        <h5>Points Négatifs :</h5> 
        <span style= "font-size : 20px";
            ▪️ Complexité pour les débutants : L'interface peut être déroutante pour les nouveaux utilisateurs en raison de la multitude d'options proposées.<br>
            ▪️ Problèmes de régulation : Binance a fait face à des problèmes de régulation dans certains pays, ce qui peut créer de l'incertitude pour les utilisateurs.<br>
            ▪️ Sécurité : Bien que sécurisée, Binance a été victime de hacks dans le passé, ce qui peut inquiéter certains utilisateurs.<br>
            ▪️ Support client limité : Le support client de Binance a souvent été critiqué pour sa lenteur et son efficacité.</span><br>
        <br>
        <span style= "font-size : 30px; font-weight: bold; color: goldenrod">
        <u>Kraken</u></span><br> 
        <h5>Points Positifs :</h5>
        <span style= "font-size : 20px";
            ▪️ Sécurité de niveau élevé : Kraken est reconnu pour ses mesures de sécurité avancées, incluant la conservation des fonds dans des portefeuilles froids et une authentification renforcée.<br>
            ▪️ Frais compétitifs : Les frais de transaction sont relativement bas par rapport à certaines autres plateformes.<br>
            ▪️ Transparence et régulation : Kraken est bien régulé et offre des informations détaillées sur ses processus de sécurité et de gestion des fonds.<br>
            ▪️ Support client : Un support client réactif et bien noté.<br>
            ▪️ Outils pour traders avancés : Kraken offre des outils avancés de trading, incluant des options de trading sur marge.</span><br>
        <br>
        <h5>Points Négatifs :</h5>
        <span style= "font-size : 20px";
            ▪️ Interface complexe pour les débutants : Kraken peut être difficile à naviguer pour ceux qui ne sont pas familiarisés avec les plateformes de trading de cryptomonnaies.<br>
            ▪️ Sélection limitée de cryptomonnaies : Moins de cryptomonnaies disponibles que sur Binance, ce qui peut être un inconvénient pour ceux qui cherchent à diversifier leurs investissements.<br>
            ▪️ Retraits et dépôts lents : Les transactions peuvent parfois prendre du temps, surtout pour les retraits.<br>
            ▪️ Frais de dépôt pour certains types de paiements : Les frais pour certains types de paiements, comme les virements bancaires internationaux, peuvent être relativement élevés.</span>""", unsafe_allow_html=True)
    
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
        <h1 style="text-align: center; color: goldenrod">La Crypto en détail</h1>
        """, unsafe_allow_html=True)
        st.text("")
        st.divider()
        
        # Appel de la fonction evolution pour afficher les valeurs les les courbes d'évolution
        evolution()
        st.text("")
        st.text("")
    
    # Si selection de la page Historique 
    elif selection == 'Plateforme': 
        st.markdown("""
        <h1 style="text-align: center; color: goldenrod; line-height: 0.1">Comparaison entre differentes plateformes</h1>
        """, unsafe_allow_html=True)
        st.divider()
        plateforme()

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
            options = ['Accueil','Details','Plateforme'])
    
# Appel de la fonction page
page()