import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from logger import logger as log
import src.config as config

from src.compute_stat import (
    stats_commune, 
    stats_departement,
    stats_usage,
    stats_dpe,
    stats_niveau_bt
)
from src.compute_text_batiment import (
    preprocesse_batiment_groupe_synthese_propriete_usage,
    prepocess_batiment_groupe_dpe_statistique_logement,
    prepocess_batiment_batiment_groupe,
    prepocess_batiment_groupe_ffo_bat,
    generer_description_batiment
)



# etl pipeline

def etl_pipeline(root :str, output:str) -> None:
    """etl pipteline """

    log.info(f"Démarrage du pipeline ETL. src: {root} -> dst: {output}")

    # load
    batiment_groupe_synthese_propriete_usage_path = 'batiment_groupe_synthese_propriete_usage.csv'
    batiment_groupe_dpe_statistique_logement_path = 'batiment_groupe_dpe_statistique_logement.csv'
    batiment_groupe_path = 'batiment_groupe.csv'
    batiment_groupe_ffo_bat_path = 'batiment_groupe_ffo_bat.csv'

    try: 
        log.info(" Chargement des fichiers CSV...")
        batiment_groupe_synthese_propriete_usage = pd.read_csv(os.path.join(root, batiment_groupe_synthese_propriete_usage_path),low_memory=False)        
        batiment_groupe_dpe_statistique_logement = pd.read_csv(os.path.join(root, batiment_groupe_dpe_statistique_logement_path),low_memory=False)        
        batiment_groupe = pd.read_csv(os.path.join(root, batiment_groupe_path),low_memory=False)        
        batiment_groupe_ffo_bat= pd.read_csv(os.path.join(root, batiment_groupe_ffo_bat_path),low_memory=False)

    except FileNotFoundError as e:
        log.error(f"Fichier non trouvé: {str(e)}")
        return
    except Exception as e:
        log.error(f"Erreur lors du chargement des fichiers: {str(e)}")
        return

    #transform
    
    log.info("Transformations...")
    
    log.info(" Transformation text pour chaque batiment ... ")
    batiment_groupe_synthese_propriete_usage_transform = preprocesse_batiment_groupe_synthese_propriete_usage(batiment_groupe_synthese_propriete_usage)
    batiment_groupe_dpe_statistique_logement_transform = prepocess_batiment_groupe_dpe_statistique_logement(batiment_groupe_dpe_statistique_logement)
    batiment_groupe_transform = prepocess_batiment_batiment_groupe(batiment_groupe)
    batiment_groupe_ffo_bat_transform = prepocess_batiment_groupe_ffo_bat(batiment_groupe_ffo_bat)

    df_merged = batiment_groupe_synthese_propriete_usage_transform\
    .merge(batiment_groupe_dpe_statistique_logement_transform, on='batiment_groupe_id', how='inner')\
    .merge(batiment_groupe_transform, on='batiment_groupe_id', how='inner')\
    .merge(batiment_groupe_ffo_bat_transform, on='batiment_groupe_id', how='inner')

    batiment_description_dataset = pd.DataFrame({'Description_btm':df_merged.apply(generer_description_batiment, axis=1) })
    
    os.makedirs(output, exist_ok=True)
    
    # Sauvegarder les résultats
    output_path = os.path.join(output, 'batiment_description_dataset.csv')
    batiment_description_dataset.to_csv(output_path, index=False)
    
    
    log.info("transformation stat ... ")
    
    df_stats_commune = stats_commune(df_merged)
    df_stats_departement = stats_departement(df_merged)
    df_stats_usage = stats_usage(df_merged)
    df_stats_dpe = stats_dpe(df_merged)    
    df_stats_niveau_bt = stats_niveau_bt(df_merged)

    # save
    df_stats_commune.to_csv(os.path.join(output, 'stats_commune.csv'), index=False)
    df_stats_departement.to_csv(os.path.join(output, 'stats_departement.csv'), index=False)
    df_stats_usage.to_csv(os.path.join(output, 'stats_usage.csv'), index=False)
    df_stats_dpe.to_csv(os.path.join(output, 'stats_dpe.csv'), index=False)
    df_stats_niveau_bt.to_csv(os.path.join(output, 'stats_niveau_bt.csv'), index=False)

    log.info("Pipeline ETL terminé avec succès")


if __name__ == "__main__":

    etl_pipeline(
        config.dir_in_etl, 
        config.dir_out_etl
        )
