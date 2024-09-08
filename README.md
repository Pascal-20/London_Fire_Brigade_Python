# Prediction du Temps de Reponse de la Brigade des Pompiers de Londres

## Introduction
Comme dans toutes les villes du monde, des accidents de tout type peuvent arriver et la ville de Londres n'en fait pas exception. A cet effet, elle dispose d'une Brigade des Pompiers qui assure les interventions contre les sinistres dans toute la ville. Ce projet que j'ai mené avec deux autres membres de ma classe de formation (Eva et Nathalie) porte donc sur cette brigade. Les données mises à notre disposition sont disponbiles [ici](https://data.london.gov.uk/).

L'objectif de ce projet est d'analyser et estimer les temps de réponse et de mobilisation de la Brigade des Pompiers de Londres suite à un incident. Au cours de ce travail, nous explorerons les différents outils d'analyse de données avec Python et ses librairies. Nous allons d'abord préparer les données de sorte à les rendre exploitable. Ensuite, nous visualiserons ces données à travers des graphiques et enfin, nous entrainerons des modèles de Machine Learning pour estimer le temps de reponse et de mobilisation de la Brigade.

## Action menées 
Pour atteindre les objectifs de ce projet, les actions suivantes ont été entreprises : 

- Telechargement des données depuis le site de la Brigade de 2016 à 2023.
- Nettoyage et prétraitement de l'ensemble de données à l'aide de bibliothèques Python telles que Pandas pour garantir la qualité et la cohérence des données.
- Analyse géographique, temporelle, du type d'incidents, des retards à partir de la visualisation des données créées avec Matplotlib, Seaborn et Power Bi. Cela nous donnera plus de détails sur les causes de retards, les zones ayant le plus de retard, les périodes temporelles où il y a le plus d'accidents et enfin les zones ayant le plus de sinistres.
- Modélisation des données avec pour variable cible **TravelTimeSeconds**. Compte tenu du volume de données avec lequel nous travaillons, nous avons selectionné quelques variables numériques et categorielles.

#### Résultats

Les statistiques de notre variable cible sont les suivantes :

<p align="center">
  <img width="400" " src="https://github.com/user-attachments/assets/a3e51ffb-44eb-48b6-9563-d759bb9f9613">
</p>

Nous avons commencé par entrainer des modèles de Regression mais malgré nos efforts pour utiliser plusieurs modèles de régression différents (Linear Regression, Gradient Boosting Regressor)mais, nous n'avons pas obtenu des résultats satisfaisants comme prévu.

Le modèle Gradient Boosting Regressor, un peu meilleur que le modèle Linear Regression, nous donne les scores suivants : 
+ **Train R2 Score: 0.3728651228332751**
+ **Test R2 Score: 0.37399282160333824**

Nous avons donc opté pour un modèle de classification qui nous donne des résultats bien plus satisfaisants. Il a fallu d'abord réduire nos données et c'est ce que nous avons fait compte tenu du fait que nous avons une grande quantité de données.

La solution trouvée a été de créer des dictionnaires permettant de regrouper les valeurs uniques de nos variables catégorielles, en quelques valeurs seulement. Nous obtenons donc les valeurs uniques suivantes : 

<p align="center">
  <img width="400" " src="https://github.com/user-attachments/assets/7ee67807-2803-49d6-ab25-7b35e9e75a90">
</p>

Notre modèle **RandomForestRegressor** a été défini par classes grâce aux quartiles, telles que : 

- **Classe 0 : valeurs inférieures à q1**
- **Classe 1 : valeurs entre q1 et q2**
- **Classe 2 : valeurs entre q2 et q3**
- **Classe 3 : valeurs supérieures à q3**

Nous l'avons defini par classe pour avoir des estimations fiables ce qui nous semble plus pertinent au vu du nombre de quartiers dans lesquels interviennent les Pompiers mais aussi au vu des données.

Notre modèle obtient le score suivant :

**Précision du modèle :  0.761052235876854**

<p align="center">
  <img width="400" " src="https://github.com/user-attachments/assets/55d01c2c-71a3-4a75-b7d8-a232e9e324dd">
</p>

## Conclusion
Nous pouvons conclure que l'objectif global du projet a été atteint. Après une analyse approfondie des données, nous avons développé un modèle de Machine Learning performant avec un score de précision de 75 %. Ce modèle se rapproche bien de la réalité, même s'il reste une marge d'amélioration de 25 %. 
Malgré l'impact de certaines variables externes sur nos données, nous pensons que notre modèle pourrait être amélioré en disposant d'informations plus précises sur les éléments suivants :
**La configuration urbaine et le trafic routier (c'est-à-dire la facilité ou les obstacles pour accéder au lieu de l'incident) ainsi que la répartition démographique.**

## Limites
Nos principales limites résident dans notre modèle de Machine Learning, le RandomForestRegressor.

En analysant les scores de chaque classe, on observe des variations. Par exemple, la classe 3 affiche les meilleurs résultats avec une précision de 0,81, un rappel de 0,84 et un F1-score de 0,82, montrant une forte performance du modèle pour cette classe. À l'inverse, la classe 2 a des résultats moins satisfaisants avec une précision de 0,75, un rappel de 0,66 et un F1-score de 0,70.

En somme, bien que le modèle présente de bonnes performances globales, des améliorations sont possibles, notamment pour certaines classes où la précision ou le rappel sont plus faibles.

## Perspectives et solutions

Ce projet a montré un grand potentiel et pourrait servir à développer des applications futures destinées à deux types d'utilisateurs : **les pompiers** et **le grand public**. L'objectif principal serait de faciliter la transmission d'informations entre le moment où un incident est signalé et l'arrivée des pompiers sur les lieux.

L'application pourrait proposer plusieurs fonctionnalités :

- **Suivi en temps réel** : Permettre aux utilisateurs de suivre l'état de leur signalement en temps réel, avec des mises à jour sur l'heure estimée d'arrivée des pompiers.
  
- **Navigation avancée** : Offrir des fonctionnalités de navigation avancée pour aider les utilisateurs à indiquer avec précision l'emplacement de l'incident, optimisant ainsi l'itinéraire des pompiers pour une intervention rapide.

- **Conseils** : Fournir des conseils pratiques et des instructions sur la conduite à tenir en attendant l'arrivée des secours, tels que des fiches éducatives sur les gestes de premiers secours.


