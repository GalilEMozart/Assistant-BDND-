# 🧠 Assistant RAG Local pour la BDNB

Ce projet est un assistant intelligent, basé sur l'architecture **RAG (Retrieval-Augmented Generation)** qui intérroge la **Base de Données Nationale des Bâtiments (BDNB)**.   
Le projet est entièrement **exécutable en local** : aucun appel à une API externe. Il utilise un **modèle de langage local** (type Mistral) et une base vectorielle **ChromaDB**.


Le choix du stack pour leurs simplicité d'utilisation, pour des questions de scalabilité et perfmance une étude doit être menée; pour le besoin de ce POC, ce stack suffit largement.

---

## 📁 Arborescence du projet

```
.
├── api/                   # Backend FastAPI
├── frontend/              # Interface web React
├── src/                   # Traitement RAG, ingestion, génération de texte
├── data/                  # Fichiers BDNB transformés
├── db/                    # dossier base de données vectorielle ChromaDB
├── models_llm/            # Modèle LLM local (ex: mistral.gguf)
├── notebook/              # Analyses exploratoires (Jupyter)
├── logs/                  # Logs d'exécution
├── docker-compose.yml     # Orchestration Docker
├── Makefile               # Commandes utiles
├── requirements.txt       # Dépendances Python
└── readme.md              # Ce fichier
```

---

## 🚀 Lancer le projet

### 1. Prérequis

- Docker & Docker Compose installés
- Python
- L'utilitaire make installé 


### 1. Intialisation

Lancer la commande `make init` pour initialiser tous les dossiers nécessaires.  
Télécharger les poids du modèle mistral.gguf (ou autre modèle compatible GGUF) et le stocker dans le dossier `models_llm`.

### 2. Data

Les données sont à télécharger [ici](https://www.data.gouv.fr/fr/datasets/r/ad4bb2f6-0f40-46d2-a636-8d2604532f74) ou bien avec la commande `make data`.  
Un échantillon est tiré, avec lequel on travaillera. Il faut donc lancer la commande `make sample` pour effectuer l'échantillonage.

Le poids du modèle à téléchager ici, et le placer dans le dossier models_llm.

---

### 2. Lancer l'app (API + Frontend)

```bash
make up
```

- Backend FastAPI : http://localhost:8000
- Frontend React : http://localhost:3000

---

## 🔧 Commandes utiles

```bash
make init            # Initialise tous les dossiers essentiels
make env             # Active l'environnement virtuel et install les dépendences nécessaires
make data            # Téléchager les données brutes
make sample          # Echantillon les données 
make etl             # Lance le pipeline etl, qui charge, transforme les données (features), et les stockes
make up              # Lance docker-compose
make ingest          # Lance l'ingestion RAG (vectorisation des documents)
```

---

## Notebook

Ces notebook contient les codes qui servies du featuring engineering et la reponse aux questions de manières analytiquet en intégeant les base de données avec les requêtes.

Vous trouverez 3 notebooks:
- 1. echantillonage.ipynb: echantillons les données à partir du jeu de données brut
- 2. reponse_aux_questions.ipynb: contient les reponses anlytiques aux questions
- 3. preprocessing.ipynb: contient les preprocessing des données. Expliquer les approches, choix, amélioration possible. Permets de visualiser les resultats intermédaires obtenues et les résultats des tables finales.


## 🧩 Composants

### 🧠 Backend (FastAPI)

- Chargement des embeddings
- Interrogation de ChromaDB
- Génération de réponses avec modèle local (via `llama-cpp-python`)

📁 Fichiers :
- `api/main.py` : point d’entrée de l’API
- `src/rag.py` : logique RAG
- `src/ingest_data.py` : ingestion + embeddings
- `src/etl.py` : pipeline elt
- `src/config.py` : contient toutes les configurations nécessaires
- `src/logger.py` : le logger
- `src/compute_stat.py` et `src/compute_text_batiment.py` : effectue le preprocessing
- `src/compute_stat.py` : sample le jeu de données

---

### 💻 Frontend (React)

Interface minimaliste de type chat pour interroger l’assistant.

📁 Localisation : `frontend/`

![](./images/Screenshot%20from%202025-04-22%2015-50-37.png)

---

## 📦 Technologies utilisées

| Domaine          | Techno                      |
|------------------|-----------------------------|
| Backend API      | FastAPI                     |
| Embedding & RAG  | ChromaDB + modèles HF       |
| LLM Local        | Mistral (GGUF)              |
| Vectorisation    | SentenceTransformers (fr)   |
| Frontend         | React + Nginx               |
| Conteneurisation | Docker + Docker Compose     |

---

## 📝 TODO / Roadmap

- [ ] Recherche hybride (mots-clés + sémantique)
- [ ] Authentification utilisateur
- [ ] Téléversement de fichiers
- [ ] Génération de synthèses automatiques (par commune / DPE)
- [ ] Fine-tuning du model 
- [ ] Features engineering 
- [ ] Données externe pour enrichier les modèles (pour le fine-tuning)
- [ ] Evaluation riguoreuse du système 
- [ ] CI/CD (test unitaite/intégration)
- [ ] Architecture avancées de RAG
- [ ] Documentation complet de code
- [ ] Fichier sample.py a completer
- [ ] Tester tous les differents scritps

---

## 📚 Données utilisées

- **Base de Données Nationale des Bâtiments (BDNB)**: Télécharger les données [ici](https://www.data.gouv.fr/fr/datasets/r/ad4bb2f6-0f40-46d2-a636-8d2604532f74)

Un échantillon de données est utilise pour ce projet (faute de ressources).

## Reponse aux questions
1. 

---

## 🤝 Contributions

Les contributions sont les bienvenues ! N’hésitez pas à ouvrir une **issue** ou une **pull request**.
