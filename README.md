<div style="text-align: center; display: flex; align-items: center; justify-content: center; gap: 12px;">
  <img src="images/logo.PNG" alt="Logo ESI" width="57" />
  <h1 style="margin: 0;">Dashboard RGPH 2024</h1>
</div>

## Projet : Dashboard Interactif RGPH 2024

### Description

Le **Dashboard RGPH 2024** est une application interactive développée pour explorer les données issues du **Recensement Général de la Population et de l'Habitat (RGPH) 2024**.  
Grâce à une interface claire et intuitive, il permet de visualiser les dynamiques démographiques et socioéconomiques au niveau régional et national.

---

## Source des Données

Les données utilisées dans ce projet proviennent du fichier Excel suivant :

**Indicateurs démographiques et socioéconomiques du Royaume du Maroc selon les résultats du RGPH 2024.xlsx**  
**Source :** Téléchargé depuis le site officiel du **Haut-Commissariat au Plan (hcp.ma)**

Ce fichier brut a été nettoyé, restructuré et transformé pour produire un nouveau fichier Excel contenant deux feuilles distinctes :

- **Population** :  
  Données agrégées (urbain + rural) par région, avec total national

- **Ménage** :  
  Statistiques sur les ménages, également regroupées par région

Ces deux feuilles sont exploitées directement par le dashboard pour les visualisations et tableaux interactifs.

---

## Structure du Dashboard

### 1. Accueil

- Présentation du projet
- Objectifs du tableau de bord
- Informations générales sur les données et leur traitement

### 2. Section Statistiques (section clé)

Deux sous-sections interactives :

- **Population** :  
  Graphiques comparatifs par région, milieu, sexe, etc.

- **Ménage** :  
  Statistiques sur les ménages par région avec filtres dynamiques

### 3. Tableau de Population

- Affichage tabulaire interactif
- Filtres par :
  - Milieu de résidence
  - Sexe
  - Catégorie
- Possibilité de téléchargement

### 4. Tableau de Ménage

- Exploration détaillée des indicateurs liés aux ménages
- Téléchargement des données filtrées

---

## Structure du Projet

Voici la structure des fichiers et dossiers du projet :



| Élément/Fichier          | Description                                                         |
|--------------------------|----------------------------------------------------------------------|
| `app.py`                 | Point de départ de l'application Streamlit                         |
| `pages/pop.py`           | Page dédiée aux données de population                              |
| `pages/men.py`           | Page dédiée aux données des ménages                                |
| `data/`                  | Contient les  Données brutes du HCP ,  Script de préparation des données en Python, le fichier nettoyé à 2 feuilles Excel
| `images/`                | Logos et illustrations utilisés dans l'application                 |
| `README.md`              | Documentation du projet                                             |
| `requirements.txt`       | Liste des dépendances Python                                        |
| `.streamlit/config.toml` | Configuration spécifique à Streamlit (thème, serveur, etc.)           |

---

## Technologies Utilisées

- Python
- Streamlit
- Pandas
- Plotly
- Excel (pour le prétraitement initial)

---

## Auteur

**Hadil Barzani**  
Étudiant à l'ESI  
Stagiaire au Haut-Commissariat au Plan – DSIS

---

## Déploiement

- **URL de déploiement ** : https://dashboard-rgph-2024.streamlit.app/

Pour exécuter localement :

```bash
python -m pip install -r requirements.txt
streamlit run main.py
```

Pour déployer (exemples) :
- Streamlit Cloud : téléversez le dépôt et ajoutez `main.py` comme script de démarrage.
- Heroku / Railway / Render : créez un service Python, installez `requirements.txt` et lancez `streamlit run main.py`.

Remplacez `your-app-name` par le nom choisi pour votre application Streamlit et utilisez l'URL fournie après le déploiement.
