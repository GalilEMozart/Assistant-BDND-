VENV_DIR=my_env
PYTHON=$(VENV_DIR)/bin/python
DATA_URL=https://www.data.gouv.fr/fr/datasets/r/ad4bb2f6-0f40-46d2-a636-8d2604532f74 
DATA_OUTPUT=./data/brutes
DATA_OUTPUT_ZIP=./data/zip 

init:
	@echo " Initialisation du projet"
	@# Crée les dossiers nécessaires
	mkdir -p models_llm
	mkdir -p data/etl_input data/etl_output
	mkdir -p db
	mkdir -p logs
	mkdir -p $(DATA_OUTPUT)
	mkdir -p $(DATA_OUTPUT_ZIP)

env:
	@# Crée l’environnement virtuel si besoin
	if [ ! -d $(VENV_DIR) ]; then \
		echo " Création de l'environnement virtuel..."; \
		python3 -m venv $(VENV_DIR); \
		$(PYTHON) -m pip install --upgrade pip; \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "Environnement virtuel déjà créé."; \
	fi

data:
	@# Télécharge les données brutes si elles n'existent pas
	if [ ! -f $(DATA_OUTPUT) ]; then \
		echo "⬇️ Téléchargement des données brutes..."; \
		wget -O $(DATA_OUTPUT_ZIP)/donnees_brutes.tar.gz $(DATA_URL); \
		tar -xvzf $(DATA_OUTPUT_ZIP)/donnees_brutes.tar.gz -C $(DATA_OUTPUT); \
	else \
		echo " Données brutes déjà présentes."; \
	fi

etl:
	$(PYTHON) src/ingest_data.py

ingest: init env 
	$(PYTHON) src/ingest_data.py

up: 
	docker compose up --build -d

down:
	docker compose down
