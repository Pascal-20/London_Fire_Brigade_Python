#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd 

import streamlit as st 



st.set_page_config(
    page_title="Temps de réponse de la LFB",
    page_icon=":fire:",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data()
def get_data_inc():
    return pd.read_csv(
        'Incidents.csv',
         nrows=10)
def get_data_mob():
    return pd.read_csv(
        'Mobilisations.csv',
         nrows=10)
def get_data_dist():
    return pd.read_csv(
        'Dataframe_distance.csv',
         nrows=10)
def get_data_preprocessed():
    return pd.read_csv(
        "df_preprocessed.csv",
        nrows=10000000)


df_inc = get_data_inc()
df_mob = get_data_mob()
df_dist = get_data_dist()
colonnes_a_supprimer = ["HourOfCall_x", "StopCodeDescription", "ProperCase", 'IncGeo_WardName', 'FRS', 'NumCalls', 'CalYear_y', 'HourOfCall_y', 'ResourceMobilisationId', 'Resource_Code', 'PerformanceReporting', 'DateAndTimeLeft', 'DeployedFromStation_Code', 'PumpOrder', 'PlusCode_Code', 'PlusCode_Description', "DateAndTimeMobilised",]
df_dist = df_dist.drop(columns=colonnes_a_supprimer)
df_preprocessed = get_data_preprocessed() 


st.cache(persist=True)
import base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
      background-image: url("data:image/png;base64,%s");
      background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("background.png")

logo = 'pompier3.jpg'

st.sidebar.image(logo, use_column_width=True)
st.sidebar.write("Prediction du temps de réponse de la LFB:")

# st.write("You selected:", section)

pages = ["Introduction", "Jeux de données",
         "Machine Learning", "A vous de jouer !", "Conclusion"]

page = st.sidebar.radio("Aller vers la page :", pages)


if page == pages[0]:

    st.title("Introduction")

    st.write("### La Brigade de pompiers de Londres (LFB) : ")
    st.markdown("###### - Environ 5 000 pompiers professionnels et 500 volontaires")
    st.markdown("###### - 150 véhicules d'intervention")
    st.markdown("###### - Siège social : Southwark")
    st.markdown("###### - Casernes : réparties dans toute la ville de Londres")
    st.markdown("###### - Interventions : incendies, operations de sauvetages")
    
    st.write("")
    st.write("### Objectif : ")
    st.markdown("###### - Analyser les performances opérationnelles de la brigade en termes de temps de réponse et de mobilisation lors d'incidents")
    st.markdown("###### - Modéliser le temps de réponse")
    st.markdown(
        "###### - Proposer des solutions pour améliorer les performances de la brigade")
    
    st.write("")
    st.write("### Méthode de travail : ")
    st.markdown("###### - Analyse de données avec Pandas")
    st.markdown("###### - Visualisation des données avec Matplotlib et Seaborn")
    st.markdown(
        "###### - Modélisation du temps de reponse par Machine Learning avec Scikit Learn")

elif page == pages[1]:
    
    st.title("Exploration des données")
    
    tab1, tab2, tab3 = st.tabs(["Volumétrie", "Gestion des données", "Dataframe Final"])
    
    tab1.write("#### Source")
    tab1.write("###### http://data.london.gov.uk - Portail de partage de données gratuit et ouvert permettant d’accéder à l’ensemble des données relatives à Londres. ")
    
    tab1.write("") 
    tab1.write("#### Deux jeux de données :")
    tab1.write("###### 1. Incidents.csv : Informations détaillées sur chaque incident déclaré depuis 2009.")
    tab1.write("###### 2. Mobilisations.csv : Informations détaillées sur la mobilisation des ressources en réponse à ces incidents.")
    tab1.write("###### Mises à jour mensuelles depuis janvier 2009.") 
    
    tab1.write("")
    tab1.write("##### Incidents.csv : 39 variables (1636512, 39) - 515,08 Mo.")
    tab1.dataframe(df_inc, width = 1000, height = 260)
    
    tab1.write("")
    tab1.write("##### Mobilisation.csv : 21 variables (2885296, 22) - 525,62 Mo.")
    tab1.dataframe(df_mob, width = 1000, height = 250)
    
    tab1.write("")
    tab1.write("##### Volume total : 1,02 Go.")

    tab2.write("#### Gestion des valeurs manquantes")
    tab2.write("###### - 11% de valeurs manquantes")
    tab2.write("###### - 14 236 302 valeurs manquantes sur 127 300 480  ")
    tab2.write("###### - Suppression des données antérieures à 2016 ")
    tab2.write("###### - Suppression des colonnes non pertinentes ou qui contenaient > 60% de valeurs manquantes")
    tab2.write("###### - Suppression des lignes contenant des valeurs manquantes lorsque la colonne contenait < 10% de valeurs manquantes")
    tab2.write("###### - Remplacement des valeurs manquantes quand nécessaire, selon différentes stratégies")
    
    tab2.write("")
    tab2.write("#### Ajout de nouvelles variables")
    tab2.write("###### - Latitude_Incident : les coordonnées GPS correspondant à la latitude du lieu de l’incident.")
    tab2.write("###### - Longitude_Incident : les coordonnées GPS correspondant à la longitude du lieu de l’incident.")
    tab2.write("###### - Distance : le calcul de la distance, en km, entre le lieu de l’incident et la station associée à l’incident, c’est à dire le lieu de déploiement des pompiers")
             
    
    tab3.write("###### - Concaténation en un seul fichier csv, grâce à la variable “IncidentNumber”, qui nous servira d’index.")
    tab3.write("###### - 38 variables au final et 0% de valeurs manquantes")
    tab3.dataframe(df_dist, width = 1000)
    

  
elif page == pages[2]:
    st.title("Machine Learning")
    
    tab4, tab5, tab6 = st.tabs(["Gestion des données", "Dataframe final pour la modélisation", "Performance du modèle"])
    
    tab4.write("#### Ajout et suppression de variables :")
    tab4.write("###### - Ajout : Year, Month, Day, Weekday (année, mois, jour et nom du jour de la semaine, découlant de la colonne “DateOfCall”).")
    tab4.write("###### - Suppression des colonnes non pertinentes pour l'entrainement de notre modèle")
    tab4.write("###### - Suppression lignes où TravelTimeSeconds = 0")
    
    tab4.write("#### Variables retenues :")
    tab4.write("###### - Variable cible : TravelTimeSeconds")
    tab4.write("###### - Variables numériques retenues : Year, Day, Distance, TurnoutTimeSeconds")
    tab4.write("###### - Variables catégorielles retenues : Month, Weekday, IncidentGroup, SpecialServiceType, PropertyCategory, AdressQualifier, IncGeoBoroughName, ")
    tab4.write("###### IncidentStationGround, FirstPumpArriving_DeployedFromStation, DelayCode_Description")
    
    tab4.write("")
    tab4.write("#### Création de dictionnaires :")
    tab4.write("###### - Création de dictionnaires permettant de regrouper les valeurs uniques de nos variables catégorielles en quelques valeurs seulement")
    tab4.write("###### - Nous obtenons les valeurs uniques suivantes :")
    
    col1, col2 = tab4.columns([0.65, 0.35])
    col1.image("dictionnaires.png")
    tab4.write("")
    tab4.write("###### Pour information, voici la manière dont les zones géographiques ont été découpées :")
    tab4.image("carte londres.png")
    
    tab5.write("#### Statistiques de la variable cible :")
    tab5.write("###### - Valeur minimale de TravelTimeSeconds : 1.0")
    tab5.write("###### - Valeur maximale de TravelTimeSeconds : 1195.0")
    tab5.write("###### - Moyenne de TravelTimeSeconds : 281.14")
    tab5.write("###### - Premier quartile (Q1) : 183.0")
    tab5.write("###### - Deuxième quartile (médiane, Q2) : 256.0")
    tab5.write("###### - Troisième quartile (Q3) : 348.0")
    
    tab5.write("")
    tab5.write("#### Classe pour l'entrainement du modèle :")
    tab5.write("###### - Classe 0 : valeurs inférieures à q1 ")
    tab5.write("###### - Classe 1 : valeurs entre q1 et q2 ")
    tab5.write("###### - Classe 2 : valeurs entre q2 et q3 ")
    tab5.write("###### - Classe 3 : valeurs supérieures à q3 ")
    
    tab5.write("")
    tab5.write("#### Dataframe final pour la modélisation :")
    maxMessageSize = 600
    tab5.dataframe(df_preprocessed.head(10), width = 1000)
    
    tab6.write("## Précision du modèle : 0.761052235876854")
    
    tab6.write("")
    tab6.write("#### Matrice de corrélation :")
    tab6.image("Matrice de corrélation.png")
    
    tab6.write("")
    tab6.write("#### Rapport de classification :")
    tab6.image("Rapport de classification.png")
    

elif page == pages[3]:
    st.title("A vous de jouer !")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    # Utiliser les widgets Streamlit pour les sélections
    year = col1.selectbox('Année', df_preprocessed['Year'].unique())
    month = col2.selectbox('Mois', df_preprocessed['Month'].unique())
    day = col3.selectbox('Jour', df_preprocessed['DayOfMonth'].unique())
    incident_group = col1.selectbox('Type d\'incident', df_preprocessed['IncidentGroup'].unique())
    property_category = col2.selectbox('Type de propriété', df_preprocessed['PropertyCategory'].unique())
    incident_station = col3.selectbox('Localisation', df_preprocessed['IncidentStationGround'].unique())
    
    
    # Bouton "Valider" pour filtrer les données
    if st.button('Valider'):
        # Filtrer les données en fonction des sélections
        filtered_df_preprocessed = df_preprocessed[(df_preprocessed['Year'] == year) & 
                                                   (df_preprocessed['Month'] == month) & 
                                                   (df_preprocessed['DayOfMonth'] == day) &
                                                   (df_preprocessed['IncidentGroup'] == incident_group) &
                                                   (df_preprocessed['PropertyCategory'] == property_category) &
                                                   (df_preprocessed['IncidentStationGround'] == incident_station)]
        

        # Afficher les données filtrées
        if not filtered_df_preprocessed.empty:
            # Définir les valeurs
            min_value = 1
            max_value = 1000
            mean_value = 277.4228605577073
            Q1 = 180.0
            Q2 = 254.0
            Q3 = 346.0
             
            # Calculer la valeur moyenne du temps de voyage filtré
            filtered_mean_time = filtered_df_preprocessed['TravelTimeSeconds'].mean()
             
            if filtered_mean_time < Q1:
                classe = 0
            elif Q1 <= filtered_mean_time < Q2:
                classe = 1
            elif Q2 <= filtered_mean_time < Q3:
                classe = 2
            else:
                classe = 3
            
            st.write("")
            st.write("##    Prédiction du modèle : Classe", classe)
            st.image("classe.png")
            st.write("")
            st.write("## Temps de réponse moyen (secondes) :", filtered_df_preprocessed['TravelTimeSeconds'].mean())
            st.write("## Temps de réponse moyen (minutes) :", filtered_df_preprocessed['TravelTimeSeconds'].mean() / 60)
            st.write("")
            st.write("")
            
           
            # Afficher le graphique avec les quartiles et les labels
            st.markdown(f"""
                <div style="position: relative;">
                    <div style="width: 1000px; height: 40px; border: 1px solid black; border-radius: 5px; position: relative;">
                        <div style="height: 100%; width: {(filtered_mean_time - min_value) / (max_value - min_value) * 100}%; background-color: #007bff; border-radius: 5px;"></div>
                        <div style="position: absolute; top: 50%; transform: translateY(-50%); width: 100%; display: flex; justify-content: space-between;">
                            <div style="position: absolute; left: 0; font-weight: bold; top: 20px;">Min</div>
                            <div style="position: absolute; left: {((Q1 - min_value) / (max_value - min_value)) * 100}%; font-weight: bold; top: 20px; ">Q1</div>
                            <div style="position: absolute; left: {((Q2 - min_value) / (max_value - min_value)) * 100}%; font-weight: bold; top: 20px; ">Q2</div>
                            <div style="position: absolute; left: {((Q3 - min_value) / (max_value - min_value)) * 100}%; font-weight: bold; top: 20px; ">Q3</div>
                            <div style="position: absolute; right: 0; font-weight: bold; top: 20px; ">Max</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("Aucune donnée disponible pour ces sélections.")
    


elif page == pages[4]:
    st.title("Conclusion générale")
    tab1, tab2, tab3 = st.tabs(["Conclusion", "Limites et difficultés", "Ouverture"])
    tab1.write("#### Conclusion")
    tab1.write("###### L’objectif de ce projet était d’analyser et d'estimer les temps de réponse et de mobilisation de la Brigade des Pompiers de Londres suite à un incident.")
    tab1.write("###### Pour cela, nous avions à disposition deux principaux jeux de données provenant du site data.london.gov.uk et référençant l’ensemble des incidents et des ") 
    tab1.write("###### mobilisations de 2009 à 2023.")
    tab1.write("")
    tab1.write("")
    tab1.write("")
    tab1.write("###### Nous sommes en mesure aujourd’hui de conclure que l’objectif global du projet à été atteint. En effet, après une analyse poussée de nos jeux de donnée, ") 
    tab1.write("###### nous avons réussi à créer un modèle de Machine Learning performant, affichant un score de précision de 75%. Comme il a été démontré, ce modèle se rapproche ")
    tab1.write("###### considérablement de la réalité, bien qu'il reste une marge d'amélioration de 25%.")
    tab1.write("")
    tab1.write("")
    tab1.write("")
    tab1.write("###### Malgré l'influence de certaines variables externes sur nos données, nous sommes d'avis que notre modèle pourrait bénéficier d'améliorations grâce à des ")
    tab1.write("###### informations plus précises sur :")
    tab1.write("###### - La configuration urbaine et le trafic routier (la facilité d'accès ou l'obstacle rencontré pour atteindre le lieu de l'incident)")
    tab1.write("###### - La répartition démographique")

    tab2.write("#### Limites")
    tab2.write("###### Nos principales limites se trouvent dans notre modèle de Machine Learning (RandomForestRegressor).")
    tab2.write("###### En effet, en examinant les scores pour chaque classe individuelle, nous pouvons voir des variations. Par exemple, la classe 3 obtient les meilleurs résultats")
    tab2.write("###### avec une précision de 0,81, un rappel de  0,84 et un F1-score de 0,82, indiquant que le modèle est particulièrement performant dans la classification de cette classe.")
    tab2.write("###### Dans l’autre sens, la classe 2 obtient des résultats moins performants, avec une précision de 0,75, mais un rappel de seulement 0,66 et un F1-score de 0,70.")
    tab2.write("###### En conclusion, bien que ce modèle de classification ait des performances globalement bonnes, il y a toujours des domaines où des améliorations pourraient être")
    tab2.write("###### apportées, en particulier pour certaines classes où la précision ou le rappel sont légèrement inférieurs.")

    tab2.write("")
    tab2.write("#### Difficultés")
    tab2.write("###### Nous avons rencontré certaines **difficultés** lors de la phase de **Machine Learning**.")
    tab2.write("###### En effet, les ordinateurs de **Pascal** et **Nathalie** n’étaient pas suffisamment puissants pour exécuter les codes, qui ont donc été entièrement développé par")
    tab2.write("###### **Eva** pour cette partie.")
    
    
    tab3.write("#### Création d'application")
    tab3.write("###### Ce projet s'est avéré très intéressant et pourrait être utilisé à l'avenir pour la conception d'applications destinées à deux publics distincts : ")
    tab3.write("###### les pompiers d'un côté, et les utilisateurs de l'autre.")
    tab3.write("###### L'objectif serait de faciliter la transmission d'informations entre le moment du signalement de l'incident et l'arrivée des pompiers sur les lieux.")
    tab3.write("")
    
    col1, col2, col3 = tab3.columns(3)
    
    col1.image("notif.webp")
    col2.write("")
    col2.write("")
    col2.write("")
    col2.write("")
    col2.write("")
    col2.write("###### Cette application pourrait contenir les fonctionnalités suivantes :")
    col2.write("")
    col2.write("")
    col2.write("###### Suivi en temps réel :")
    col2.write("L'application pourrait permettre aux utilisateurs de suivre en temps réel le statut de leur signalement, y compris des mises à jour sur l'heure estimée d'arrivée des pompiers.")
    col2.write("")
    col2.write("")
    col2.write("###### Navigation avancée :") 
    col2.write("L’application pourrait intégrer des fonctionnalités de navigation avancées pour aider les utilisateurs à fournir des indications précises sur l'emplacement de l'incident. Cela permettrait aux équipes de pompiers de se rendre rapidement sur les lieux en choisissant l'itinéraire le plus adapté.")
    col2.write("")
    col2.write("")
    col2.write("###### Conseils :") 
    col2.write("L’application pourrait fournir des conseils et des instructions utiles aux utilisateurs sur la manière de réagir en attendant l'arrivée des secours (par exemple : fiche éducative sur les gestes de 1er secours).")