import pandas as pd 
import streamlit as st
from streamlit_option_menu import option_menu

def data_hist():
    df = pd.read_csv('histo_generator.csv')
    return df

def accueil():
    st.write("Bienvenue sur l'application Datanova - Crypto")
    data_hist()

def details():
    st.write("Vous êtes ici pour plus de détails")


def page():
    if selection == 'Accueil':
        accueil()
    elif selection == 'Details':
        details()


with st.sidebar:
    selection = option_menu(
            menu_title=None,
            options = ['Accueil','Details'])

page()