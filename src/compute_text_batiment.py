import pandas as pd
from logger import logger as log


classe_dpe = {
    'nb_classe_bilan_dpe_a': 'Classe A pour le diagnostic de performance énergétique (DPE)',
    'nb_classe_bilan_dpe_b': 'Classe B pour le diagnostic de performance énergétique (DPE)',
    'nb_classe_bilan_dpe_c': 'Classe C pour le diagnostic de performance énergétique (DPE)',
    'nb_classe_bilan_dpe_d': 'Classe D pour le diagnostic de performance énergétique (DPE)',
    'nb_classe_bilan_dpe_e': 'Classe E pour le diagnostic de performance énergétique (DPE)',
    'nb_classe_bilan_dpe_f': 'Classe F (passoire thermique) pour le diagnostic de performance énergétique (DPE)',
    'nb_classe_bilan_dpe_g': 'Classe G (passoire thermique) pour le diagnostic de performance énergétique (DPE)',

    
    'nb_classe_conso_energie_arrete_2012_a': "Classe A selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_b': "Classe B selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_c': "Classe C selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_d': "Classe D selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_e': "Classe E selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_f': "Classe F (passoire thermique) selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_g': "Classe G (passoire thermique) selon la méthode de l'arrêté du 8 février 2012",
    'nb_classe_conso_energie_arrete_2012_nc': " Pas de Classe attribuée selon la méthode de l'arrêté du 8 février 2012"
}


def transform_class_dpe(row:pd.Series) -> list:
    """ transforme les batiments en text pour leurs classes dpe """
    
    res = [classe_dpe[col] for col, val in row.items() if val > 0]
    return ','.join(res)


def generer_description_batiment(row:pd.Series) -> list:
    """ transforme toutes les colonnes une seule colonne textuelle qui decrit un batiment """
    
    return (
        f"Le bâtiment {row['batiment_groupe_id']} de type {row['usage_principal_bdnb_open']}, "
        f"construit en {row['annee_construction']}, se trouve dans le département {row['code_departement_insee']}, "
        f"dans la commune {row['libelle_commune_insee']} (code postal {row['code_commune_insee']}), "
        f"il possède une surface de {row['s_geom_groupe']} m², {row['nb_niveau']} étage(s) avec {row['nb_log']} logement(s), "
        f"des murs en {row['mat_mur_txt']}, un toit en {row['mat_toit_txt']}, "
        f"et est classé {row['classe dpe (diagnostique de performance energetique)']} au diagnostic de performance énergétique."
    )

def preprocesse_batiment_groupe_synthese_propriete_usage(df:pd.DataFrame) -> pd.DataFrame:
    """ Preprocess batiment_groupe_synthese_propriete_usage dataframe, regroupant principalement le type de propriete """
    log.info("Prétraitement dataframe synthese_propriete_usage.csv")

    return df


def prepocess_batiment_groupe_dpe_statistique_logement(df:pd.DataFrame) -> pd.DataFrame:
    """ Preprocess groupe_dpe_statistique_logement dataframe, contenant les infos sur le dpe (diagnostique de performance energetique) """
    
    log.info("Prétraitement dataframe dpe_statistique_logement.csv")
    
    df_drop_nan = df.dropna()
    
    df_btId_dpt = df_drop_nan[['batiment_groupe_id']].copy()
    df_classe = df_drop_nan.drop(['batiment_groupe_id','code_departement_insee'], axis=1)
    df_btId_dpt['classe dpe (diagnostique de performance energetique)'] = df_classe.apply(transform_class_dpe, axis=1)

    return df_btId_dpt


def prepocess_batiment_batiment_groupe(df:pd.DataFrame) -> pd.DataFrame:
    """Preprocess batiment_groupe dataframe, contenant les infos tel que: la surface, nom de commune, etc) """
    log.info("Prétraitement dataframe batiment_groupe.csv")
    
    df_drop_nan = df.dropna()
    log.info(f"Après suppression des NaN: {len(df_drop_nan)} lignes")

    df_drop_axis = df_drop_nan.drop(['geom_groupe','code_departement_insee','code_iris','code_epci_insee'],axis=1)
    
    return df_drop_axis

def prepocess_batiment_groupe_ffo_bat(df:pd.DataFrame) -> pd.DataFrame:
    """Preprocess batiment_groupe_ffo_bat dataframe, contenant les infos tel que: l'anne de construction, nombre de niveau, nombe de logment, etc) """
    log.info("Prétraitement dataframe groupe_ffo_bat.csv")
    
    df_drop_nan = df.dropna()
    log.info(f"Après suppression des NaN: {len(df_drop_nan)} lignes")
    
    df_drop_axis = df_drop_nan.drop(['code_departement_insee', 'usage_niveau_1_txt'], axis=1)
    
    return df_drop_axis
