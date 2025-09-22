import pandas as pd
import tabula

def parser_groupes_par_semaine(df, semaine_start=4):
    semaine_cols = df.columns[semaine_start:]
    groupes = set()
    for col in semaine_cols:
        groupes |= set(df[col].dropna().unique())
    groupes = [g for g in groupes if pd.notna(g)]
    resultat_global = []
    for groupe in groupes:
        occurences_groupe = []
        for col in semaine_cols:
            indices = df.index[df[col] == groupe].tolist()
            if indices:
                occurences_groupe.append({'semaine': col, 'creneau': indices})
        resultat_global.append({'groupe': groupe, 'occurences': occurences_groupe})
    return resultat_global

if __name__ == "__main__":
    file_path = "coloscope.pdf"
    tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True, lattice=True)
    df = tables[0]
    resultats = parser_groupes_par_semaine(df)
    print(resultats)
    # Optionnel: écrire dans un fichier
    import json
    with open("resultats.json", "w") as f:
        json.dump(resultats, f, indent=2)