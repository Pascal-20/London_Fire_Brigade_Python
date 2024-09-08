# Prediction du Temps de Reponse de la Brigade des Pompiers de Londres

## Introduction
Comme dans toutes les villes du monde, des accidents de tout types peuvent arriver et la ville de Londres n'en fait pas exception. A cet effet, elle dispose d'une Brigade des Pompiers qui assure les interventions contre les sinistres dans toute la ville. Ce projet que j'ai mené avec deux autres membres de ma classe de formation (Eva et Nathalie) porte donc sur cette brigade. Les données mis à notre disposition sont disponbile [ici](https://data.london.gov.uk/).

L'objectif de ce projet est d'analyser et estimer les temps de réponse et de mobilisation de la Brigade des Pompiers de Londres suite à un incident. Au cours de ce travail, nous explorerons les differents outils d'analyse de données avec Python et ses librairies. Nous allons d'abord preparer les données de sorte à les rendre exploitable ensuite nous visualiserons ces données à travers des graphiques et enfin, nous entrainerons des modeles de Machine Learning pour estimer le temps de reponse et de mobilisation de la Brigade.

## Action menées 
Pour atteindre les objectifs de ce projet, les actions suivantes ont été entreprises : 

- Telechargement des données depuis le site de la Brigade de 2016 à 2023.
- Nettoyage et prétraitement de l'ensemble de données à l'aide de bibliothèques Python telles que Pandas pour garantir la qualité et la cohérence des données.
- Analyse géographique, temporelle, du type d'incidents, des retards à partir de la visualisation des données créées avec Matplotlib, Seaborn et Power Bi. Cela nous donnera plus de détails sur les causes de retards, les zones ayant le plus de retard, les periodes temporelles où il y a le plus d'accidents et enfin les zones ayant le plus de sinistre.
- Modelisation des données avec pour variable cible **TravelTimeSeconds**. Compte tenu du volume de données avec lequel nous travaillons, nous avons selectionné quelques variables numériques et categorielles.

#### Résultats

Les statistiques de notre variable cible sont les suivantes :

<p align="center">
  <img width="400" " src="https://github.com/user-attachments/assets/a3e51ffb-44eb-48b6-9563-d759bb9f9613">
</p>

Nous avons commencé par entrainer des modèles de Regression mais malgré nos efforts pour utiliser plusieurs modèles de régression différents (Linear Regression, Gradient Boosting Regressor), nous n'avons pas obtenu des résultats aussi satisfaisants que prévu.

Le modèle Gradient Boosting Regressor, un peu meilleur que le modèle Linear Regression, nous donne les scores suivants : 
+ **Train R2 Score: 0.3728651228332751**
+ **Test R2 Score: 0.37399282160333824**

Nous avons donc opté pour un modèle de classification qui nous donne des resultats bien plus satisfaisant. Il a fallut d'abord reduire nos données et c'est ce que nous avons fait compte tenu du fait que nous avons une grande quantité de données.

La solution trouvée a été de créer des dictionnaires permettant de regrouper les valeurs uniques de nos variables catégorielles, en quelques valeurs seulement. Nous obtenons donc les valeurs uniques suivantes : 

<p align="center">
  <img width="400" " src="https://github.com/user-attachments/assets/7ee67807-2803-49d6-ab25-7b35e9e75a90">
</p>

Notre modèle **RandomForestRegressor** a été defini par classes grâce aux quartiles, telles que : 

- **Classe 0 : valeurs inférieures à q1**
- **Classe 1 : valeurs entre q1 et q2**
- **Classe 2 : valeurs entre q2 et q3**
- **Classe 3 : valeurs supérieures à q3**

Nous l'avons defini par classe pour avoir des estimations fiable ce qui nous semble plus pertinent au vu du nombre de quartier dans lesquels interviennent les Pompiers mais aussi au vu des données.

Notre modèle obtient le score suivant :

**Précision du modèle :  0.761052235876854**

<p align="center">
  <img width="400" " src="https://github.com/user-attachments/assets/55d01c2c-71a3-4a75-b7d8-a232e9e324dd">
</p>
