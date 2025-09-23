import streamlit as st
import pandas as pd
import base64

# --- CSS GLOBAL ---
st.markdown("""
    <style>
     
        /* Only set font globally */
        * {
            font-family: "Segoe UI", sans-serif;
        }

        hr {
            border: 1px solid #cccccc;
        }
        /* couleur du titre principal */
        h1 {
            color: #6B0039 !important;
        }

        .custom-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .custom-header img {
            height: 70px;
        }

        .header-text h1 {
            margin: 0;
            color: #1f4e79;
            border: 2px solid #1f4e79;
            padding: 10px;
            border-radius: 5px;
            background-color: #e6f0f9;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .header-text span {
            font-size: 16px;
            color: #666666;
        }

        .centered-title {
            text-align: center;
        }

        .intro-text {
            font-size: 17px;
            line-height: 1.6;
            text-align: center;
        }

        .ul-objectif {
            font-size: 17px;
            line-height: 1.6;
            padding-left: 30px;
        }

        .footer {
            text-align: center;
            color: #666666;
            font-size: 14px;
            margin-top: 30px;
            Background-color: #e7dde2;
        }

        .subtitle {
            color: #70214b !important;
        }

        .section-title {
            color: #003366;
            font-weight: 600;
        }

        .spaced-section {
            margin-top: 25px;
        }

        div.stButton > button:first-child {
            background-color: #f8f4f7 !important;
        }
        .st-emotion-cache-3jjymv.e1g8wfdw0 p{
            color: #F5EDF2 !important;
            background-color: #6B0039 !important;
            }  
        span.st-emotion-cache-ujm5ma.ejhh0er0{
            background-color: #1f4e79 !important;}
        div.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-ae.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9.st-ba.st-bb.st-bc{
            background-color: #6B0039!important;
            }
         /*page statistiques*/
        .stats-container {
            display: flex;
            gap: 30px;
            justify-content: center;
            margin-top: 40px;
        }

        .stats-box {
            background-color: #6B0039;
            color: #f8f4f7;
            border-radius: 16px;
            padding: 40px 30px;
            width: 45%;
            transition: transform 0.3s ease;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .stats-box:hover {
            transform: scale(1.05);
        }

        .stats-box h2 {
            margin-bottom: 15px;
            font-size: 28px;
        }

        .stats-box p {
            font-size: 16px;
            line-height: 1.6;
        }
    

        
      
            </style>
""", unsafe_allow_html=True)

# --- Configuration Streamlit ---
st.set_page_config(page_title="Dashboard RGPH 2024", layout="wide")


# --- Chargement des données Excel ---
@st.cache_data
def load_data():
    file_path = "data/rgph2024_regions.xlsx"
    try:
        data_dict = {
            "Population": pd.read_excel(file_path, sheet_name="Population"),
            "Menage": pd.read_excel(file_path, sheet_name="Ménages")
        }
        return data_dict
    except FileNotFoundError:
        st.error(f"Fichier non trouvé : {file_path}")
        return {"Population": pd.DataFrame(), "Menage": pd.DataFrame()}
    except ValueError as e:
        st.error(f"Erreur lors du chargement des feuilles : {e}")
        return {"Population": pd.DataFrame(), "Menage": pd.DataFrame()}

data = load_data()

# --- Chargement et affichage du logo dans l'en-tête ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("images/logo.PNG")

st.markdown(f"""
    <div class="custom-header">
        <img src="data:image/png;base64,{img_base64}" alt="Logo ESI+HCP">
        <div class="header-text">
            <h1>Dashboard RGPH 2024</h1> 
        </div>
    </div>
""", unsafe_allow_html=True)
# --- Gestion de la navigation avec session_state ---


params = st.query_params
passed_menu = params.get("menu", None)

if passed_menu and passed_menu != st.session_state.get("menu"):
    st.session_state.menu = passed_menu
    st.query_params.clear()  # Clear the URL for cleanliness

# Initialisation de la session_state pour le menu
if "menu" not in st.session_state:
    st.session_state.menu = "Accueil"

# Sidebar navigation
st.sidebar.title("Menu")
menu = st.sidebar.radio("Aller vers :", ["Accueil", "À propos", "Statistiques", "Tableau de population", "Tableau de ménage"], 
                        index=["Accueil", "À propos", "Statistiques", "Tableau de population", "Tableau de ménage"].index(st.session_state.menu))

if menu != st.session_state.menu:
    st.session_state.menu = menu


# === PAGE: ACCUEIL ===
if st.session_state.menu == "Accueil":
    st.title("ACCUEIL")

    st.markdown("<h3 class='subtitle'>Introduction du Dashboard</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div >
        Bonjour et bienvenue sur le <strong>Dashboard RGPH 2024</strong> !
        Ce tableau de bord interactif a été conçu pour visualiser et analyser les données issues du 
        <strong>Recensement Général de la Population et de l'Habitat (RGPH) 2024</strong>. 
        Les informations présentées ici proviennent des données officielles du <strong>Haut-Commissariat au Plan (HCP)</strong>, 
        après un processus rigoureux de filtrage et de structuration.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Aller aux Statistiques", key="btn_stats", use_container_width=True):
        st.session_state.menu = "Statistiques"
        st.rerun()


    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h3 class='subtitle'>Description du Dataset</h3>", unsafe_allow_html=True)
    st.markdown("**Ces données sont composées de deux volets principaux :**")

    st.markdown("""
    <div class='intro-text'>
        <span class='section-title'>Volet Population</span><br>
        Ce volet regroupe des informations sur la démographie, l'éducation, et l'emploi/économie.
        Les données sont disponibles pour l'ensemble, le milieu rural et le milieu urbain.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Accéder au Volet Population", key="btn_pop", use_container_width=True):
        st.session_state.menu = "Tableau de population"
        st.rerun()

    st.markdown("""
    <div class='intro-text spaced-section'>
        <span class='section-title'>Volet Ménages</span><br>
        Ce volet fournit des données sur le type de logement, les conditions de vie, l'équipement, et l'environnement des ménages.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Accéder au Volet Ménages", key="btn_menage", use_container_width=True):
        st.session_state.menu = "Tableau de ménage"
        st.rerun()



 # === PAGE: À propos ===       
elif st.session_state.menu == "À propos":
    st.title("À propos")
    st.markdown("<h3 class='subtitle'>Qui sommes-nous ?</h3>", unsafe_allow_html=True)
    st.write("""
    Je suis **Hadil Barzani**, étudiant à l'**ESI** (École Supérieure d'Informatique) et stagiaire au sein de la **DSIS-HCP**.
    
    Ce tableau de bord a été développé dans le cadre de mon stage pour visualiser et interpréter les données du **RGPH 2024**.
    
    L'objectif est de permettre une compréhension claire des données démographiques, sociales et économiques à travers des visualisations interactives.
    """)

    st.markdown("<h3 class='subtitle'>FAQ</h3>", unsafe_allow_html=True)
    question = st.selectbox("Questions fréquentes :", [
        "C'est quoi le HCP ?",
        "C'est quoi le RGPH ?",
        "Quel est l'objectif de ce dashboard ?",
        "Comment sont collectées les données ?",
        "Comment puis-je vous contacter si ma question n'apparaît pas dans la FAQ ?"
    ])
    if question == "C'est quoi le HCP ?":
        st.info("""
        Le **Haut-Commissariat au Plan (HCP)** est l'organisme marocain chargé de la production, 
        l'analyse et la diffusion des statistiques officielles, y compris les recensements.
        """)

    elif question == "C'est quoi le RGPH ?":
        st.info("""
        Le **Recensement Général de la Population et de l'Habitat (RGPH)** est une opération statistique nationale 
        visant à recueillir des informations sur la population et les logements d'un pays. 
        Il permet d'obtenir des données fiables pour la planification et les politiques publiques.
        """)



    elif question == "Quel est l'objectif de ce dashboard ?":
        st.markdown("""
        <div style='background-color:#f0f2f6; padding:15px; border-left:5px solid #91c2f9; border-radius:5px'>
            <p><strong>L'objectif est de :</strong></p>
            <ul style='margin-left:20px;'>
                <li>Visualiser les données démographiques, éducatives, économiques et de logement à l'échelle régionale,</li>
                <li>Comparer les informations entre les zones urbaines et rurales,</li>
                <li>Offrir un accès rapide et compréhensible à des statistiques clés sur la population et les ménages.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


    elif question == "Comment sont collectées les données ?":
        st.info("""
        Les données sont collectées par des enquêteurs sur le terrain via des formulaires, puis 
        centralisées et traitées par le HCP. Elles sont ensuite structurées dans des fichiers Excel analysés ici.
        """)
    elif question == "Comment puis-je vous contacter si ma question n'apparaît pas dans la FAQ ?":
        st.markdown("""
        <div style="background-color:#f0f2f6; padding:10px; border-radius:5px;">
            \U0001F4E7 Vous pouvez me contacter par email : 
            <a href="mailto:hadilbarzani@esi.ac.ma">hadilbarzani@esi.ac.ma</a><br>
            Ou \U0001F4DE par téléphone : 
            <a href="tel:+212767960379">+212 7 67 96 03 79</a>
        </div>
        """, unsafe_allow_html=True)

# === PAGE: STATISTIQUES 0 ===
elif st.session_state.menu == "Statistiques":
    st.title("Statistiques")
    st.markdown("""
    <div class="stats-container">
        <div class="stats-box" >
            <h2>Population</h2>
            <p>
                 Dans cette section, vous pouvez consulter les <strong>principales statistiques démographiques, éducatives et sur l'emploi</strong> 
            du RGPH 2024, ainsi que des interprétations qui aident à mieux comprendre la population marocaine.
            </p>
        </div>
        <div class="stats-box">
            <h2>Ménage</h2>
            <p>
                Cette section présente les données liées aux <strong>logements et conditions de vie</strong> : 
                type de logement, confort, infrastructures, densité, accès aux services... 
                Des indicateurs macro sont interprétés pour mieux comprendre la qualité de vie des ménages.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Voir les statistiques de la Population", key="stat_pop"):
            st.switch_page("pages/Analyse Statistique de la Population.py")  

    with col2:
        if st.button("Voir les statistiques des Ménages", key="stat_menage"):
            st.switch_page("pages/Analyse Statistique des Ménages.py")

# === PAGE: TABLEAU DE POPULATION ===
elif st.session_state.menu == "Tableau de population":
    st.title("Tableau de la population")

    st.markdown("""
    Ce tableau présente les **statistiques détaillées sur la population** issues du RGPH 2024. Les données sont classées selon trois axes :
    - **Milieu de résidence** : Ensemble, Urbain, Rural  
    - **Sexe** : Ensemble, Féminin, Masculin  
    - **Régions** : Les 12 régions administratives du pays, chacune représentée par 3 lignes (une pour chaque milieu), plus 3 lignes supplémentaires représentant le total national réparti par milieu urbain, rural et total général.

    Les indicateurs sont regroupés autour de trois thématiques principales :
    - **Démographie**
    - **Éducation**
    - **Économie / Emploi**

    > \U0001F4A1 Chaque ligne correspond à une combinaison unique : **[Région] × [Milieu de résidence]**
    """, unsafe_allow_html=True)

    with st.expander("\u2139\ufe0f Explication des colonnes (indicateurs disponibles)"):
            st.markdown("""
            Voici les **grandes catégories d'indicateurs** disponibles dans ce tableau, classées selon les thématiques analysées :

            ###  Démographie
            - **Population légale** (dans "ensemble" uniquement)
            - **Population municipale**
            - **Répartition par sexe (%)**
            - **Répartition par âge quinquennal (%)**
            - **Population de 15 ans et plus**
            - **État matrimonial des 15 ans et plus (%)** :
                - Célibataire
                - Marié(e)
                - Divorcé(e)
                - Veuf(ve)
            - **Âge moyen au mariage**
            - **Indicateur conjoncturel de fécondité**
            - **Descendance finale des femmes** (nombre moyen d'enfants par femme)
            - **Taux de prévalence du handicap**

            ###  Éducation
            - **Population de 7-12 ans (%)**
            - **Taux de scolarisation des 6-11 ans (%)**
            - **Population de 10 ans et plus**
            - **Taux d'analphabétisme des 10 ans et plus (%)**
            - **Taux d'analphabétisme des 15 ans et plus (%)**
            - **Population alphabète de 10 ans et plus**
            - **Langues lues et écrites (%)** :
                - Arabe
                - Amazigh (Tifinagh)
                - Anglais
                - Français
            - **Niveau d'études (%)** :
                - Aucun niveau
                - Préscolaire
                - Primaire
                - Secondaire collégial
                - Secondaire qualifiant
                - Supérieur
            - **Langues locales utilisées (%)** :
                - Darija
                - Tachelhit
                - Tamazight
                - Tarifit
                - Hassania

            ### Emploi / Économie
            - **Population de 15 ans et plus**
            - **Population active de 15 ans et plus**
            - **Population inactive de 15 ans et plus**
            - **Taux d'activité des 15 ans et plus (%)**
            - **Taux de chômage (%)**
            - **Population active occupée de 15 ans et plus**
            - **Statut professionnel (%)** :
                - Employeur
                - Indépendant
                - Salarié secteur public
                - Salarié secteur privé
                - Aide familiale
                - Apprenti
                - Coopérateur / Associé
                - Autres

            **NB :** Chaque indicateur est généralement décliné selon le sexe :
            - **Ensemble**
            - **Féminin**
            - **Masculin**
            """)



     # === Définition des intitulés par catégorie ===
    indicateurs = {
        "Démographie": [
            "Population légale", "Population municipale", "Sexe (%)",
            "Âge quinquennal (%)","Population de 15 ans et plus", "État matrimonial des 15 ans et plus",
            "Âge moyen singulier au mariage", "Indicateur conjoncturel de fécondité", "Descendance finale des femmes","Taux de prévalence du handicap (%)"
        ],
        "Éducation": [
            "Population de 7-12 ans", "Taux de scolarisation des 6-11 ans", "Population de 10 ans et plus",
            "Taux d'analphabétisme des 10 ans et plus (%)", "Population de 15 ans et plus","Taux d'analphabétisme des 15 ans et plus (%)",
            "Population alphabète de 10 ans et plus", "Langues lues et écrites",
            "Niveau d'études dans l'enseignement général (%)", "_Langues locales utilisées (non exclusives) (%)"
        ],
        "Emploi": [
            "Population de 15 ans et plus", "Population active de 15 ans et plus",
            "Population inactive de 15 ans et plus", "Taux d'activité des 15 ans et plus",
            "Taux de chômage", "Population active occupée de 15 ans et plus",
            "Statut professionnel des actifs occupés de 15 ans et plus (%)"
        ]
    }

    # === Fonction de filtrage des colonnes ===
    def filtrer_colonnes_par_theme(colonnes, theme_selectionne, sexe_selectionne):
        colonnes_de_base = ["Code_geographique", "Collectivites_territoriales", "Milieu"]  # <-- Use only "Milieu" if "Région" does not exist

        # Sélection des colonnes de sexe
        if sexe_selectionne == "Tous":
            colonnes_sexe = [col for col in colonnes if col.startswith("Sexe :")]
        else:
            prefix = f"Sexe : {sexe_selectionne}"
            colonnes_sexe = [col for col in colonnes if col.startswith(prefix)]

        # Filtrage par thème
        if theme_selectionne == "Toutes":
            colonnes_theme = colonnes_sexe
        else:
            mots_cles = indicateurs[theme_selectionne]
            colonnes_theme = [col for col in colonnes_sexe if any(ind in col for ind in mots_cles)]

        return colonnes_de_base + colonnes_theme

    # === Filtres de sélection utilisateur ===
    with st.container():
        st.markdown("<h3 class='subtitle' >Filtres</h3>", unsafe_allow_html=True)

        filtre_milieu = st.selectbox("Filtrer par milieu de résidence", ["Tous", "Ensemble", "Urbain", "Rural"])
        filtre_sexe = st.selectbox("Filtrer par sexe", ["Tous", "Ensemble", "Masculin", "Féminin"])
        filtre_theme = st.selectbox("Filtrer par catégorie", ["Toutes", "Démographie", "Éducation", "Emploi"])

    # === Chargement des données ===
    df_pop = data["Population"]

    if filtre_milieu != "Tous":
        df_pop = df_pop[df_pop["Milieu"] == filtre_milieu]

    colonnes_finales = filtrer_colonnes_par_theme(df_pop.columns.tolist(), filtre_theme, filtre_sexe)
    df_affiche = df_pop[colonnes_finales]

    # === Affichage du tableau filtré ===
    st.dataframe(df_affiche, use_container_width=True)


# === PAGE: TABLEAU DE MÉNAGE ===
elif st.session_state.menu == "Tableau de ménage":
    st.title("Tableau de ménage")

    st.markdown("""
    Ce tableau présente les **statistiques détaillées sur les ménages et les conditions de logement**, issues du RGPH 2024.
    Les données sont classées selon deux axes principaux :
    
    - **Milieu de résidence** : Ensemble, Urbain, Rural  
    - **Régions** : tous,Les 12 régions administratives, chacune représentée par 3 lignes (une par milieu), plus 3 lignes supplémentaires représentant le total national réparti par milieu urbain, rural et total général.

    Les indicateurs sont regroupés autour de cinq thématiques :
    
    -  **Informations de base**
    -  **Type de logement**
    -  **Conditions de vie**
    -  **Infrastructures & environnement**

    > \U0001F4A1 Chaque ligne correspond à une combinaison unique : **[Région] × [Milieu de résidence]**
    """, unsafe_allow_html=True)

    with st.expander("\u2139\ufe0f Explication des colonnes (indicateurs disponibles)"):
        st.markdown("""
        Voici les **grandes catégories d'indicateurs** disponibles dans ce tableau :

        ### Informations de base
        - **Population municipale**
        - **Nombre de ménages**
        - **Taille moyenne des ménages**
        - **Nombre de ménages sédentaires**

        ### Type de logement (%)
        - Villa / étage de villa
        - Appartement
        - Maison marocaine
        - Maison sommaire / bidonville
        - Logement rural
        - Autre

        ### Conditions de vie
        - **Nombre moyen de personnes par pièce**
        - **Statut d'occupation (%)** :
            - Propriétaire
            - Locataire
            - Autre
        - **Âge du logement (%)** :
            - Moins de 10 ans
            - 10–19 ans
            - 20–49 ans
            - 50 ans ou plus

        - **Disponibilité des éléments essentiels de confort (%)** :
            - Cuisine
            - W.C
            - Pièce d'eau
            - Électricité
            - Eau courante

        ### Infrastructures & environnement
        - **Évacuation des eaux usées (%)** :
            - Réseau public
            - Fosse septique
            - Autre
        - **Évacuation des déchets ménagers (%)** :
            - Bac à ordures communal
            - Camion communal / privé
            - Nature
            - Autres
        - **Combustible utilisé pour la cuisson (%)** :
            - Électricité
            - Gaz
            - Charbon
            - Bois énergie
            - Autre
        - **Distance moyenne au goudron (km)**
        """)

    # === Définition des intitulés par catégorie ménage ===
    categories_menage = {
        "Informations de base": [
            "Population municipale", "Ménages population", "Taille moyenne des ménages", "Ménages sédentaires"
        ],
        "Type de logement (%)": [
            # On ne liste pas ici car on va utiliser le préfixe commun dans le filtre
        ],
        "Conditions de vie": [
            "Nombre moyen de personnes par pièce", "Statut d'occupation du logement (%)", "Âge du logement (%)", "Disponibilité des éléments essentiels de confort (%)"
        ],
        "Infrastructures & environnement": [
            "Mode d'évacuation des eaux usées (%)", "Mode d'évacuation des déchets ménagers (%)", "Combustible de cuisson utilisé (%)", "Distance moyenne des logements à la route goudronnée (Km)"
        ]
    }

    # === Fonction de filtrage des colonnes pour ménage ===
    def filtrer_colonnes_menage(colonnes, categorie_selectionnee):
        colonnes_de_base = ["Code_geographique", "Collectivites_territoriales", "Milieu"]
        
        if categorie_selectionnee == "Toutes":
            colonnes_filtrees = [col for col in colonnes if col not in colonnes_de_base]
        
        elif categorie_selectionnee == "Type de logement (%)":
            # On filtre toutes les colonnes qui commencent par ce préfixe
            colonnes_filtrees = [col for col in colonnes if col.startswith("Type de logement (%)")]
        
        else:
            mots_cles = categories_menage[categorie_selectionnee]
            colonnes_filtrees = [col for col in colonnes if any(mot_cle in col for mot_cle in mots_cles)]
        
        return colonnes_de_base + colonnes_filtrees

    # === Filtres dans l'interface utilisateur ===
    with st.container():
        st.markdown("<h3 class='subtitle'>Filtres Ménages</h3>", unsafe_allow_html=True)

        filtre_milieu_menage = st.selectbox("Filtrer par milieu de résidence", ["Tous", "Ensemble", "Urbain", "Rural"], key="milieu_menage")
        filtre_categorie_menage = st.selectbox("Filtrer par catégorie", ["Toutes"] + list(categories_menage.keys()), key="categorie_menage")

    # === Chargement des données ménage ===
    df_menage = data["Menage"]  

    if filtre_milieu_menage != "Tous":
        df_menage = df_menage[df_menage["Milieu"] == filtre_milieu_menage]

    # Filtrage des colonnes selon la catégorie sélectionnée
    colonnes_finales_menage = filtrer_colonnes_menage(df_menage.columns.tolist(), filtre_categorie_menage)

    # DataFrame final filtré
    df_menage_affiche = df_menage[colonnes_finales_menage]

    # === Affichage du tableau ménage filtré ===
    st.dataframe(df_menage_affiche, use_container_width=True)

# --- Pied de page ---
st.markdown("""
    <div class="footer">
        © 2025 – Dashboard RGPH 2024 | <span>Projet encadré par le HCP • Réalisé par une stagiaire de l'ESI</span>|<strong> Hadil BARZANI </strong> 
    </div>
""", unsafe_allow_html=True)



