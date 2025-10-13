# Import des bibliothèques
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyPDF2 import PdfReader

# Configuration de Seaborn pour les graphes
sns.set(style="whitegrid")

# Dossier contenant les PDF
pdf_folder = "./data"

# Fonction pour lister tous les fichiers PDF dans le dossier
def list_pdf_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".pdf")]

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Fonction pour compter les occurrences avec regex (insensible à la casse)
def count_occurrences(text, pattern):
    return len(re.findall(pattern, text, re.IGNORECASE))

# Fonction pour diviser le texte par pages
def split_text_pages(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        pages_text = [page.extract_text() for page in reader.pages]
    return pages_text

# Fonction principale pour analyser un texte de livre
def analyze_book(pdf_path, book_name):
    text = extract_text_from_pdf(pdf_path)
    pages_text = split_text_pages(pdf_path)
    n_pages = len(pages_text)
    
    # Comptage global
    stats = {
        "Livre": book_name,
        "Pages": n_pages,
        "Harry_cicatrice": count_occurrences(text, r"\bcicatrice\b"),
        "Hermione_mais": count_occurrences(text, r"\bmais\b"),
        "Dumbledore_interfere": count_occurrences(text, r"Dumbledore.*(décide|change|intervient|ordonne|influence|tourne et retourne)"),
        "Rogue_dark": count_occurrences(text, r"Rogue.*(mystérieux|dark|méchant|terrible)"),
        "Harry_speak": count_occurrences(text, r"\bHarry\b"),
        "Hermione_speak": count_occurrences(text, r"\bHermione\b"),
        "Ron_speak": count_occurrences(text, r"\bRon\b"),
        "Actes_illicites": count_occurrences(text, r"vol|tricherie|mensonge|meurtre|attaque|poison")
    }
    
    # Normalisation par 100 pages
    for key in ["Harry_cicatrice", "Hermione_mais", "Dumbledore_interfere", "Rogue_dark", "Actes_illicites"]:
        stats[f"{key}_par_100_pages"] = stats[key] / n_pages * 100
    
    return stats

# Parcours de tous les fichiers PDF et création du DataFrame
pdf_files = list_pdf_files(pdf_folder)
stats_list = []

for i, pdf in enumerate(pdf_files):
    book_name = f"HP{i+1}"
    stats_list.append(analyze_book(pdf, book_name))

df = pd.DataFrame(stats_list)

# Affichage du tableau des statistiques
print(df)

# ----------------------------
# Visualisations
# ----------------------------

# Création du dossier plots s'il n'existe pas
os.makedirs("./plots", exist_ok=True)

# ----------------------------
# Bar plot des occurrences brutes
# ----------------------------
fig, ax = plt.subplots(figsize=(12,6))
df_plot = df.set_index("Livre")[["Harry_cicatrice", "Hermione_mais", "Dumbledore_interfere", "Rogue_dark", "Actes_illicites"]]
df_plot.plot(kind="bar", ax=ax)
plt.title("Statistiques par livre - Harry Potter")
plt.ylabel("Nombre d'occurrences")
plt.xticks(rotation=0)

# Sauvegarde du graphique
plt.savefig("./plots/statistiques_brutes.png", bbox_inches='tight', dpi=300)
plt.close(fig)  # ferme le graphique pour ne pas afficher à l'écran

# ----------------------------
# Bar plot des occurrences normalisées par 100 pages
# ----------------------------
fig, ax = plt.subplots(figsize=(12,6))
df_plot2 = df.set_index("Livre")[[
    "Harry_cicatrice_par_100_pages", 
    "Hermione_mais_par_100_pages", 
    "Dumbledore_interfere_par_100_pages", 
    "Rogue_dark_par_100_pages", 
    "Actes_illicites_par_100_pages"]]
df_plot2.plot(kind="bar", ax=ax)
plt.title("Statistiques par 100 pages - Harry Potter")
plt.ylabel("Occurrences par 100 pages")
plt.xticks(rotation=0)

# Sauvegarde du graphique
plt.savefig("./plots/statistiques_100_pages.png", bbox_inches='tight', dpi=300)
plt.close(fig)

# Comparaison du nombre de prises de parole
fig, ax = plt.subplots(figsize=(10,6))

# Sélection des colonnes de prises de parole
df_speak = df.set_index("Livre")[["Harry_speak", "Hermione_speak", "Ron_speak"]]

# Bar plot
df_speak.plot(kind="bar", ax=ax)
plt.title("Comparaison du nombre de prises de parole par livre")
plt.ylabel("Nombre d'occurrences du nom (approximation)")
plt.xticks(rotation=0)

# Sauvegarde du graphique
os.makedirs("./plots", exist_ok=True)
plt.savefig("./plots/prises_de_parole.png", bbox_inches='tight', dpi=300)
plt.close(fig)

# Affichage du personnage le plus bavard par livre
df_speak["Personnage_le_plus_bavard"] = df_speak.idxmax(axis=1)
print(df_speak[["Personnage_le_plus_bavard"]])


# ----------------------------
# Documentation rapide
# ----------------------------
"""
Comment chaque statistique est déterminée :
- Harry_cicatrice : recherche du mot 'cicatrice' dans le texte.
- Hermione_mais : recherche du mot 'mais' après un nom Hermione.
- Dumbledore_interfere : recherche de phrases indiquant qu'il influence l'histoire (mots-clés : décide, change, intervient, ordonne, tourne et retourne).
- Rogue_dark : recherche de phrases où Rogue est qualifié de mystérieux ou 'dark'.
- Harry/Hermione/Ron_speak : approximation du nombre de prises de parole par occurrence du nom.
- Actes_illicites : recherche de mots indiquant un acte moralement ou légalement répréhensible (vol, tricherie, meurtre, attaque, poison).

Limites :
- Comptage basé sur des mots-clés : certaines occurrences peuvent être manquées ou surcomptées.
- La prise de parole par personnage est approximative (se base sur le nom seulement, pas sur le dialogue réel).
- L'interprétation des actes illicites dépend de mots précis, certaines nuances sont ignorées.
"""