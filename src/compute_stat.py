# calcul les stats des donnees

import pandas as pd
from logger import logger as log


def calculate_comprehensive_stats_region_commune(df:pd.DataFrame, group_columns:list):
    """ calcul les stats groupees pour differentes colonnes numerique (region, commune)"""


    df = df.copy()        
    df['classe_dpe_simple'] = df['classe dpe (diagnostique de performance energetique)'].str.extract(r'Classe ([A-G])')
    df['est_passoire_thermique'] = df['classe_dpe_simple'].isin(['F', 'G'])

    
    agg_dict = {

        'nb_niveau': ['mean', 'median', 'min', 'max'],
        'annee_construction': ['mean', 'median', 'min', 'max'],
        'nb_log': ['mean', 'median', 'sum', 'min', 'max'],
        'est_passoire_thermique': 'mean',  
        
        'usage_principal_bdnb_open': lambda x: x.value_counts().to_dict(),
        'classe_dpe_simple': lambda x: x.value_counts().to_dict(),
        'mat_mur_txt': lambda x: x.value_counts().to_dict(),
        'mat_toit_txt': lambda x: x.value_counts().to_dict()
    }

    stats = df.groupby(group_columns).agg(agg_dict).reset_index()
    
    stats.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in stats.columns.values]

    count_df = df.groupby(group_columns).size().reset_index(name='nb_count')
    stats = stats.merge(count_df, on=group_columns)
    
    return stats


def ligne_en_texte_naturel(row:pd.Series):
    
    commune = row.get('code_commune_insee', 'inconnue')
    region = row.get('code_departement_insee', '')
    contexte = f"la commune {commune}" if commune != 'inconnue' else f"la région  {region}"
    
    nb_bat = row.get('nb_count', 0)
    
    texte = f"Statistiques des bâtiments dans {contexte} : "

    texte += f"Les bâtiments ont en moyenne {int(row['nb_niveau_mean'])} niveaux (médiane: {int(row['nb_niveau_median'])}, sur un total de {nb_bat} bâtiments analysés). "
    texte += f"Le nombre d'étages varie de {int(row['nb_niveau_min'])} à {int(row['nb_niveau_max'])}. "
    texte += f"L'année de construction moyenne est {int(row['annee_construction_mean'])} (médiane: {int(row['annee_construction_median'])}), "
    texte += f"avec des bâtiments construits entre {int(row['annee_construction_min'])} et {int(row['annee_construction_max'])}. "

    texte += f"Ces bâtiments comprennent en moyenne {int(row['nb_log_mean'])} logements (médiane: {int(row['nb_log_median'])}). "
    texte += f"Au total, {contexte} compte {int(row['nb_log_sum'])} logements répartis dans {nb_bat} bâtiments, "
    texte += f"avec un minimum de {int(row['nb_log_min'])} et un maximum de {int(row['nb_log_max'])} logements par bâtiment. "

    pourcentage_passoires = row['est_passoire_thermique_mean'] * 100
    texte += f"{pourcentage_passoires:.1f}% des bâtiments sont des passoires thermiques (DPE F ou G). "

    # Catégories
    def format_dict_col(d, label):
        if isinstance(d, dict) and len(d) > 0:
            total = sum(d.values())
            parts = [f"{k} ({(v/total)*100:.1f}%)" for k, v in d.items()]
            return f"{label}: " + ", ".join(parts) + ". "
        return ""

    texte += format_dict_col(row.get('usage_principal_bdnb_open_<lambda>', {}), "Les principaux usages des bâtiments sont")
    texte += format_dict_col(row.get('classe_dpe_simple_<lambda>', {}), "Répartition des classes DPE")
    texte += format_dict_col(row.get('mat_mur_txt_<lambda>', {}), "Principaux matériaux de murs")
    texte += format_dict_col(row.get('mat_toit_txt_<lambda>', {}), "Principaux matériaux de toiture")

    return texte.strip()


def calculate_comprehensive_stats_usage_classe(df:pd.DataFrame, group_columns:list):
    """ calcul les stats groupees pour differentes colonnes (dpe, niveau) """


    df = df.copy()        
    df['classe_dpe_simple'] = df['classe dpe (diagnostique de performance energetique)'].str.extract(r'Classe ([A-G])')
    df['est_passoire_thermique'] = df['classe_dpe_simple'].isin(['F', 'G'])

    if group_columns[0] != 'nb_niveau':
        col = 'nb_niveau', ['mean', 'median', 'min', 'max']
    else: 
        col = group_columns[0], lambda x: x.value_counts().to_dict()

    agg_dict = {

        'annee_construction': ['mean', 'median', 'min', 'max'],
        'nb_log': ['mean', 'median', 'count', 'sum', 'min', 'max'],
        col[0]:col[1],
        
        'code_commune_insee': lambda x: x.value_counts().to_dict(),
        'code_departement_insee': lambda x: x.value_counts().to_dict(),
        'mat_mur_txt': lambda x: x.value_counts().to_dict(),
        'mat_toit_txt': lambda x: x.value_counts().to_dict()
    }

    stats = df.groupby(group_columns).agg(agg_dict).reset_index()
    
    stats.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in stats.columns.values]

    count_df = df.groupby(group_columns).size().reset_index(name='nb_count')
    stats = stats.merge(count_df, on=group_columns)
    
    return stats

def ligne_en_texte_par_groupe(row:pd.Series, group_type:str):
    """Génère une ligne de texte naturel adaptée au groupement (niveau, DPE, usage)"""

    try:
        groupe_valeur = row[group_type]
        if isinstance(groupe_valeur, (pd.Series, dict)):
            groupe_valeur = list(groupe_valeur.values())[0] if isinstance(groupe_valeur, dict) else groupe_valeur.iloc[0]
        groupe_valeur = str(groupe_valeur).strip()
    except Exception:
        groupe_valeur = "inconnu"

    nb_bat = row.get('nb_count', 0)

    if group_type == 'nb_niveau':
        contexte = f"les bâtiments ayant {groupe_valeur} étage(s)"
    elif group_type == 'classe_dpe_simple':
        contexte = f"les bâtiments classés {groupe_valeur} au DPE"
    elif group_type == 'usage_principal_bdnb_open':
        contexte = f"les bâtiments de type {groupe_valeur.lower()}"
    else:
        contexte = f"le groupe {groupe_valeur}"

    texte = f"Statistiques pour {contexte} : "

    if group_type != 'nb_niveau':
        texte += f"En moyenne, ces bâtiments ont {int(row.get('nb_niveau_mean', 0))} niveaux (médiane: {int(row.get('nb_niveau_median', 0))}), "
        texte += f"avec un minimum de {int(row.get('nb_niveau_min', 0))} et un maximum de {int(row.get('nb_niveau_max', 0))} niveaux. "

    if group_type != 'annee_construction':
        texte += f"L'année de construction moyenne est {int(row.get('annee_construction_mean', 0))} (médiane: {int(row.get('annee_construction_median', 0))}), "
        texte += f"avec des bâtiments construits entre {int(row.get('annee_construction_min', 0))} et {int(row.get('annee_construction_max', 0))}. "

    if group_type != 'nb_log':
        texte += f"Ces bâtiments ont en moyenne {int(row.get('nb_log_mean', 0))} logements (médiane: {int(row.get('nb_log_median', 0))}). "
        texte += f"Au total, ils représentent {int(row.get('nb_log_sum', 0))} logements répartis dans {nb_bat} bâtiments, "
        texte += f"avec un minimum de {int(row.get('nb_log_min', 0))} et un maximum de {int(row.get('nb_log_max', 0))} logements par bâtiment. "

    if group_type != 'classe_dpe_simple':
        pourcentage_passoires = row.get('est_passoire_thermique_mean', 0) * 100
        texte += f"{pourcentage_passoires:.1f}% de ces bâtiments sont des passoires thermiques (DPE F ou G). "

    
    def format_dict_col(d, label, skip=False):
        if skip:
            return ""
        if isinstance(d, dict) and len(d) > 0:
            total = sum(d.values())
            parts = [f"{k} ({(v/total)*100:.1f}%)" for k, v in d.items()]
            return f"{label}: " + ", ".join(parts) + ". "
        return ""

    texte += format_dict_col(row.get('usage_principal_bdnb_open_<lambda>', {}), "Usages principaux", group_type == 'usage_principal_bdnb_open')
    texte += format_dict_col(row.get('classe_dpe_simple_<lambda>', {}), "Répartition des classes DPE", group_type == 'classe_dpe_simple')
    texte += format_dict_col(row.get('mat_mur_txt_<lambda>', {}), "Matériaux de murs")
    texte += format_dict_col(row.get('mat_toit_txt_<lambda>', {}), "Matériaux de toiture")

    return texte.strip()


# compute stat

def stats_commune(df:pd.DataFrame) -> pd.DataFrame:
    
    log.info('calcule les stats par commune ... ')
    stats_by_commune  = calculate_comprehensive_stats_region_commune(df, ['code_commune_insee'])
    
    stats_by_commune_text = pd.DataFrame({
    'code_commune_insee' :stats_by_commune['code_commune_insee'],
    'stat' : stats_by_commune.apply(ligne_en_texte_naturel,axis=1)})

    return stats_by_commune_text


def stats_departement(df:pd.DataFrame) -> pd.DataFrame:

    log.info('calcule les stats par departement ... ')
    stats_by_departement = calculate_comprehensive_stats_region_commune(df, ['code_departement_insee'])
    
    stats_by_departement_text = pd.DataFrame({
    'code_departement_insee' :stats_by_departement['code_departement_insee'],
    'stat' : stats_by_departement.apply(ligne_en_texte_naturel,axis=1)}) 

    return stats_by_departement_text 


def stats_usage(df:pd.DataFrame) -> pd.DataFrame:

    log.info("calcule les stats par les classe d'usage ... ")
    stats_by_usage = calculate_comprehensive_stats_usage_classe(df, ['usage_principal_bdnb_open'])
    
    usage_principal_bdnb_open_text = pd.DataFrame({
    'usage_principal_bdnb_open' :stats_by_usage['usage_principal_bdnb_open'],
    'stat' : stats_by_usage.apply(lambda row: ligne_en_texte_par_groupe(row,'usage_principal_bdnb_open') ,axis=1)}) 

    return usage_principal_bdnb_open_text 


def stats_dpe(df:pd.DataFrame) -> pd.DataFrame:
    
    log.info('calcule les stats par classe energetique (dpe) ... ')
    stats_by_classe_dpe = calculate_comprehensive_stats_usage_classe(df, ['classe_dpe_simple'])

    stats_by_classe_dpe_text = pd.DataFrame({
    'classe_dpe_simple' :stats_by_classe_dpe['classe_dpe_simple'],
    'stat' : stats_by_classe_dpe.apply(lambda row: ligne_en_texte_par_groupe(row,'classe_dpe_simple') ,axis=1)}) 

    return stats_by_classe_dpe_text 


def stats_niveau_bt(df:pd.DataFrame) -> pd.DataFrame:
    
    log.info('calcule les stats par niveau de batiment ... ')
    stats_by_classe_nb_niveau = calculate_comprehensive_stats_usage_classe(df, ['nb_niveau'])

    stats_by_classe_nb_niveau_text = pd.DataFrame({
    'nb_niveau' :stats_by_classe_nb_niveau['nb_niveau'],
    'stat' : stats_by_classe_nb_niveau.apply(lambda row: ligne_en_texte_par_groupe(row,'nb_niveau') ,axis=1)}) 

    return stats_by_classe_nb_niveau_text 

