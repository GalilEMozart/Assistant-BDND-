# Assistant Intelligent pour la BDNB

Ce projet implement un assistant capable d'interroger la Base de Données Nationale des Bâtiments (BDNB) en langage naturel

### Etape 1: Approche analytique 

Nous allons essayer de repondre aux questions en faisant de croisement et recherche dans differentes table.

Q1. 
- batiment_groupe_synthese_propriete_usage.csv: contient les type de batiment
-  

## Amelioration 
- Une aanyse complete de tout le jeu de données. 
    - Cartographier les relations entre toutes les tables 
    - Identifier les cles primiaire et etrangeres entre ces tables


- plus de proprocessing, la colonne 'contient_fictive_geom_groupe' de la table batiment_groupe indique la surface est generee ou pas, en tenir compte peut ameloirer les reponse de l'assistant.

- Pour les dates de creations qui marque (remplacer  par KNN),
- rajouter des donnees externe (immobilier, batiment). Ex: CAPA
- Tetst unitaire
- stress test
- Dockerized
- Performance test pour le preprocessing, retriever


## new features
- Real time response (streaming)
- Cache system
- feedback from user
- monitoring
- scalabilty S

## step
- 1ere etape: echnatillonner les donnees  (attention a fixer le seed pour avoir les memes echantillons)
- 2eme comprendre les donnees:
    - Approche: Repondre aux questions avec de l'analyse du dataset, constituer ainsi un jeu de test quant a la pertinance de la reponse de mon assistant. 
- 3ieme mettre en place un pipeline 
- 4ieme environnement reproducible
- 5 ieme mettre en place l'api (FastAPI), le front avec react, et dockerizer
- 6 ieme readme avec les futurs improvements 
- 7 ieme ameliorer peut etre le chatbot




Repondre aux questions
Regroupes les tables semblable
Mini chat


# 1. Analyse de donnees 

Apres avoir anlyse et avoir repondu aux questions de manieres analystique grace aux requetes, on peut conclure que pour repondre a nos questions nous avons besoin de trois table principalement:
- batiment_groupe_synthese_propriete_usage.csv
- batiment_groupe_dpe_statistique_logement.csv
- batiment_groupe.csv
- batiment_groupe_ffo_bat.csv


# Preprocessing 

Nous allons croises ces tables, afin de remplier notre Base de donnees vectorielle.



# Question

- How to spplit docs
- what chunk size to use
- what chunck overlap to use

- which embedding model to use 
- which DB to use

- what similarity to use

- How to evaluate our model
- how to improve it performance 
- semantic search vs key word search (BM25 ) 


# Architecture 

┌────────────┐
│ Utilisateur│
└────┬───────┘
     ↓
┌────────────┐
│ Interface  │  ← FastAPI
└────┬───────┘
     ↓
┌────────────┐
│ RAG Engine │
│ ┌────────┐ │
│ │Embedder│ → (Vector DB)
│ └────────┘ │
│ ┌────────┐ │
│ │Retriever│ ← Recherche dans la base vectorielle
│ └────────┘ │
│ ┌────────┐ │
│ │ LLM    │ ← Génère la réponse enrichie par les docs
│ └────────┘ │
└────────────┘



Features:
- Nombre de batiments pas ville, region, region, commune
- Le surface total,
- Le nombre de proprietaire 
- 


# version 1 

la premiere version integres les texte qui decrit un batiment avec toute les informations qui y sont associees, mais quand aux questions, le reponse n'etaient pas pertinents, puisque le contexte ne pouvais recuperer les infos necessaires


# version 2 

intergrer toutes les stats possibles, tirees depuis le dataset pour repondre efficacement aux questions.
Statistique par:
- Global (toutes la france)
- Region
- Departement
- Commune
- Batiment
- Type de batiment
- Annee de construction
- Classe dpe
- Region x batiment
- Grande ville francais (un peu redondant)


Transformation textuelle en langage naturelle (phrase)

