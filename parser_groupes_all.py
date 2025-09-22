import pandas as pd
import tabula
import json

def parser_groupes_par_semaine(df, semaine_start=4):
    """
    Pour chaque groupe présent dans le tableau, retourne une liste de dict par groupe :
    [
      {
        'groupe': ...,
        'occurences': [
            {'semaine': ..., 'creneau': [liste_index_ligne]}
        ]
      },
      ...
    ]
    semaine_start : index où commencent les colonnes de semaine (par défaut 4)
    """
    # Récupère les colonnes correspondant aux semaines
    semaine_cols = list(df.columns[semaine_start:])

    # Récupère tous les groupes présents dans les colonnes semaine
    groupes = set()
    for col in semaine_cols:
        groupes.update(df[col].dropna().unique())
    groupes = [g for g in groupes if pd.notna(g)]

    resultat_global = []
    for groupe in groupes:
        occurences_groupe = []
        for idx_semaine, col in enumerate(semaine_cols):
            # Cherche les lignes où le groupe apparaît dans la colonne de la semaine
            indices = df.index[df[col] == groupe].tolist()
            if indices:
                occurences_groupe.append({
                    'semaine': idx_semaine,    # Numéro réel de la semaine (commence à 0)
                    'nom_colonne': col,        # Nom de la colonne (optionnel)
                    'creneau': indices
                })
        resultat_global.append({
            'groupe': groupe,
            'occurences': occurences_groupe
        })
    return resultat_global

if __name__ == "__main__":
    file_path = "coloscope.pdf"
    # Extraction du tableau
    tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True, lattice=True)
    df = tables[0]  # Prend le premier tableau, adapte si besoin

    resultats = parser_groupes_par_semaine(df)
    print(json.dumps(resultats, indent=2, ensure_ascii=False))

    # Sauvegarde dans un fichier JSON
    with open("resultats.json", "w", encoding="utf-8") as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)