#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd 
import numpy as np 
import streamlit as st 
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA


import streamlit as st
import pandas as pd


@st.cache_data()
def get_data():
    return pd.read_csv(
        "Dataframe_distance.csv",
         nrows=100000)

df = get_data()

st.cache(persist=True)

logo = 'pompier3.jpg'

st.sidebar.image(logo, use_column_width=True)
st.sidebar.write("Prediction du temps de réponse de la LFB:")
section = st.sidebar.selectbox(
    "Navigation",
    ("Sommaire", "Jeux de données", "Visualisation", "Machine Learning", "Résultats", "Conclusion"))

# st.write("You selected:", section)

pages = ["Introduction", "Jeux de données", "Visualisation",
         "Machine Learning", "Résultats", "Conclusion"]

page = st.sidebar.radio("Aller vers la page :", pages)


if page == pages[0]:

    st.write("## Introduction")

    st.write("### La Brigade de pompiers de Londres ou LFB : ")
    st.markdown("* Environ 5 000 pompiers professionnels et 500 volontaires")
    st.markdown("* 150 véhicules d'intervention")
    st.markdown("* Siège social : Southwark")
    st.markdown("* Casernes : réparties dans toute la ville de Londres")
    st.markdown("* Interventions : incendies, operations de sauvetages")

    st.image("pompier2.jpeg")

    st.write("### Objectif : ")
    st.markdown("* Analyser les performances opérationnelles de la brigade en termes de temps de réponse et de mobilisation lors d'incidents")
    st.markdown("* Modeliser le temps de reponse")
    st.markdown(
        "* Proposer des solutions pour ameliorer les performances de la brigade")

    st.write("### Methode de travail : ")
    st.markdown("* Analyse de données avec Pandas")
    st.markdown("* Visualisation des données avec Matplotlib et Seaborn")
    st.markdown(
        "* Modelisation du temps de reponse par Machine Learning avec Scikit Learn")

elif page == pages[1]:
    st.write("## Exploration des données")

    st.dataframe(df.head())
    st.write("### Volumétrie :")
    st.write(
        "- Deux jeux de données : Incidents à Londres et Mobilisation des Pompiers.")
    st.write("- Mises à jour mensuelles depuis janvier 2009.")
    st.write("- **Incidents** : 515,08 Mo. **Mobilisation** : 525,62 Mo.")
    st.write("- Volume total : 1,02 Go.")

    st.write("### Valeurs nulles :")
    st.write("#### Avant traitement:")
    st.write("* 11% de valeurs nulles ")
    st.write("* Suppression des données < 2016 ")
    st.write("* 14 236 302 valeurs manquantes sur 127 300 480  ")
    st.write("* Suppression des colonnes lorsque les valeurs nulles > 60%")
    st.write("* Suppression des lignes lorsque les valeurs nulles < 10%")
    st.write("* Ajouts de nouvelles variables")
    st.write(
        "* Remplacement des valeurs manquantes selon différentes stratégies par 0 ou No")
    st.write("#### Après traitement:")
    st.write("* Fusion des deux Dataframes en un seul")
    st.write("* 38 variables & 0% de valeurs nulles")

elif page == pages[2]:
    st.write("### Machine Learning :")

    @st.cache_data()
    def get_data():
        return pd.read_csv(
            "df_preprocessed.csv",
             nrows=1900000)
    
 
    model = joblib.load("classification_pompier_line")

 
    df = get_data() 
    
        # Créer des selectbox pour les colonnes spécifiques
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        year = st.selectbox('Année', df['Year'].unique())
    
    with col2:
        month = st.selectbox('Mois', df['Month'].unique())
    
    with col3:
        weekday = st.selectbox('Jour', df['Weekday'].unique())
    
    with col4:
        incident_station = st.selectbox('Station', df['IncidentStationGround'].unique())
    
    with col5:
        incident_group = st.selectbox('Type \'incident', df['IncidentGroup'].unique())
     
    # Filtrer les données en fonction des sélections
    filtered_df = df[(df['Year'] == year) & 
                     (df['Month'] == month) & 
                     (df['Weekday'] == weekday) & 
                     (df['IncidentStationGround'] == incident_station) & 
                     (df['IncidentGroup'] == incident_group)]
    
if st.button('Valider'):
    
    
    # Afficher le temps de réponse
    if not filtered_df.empty:
        st.write("Temps de réponse :", filtered_df['TravelTimeSeconds'].mean())
    else:
        st.write("Aucune donnée disponible pour ces sélections.")
