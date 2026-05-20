import streamlit as st
import pandas as pd
import base64
import plotly.graph_objects as go
import plotly.express as px



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
    /*page statistiques*/
    /*carte*/
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
         

        .ensemble-card {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .milieu-line {
            display: flex;
            justify-content: space-between;
            gap: 40px;
            margin-top: 20px;
        }
        .card {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 12px;
            width: 280px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .card h3 {
            margin: 0;
            color: #333;
        }
        .card p {
            margin: 0.3rem 0;
            font-size: 16px;
        }
    

        
      
            </style>
""", unsafe_allow_html=True)

# --- Configuration Streamlit ---
st.set_page_config(page_title="Dashboard RGPH 2024", layout="wide")

# Responsive styles for smaller screens
st.markdown("""
    <style>
        @media (max-width: 900px) {
            .ensemble-card, .milieu-line {
                flex-direction: column !important;
                gap: 12px !important;
                align-items: center;
            }
            .card {
                width: 100% !important;
                max-width: 420px;
                margin: 0 auto;
            }
            .custom-header {
                flex-direction: column !important;
                gap: 8px !important;
                text-align: center;
            }
            .custom-header img { height: 50px; }
            img { max-width: 100%; height: auto; }
            .section-title, .subtitle { text-align: center; }
        }
    </style>
""", unsafe_allow_html=True)

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

# --- Bouton retour ---
if st.button("🔙 Retour"):
    st.query_params["menu"] = "Statistiques"
    st.switch_page("main.py")
# === PAGE: STATISTIQUES population 2===

# --- Titre de la page ---
st.title("Analyse Statistique des Ménages")
# --- Filtrage des données nationales ---
df_total = data["Menage"]
df_national = df_total[df_total["Code_geographique"] == 0]


# --- Sélecteur de partie ---
choix_partie = st.sidebar.selectbox(
"Choisir une partie à explorer :",
[
    "Nombre de ménages et ménages sédentaires par milieu",
    "Type de logement par Milieu",
    "Taille moyenne de ménage par Milieu",
    "Statut occupationnel des chefs de ménage par Milieu",
    "Comparaison de la disponibilité des éléments de confort : Urbain vs Rural",
    "Infrastructure & environnement des ménages"
    
]
)


# ====================================
# --- PARTIE 1 : Nombre de Ménages par Milieu
# ====================================
if choix_partie == "Nombre de ménages et ménages sédentaires par milieu":
    # -- Interprétation  --
    with st.expander(" Interprétation-Nombre de Ménages et Ménages Sédentaires par Milieu"):

        st.markdown("""
        ### Interprétation clés sur la population et les ménages sédentaires

        - **Population totale importante** avec **9 275 038 ménages** recensés dans l’ensemble du pays.
        - La majorité des ménages résident en **milieu urbain** :  
        - **6 173 930 ménages urbains**, dont **99,9 %** sont sédentaires,  
            ce qui montre une forte stabilité et un ancrage important dans les villes.
        - En revanche, le **milieu rural**, malgré un nombre total de ménages plus élevé (**13 569 389**), connaît une forte mobilité :  
        - Seulement **22,8 %** des ménages ruraux sont sédentaires (**3 096 474 ménages sédentaires**).  
        - Cela révèle que la majorité des ménages ruraux sont mobiles ou n’ont pas de résidence fixe.

        ### **Conclusion :**  
        La population est largement concentrée en zones urbaines où la sédentarité est quasi totale, tandis que dans les zones rurales, une grande partie des ménages reste mobile. Cette différence souligne les besoins spécifiques en logement et services entre urbain et rural.
        """)
    # === visualisation ===
    milieux = ["Ensemble", "Urbain", "Rural"]
    menages = []
    sedentaires = []
    taux_sedentaires = []

    for milieu in milieux:
        df_m = df_national[df_national["Milieu"] == milieu]
        total_menage = int(df_m["Ménages_Ménages population"].values[0])
        menage_sedentaire = int(df_m["Ménages sédentaires"].values[0])
        
        menages.append(total_menage)
        sedentaires.append(menage_sedentaire)
        
        taux = (menage_sedentaire / total_menage) * 100 if total_menage != 0 else 0
        taux_sedentaires.append(taux)

    st.markdown(f"""
    <div class="ensemble-card">
        <div class="card">
            <h3>{milieux[0]}</h3>
            <p><strong>Ménages :</strong><br> { "{:,}".format(menages[0]).replace(",", " ") }</p>
            <p><strong>Ménages sédentaires :</strong><br> { "{:,}".format(sedentaires[0]).replace(",", " ") }</p>
            <p><strong>Taux de sédentarité :</strong><br> {taux_sedentaires[0]:.1f}%</p>
        </div>
    </div>
""", unsafe_allow_html=True)
    # --- Affichage des cartes pour Urbain et Rural ---
    st.markdown(f"""
    <div class="milieu-line">
        <div class="card">
            <h3>{milieux[1]}</h3>
            <p><strong>Ménages :</strong><br> { "{:,}".format(menages[1]).replace(",", " ") }</p>
            <p><strong>Ménages sédentaires :</strong><br> { "{:,}".format(sedentaires[1]).replace(",", " ") }</p>
            <p><strong>Taux de sédentarité :</strong><br> {taux_sedentaires[1]:.1f}%</p>
        </div>
        <div class="card">
            <h3>{milieux[2]}</h3>
            <p><strong>Ménages :</strong><br> { "{:,}".format(menages[2]).replace(",", " ") }</p>
            <p><strong>Ménages sédentaires :</strong><br> { "{:,}".format(sedentaires[2]).replace(",", " ") }</p>
            <p><strong>Taux de sédentarité :</strong><br> {taux_sedentaires[2]:.1f}%</p>
        </div>
    </div>
""", unsafe_allow_html=True)
    # ====================================
# --- PARTIE 2 : Type de logement par Milieu
# ====================================
if choix_partie == "Type de logement par Milieu":
    # -- Interprétation  --
    with st.expander(" Interprétation-Type de logement par Milieu"):
        st.markdown("""
        Cette visualisation présente la répartition des types de logement dans les milieux urbain et rural. Elle met en évidence les formes d’habitat dominantes, en soulignant la prédominance des maisons marocaines en zone urbaine, ainsi que la diversité des logements ruraux. Les pourcentages indiquent la part relative de chaque type de logement, permettant une compréhension claire des différences entre ces deux contextes de vie.
        ### 1. En milieu urbain
        - **Maison marocaine (77%)** :  
        La majorité des logements en milieu urbain sont des maisons marocaines, ce qui signifie que 77% des habitants urbains vivent dans ce type de logement traditionnel ou classique.  
        - **Appartement (16%)** :  
        Un pourcentage plus faible, 16%, vit en appartement, ce qui indique que les appartements sont moins fréquents que les maisons marocaines dans la zone urbaine.  
        - **Autres types de logement (7%)** :  
        Les autres types de logement, tels que les logements collectifs, immeubles modernes ou autres formes d’habitation, représentent une faible part, soit environ 7% des logements urbains.

        ### 2. **En milieu rural**
        - **Logement rural (45%)** :  
        Le logement rural est le type le plus représenté, avec 45%, correspondant probablement à des habitations typiques adaptées au contexte rural.  
        - **Maison marocaine (39%)** :  
        Les maisons marocaines constituent également une part importante avec 39%, montrant la présence de constructions traditionnelles dans les zones rurales.  
        - **Autres types de logement (16%)** :  
        Les autres formes de logement rural, qui peuvent inclure des habitats précaires, constructions temporaires ou autres types spécifiques, représentent une proportion plus faible de 16%.
        """)
    # === visualisation === 
    df_rural = df_total[df_total["Milieu"] == "Rural"]
    df_urbain = df_total[df_total["Milieu"] == "Urbain"]
    #st.write("Colonnes disponibles :", df_urbain.columns.tolist())
    types_logement_cols = [col for col in df_total.columns if "Type de logement (%)" in col]

    types_logement_labels = [col.replace("Type de logement (%)_", "") for col in types_logement_cols]

    urbain_vals = [df_urbain[col].mean() for col in types_logement_cols]
    rural_vals = [df_rural[col].mean() for col in types_logement_cols]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=types_logement_labels,
        y=urbain_vals,
        name='Urbain',
        marker_color='royalblue'
    ))

    fig.add_trace(go.Bar(
        x=types_logement_labels,
        y=rural_vals,
        name='Rural',
        marker_color='orange'
    ))

    fig.update_layout(
        barmode='stack',
        title="Répartition des types de logement : Urbain vs Rural",
        xaxis_title="Type de logement",
        yaxis_title="Pourcentage (%)",
        xaxis_tickangle=-45,
        legend_title="Milieu",
        height=500,
        width=800
    )

    st.plotly_chart(fig)
# ====================================
# --- PARTIE 3 : Taille myenne de ménage par Milieu
# ====================================
if choix_partie == "Taille moyenne de ménage par Milieu":

    # -- Interprétation  --
    with st.expander(" Interprétation - Taille moyenne de ménage par Milieu"):
        st.markdown("""
        Cette visualisation met en contraste la taille moyenne des ménages entre les **zones urbaines** et **rurales**, et révèle plusieurs éléments clés :

        ### 1. **Comparaison des tailles moyennes** :
        - Les ménages **ruraux** ont une taille moyenne **supérieure** à ceux des **zones urbaines**.
        - Cela se reflète dans la médiane plus élevée pour le rural (~4.4) contre une médiane légèrement inférieure en urbain (~3.8).

        ### 2. **Dispersion des données** :
        - La **variabilité** est plus importante en **rural**, indiquée par une boîte plus grande et des moustaches plus longues. Cela signifie que les tailles de ménage varient plus d’un foyer à un autre.
        - En **urbain**, la taille des ménages est plus **homogène**.

        ### 3. **Présence d’anomalies (outliers)** :
        - On observe des **valeurs aberrantes** dans les deux milieux, notamment :
            - En rural : un ménage avec une taille exceptionnellement élevée (~4.9) et un autre très faible (~2.6).
            - En urbain : des tailles de ménage légèrement supérieures ou inférieures à la moyenne (~4.3 et ~3.6).
        - Ces anomalies peuvent signaler :
            - Des foyers très étendus (familles élargies en milieu rural).
            - Des foyers réduits (personnes seules ou couples sans enfants en zone urbaine).

        ### 4. **Structure familiale implicite** :
        - Le milieu rural semble favoriser les **structures familiales plus étendues**, potentiellement intergénérationnelles.
        - En milieu urbain, les familles tendent à être **plus nucléaires**, voire réduites, probablement à cause de la densité, du coût de la vie et des modes de vie plus individualisés.

        ### **Conclusion** :  
        La différence notable de la taille moyenne des ménages entre milieux urbain et rural **n’est pas une coïncidence** : elle reflète des **dynamiques socioculturelles**, **économiques** et **habitationnelles**. Ce genre de visualisation permet non seulement une **comparaison statistique**, mais aussi une lecture plus **qualitative** de la société.
        """)

    # === visualisation ===

    # Préparation des données pour le boxplot
    df_box = df_total[df_total["Milieu"].isin(["Urbain", "Rural"])]
    #==visualisation==
    fig = px.box(
        df_box,
        x="Milieu",
        y="Taille moyenne des ménages_Taille moyenne",
        points="all",
        color="Milieu",
        title="Taille moyenne des ménages Urbain vs Rural"
    )
    fig.update_layout(
        width=1200,
        height=500,
        xaxis_title="Milieu",
        yaxis_title="Taille moyenne",
        font=dict(size=11)
    )

    st.plotly_chart(fig, use_container_width=False)
# ====================================
# --- PARTIE 4 : Statut occupationnel des chefs de ménage par Milieu
# ====================================
if choix_partie == "Statut occupationnel des chefs de ménage par Milieu":
    # -- Interprétation  --  
    with st.expander(" Interprétation - Statut occupationnel des chefs de ménage par Milieu"):
        st.markdown("""
        Ce graphique compare les statuts d’occupation du logement entre les populations **urbaines** et **rurales**, répartis en trois catégories : **Propriétaire**, **Locataire** et **Autre**.on peut en déduire :

        ### 1.  Propriété dominante en milieu rural
        - En **zone rurale**, plus de **85 %** des ménages sont **propriétaires** de leur logement.
        - Ce chiffre est significativement plus élevé qu’en **zone urbaine**, où environ **61.5 %** des ménages sont propriétaires.
        - Cela reflète une **accessibilité accrue au foncier** dans les zones rurales, où les coûts d’acquisition sont généralement plus faibles, et la propriété souvent transmise de génération en génération.

        ### 2. La location, phénomène urbain
        - En **milieu urbain**, près de **28 %** des ménages sont **locataires**, contre seulement **3.2 %** en milieu rural.
        - Cela peut s’expliquer par :
            - Des prix immobiliers plus élevés en ville, rendant l’achat moins accessible.
            - Une plus grande **mobilité résidentielle** (étudiants, travailleurs temporaires, etc.).
            - Une offre locative plus développée et adaptée à des ménages de passage ou plus petits.

        ### 3.  Catégorie “Autre” stable mais marginale
        - La part des statuts d’occupation classés comme **"Autre"** (hébergement gratuit, logement de fonction, etc.) est **faible** mais **relativement similaire** dans les deux milieux (~10.5–11.5 %).
        - Cela peut concerner des situations spécifiques : familles élargies hébergeant des proches, fonctionnaires logés, ou encore des situations informelles de logement.

        ### Conclusion
        Le statut d’occupation du logement reflète des **inégalités territoriales** :
        - En **rural**, la propriété est la norme, souvent liée à des dynamiques familiales, culturelles et économiques locales.
        - En **urbain**, la diversité des statuts d’occupation illustre la **complexité du marché immobilier**, les **contraintes financières**, mais aussi la **fluidité des parcours de vie**.
        Cette visualisation permet de mieux comprendre les **habitudes résidentielles** et les **besoins en logement** selon le milieu de résidence.""")  

    # === visualisation ===
 
 
    # Colonnes pour statut d'occupation
    statut_cols = [col for col in df_national.columns if col.startswith("Statut d'occupation du logement (%)_")]

    statut_labels = [col.replace("Statut d'occupation du logement (%)_", "") for col in statut_cols]

    # Filtrer par milieu
    df_urbain = df_national[df_national["Milieu"] == "Urbain"]
    df_rural = df_national[df_national["Milieu"] == "Rural"]

    # Calculer moyennes
    urbain_vals = [df_urbain[col].mean() for col in statut_cols]
    rural_vals = [df_rural[col].mean() for col in statut_cols]

    # Création du graphique
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=statut_labels,
        y=urbain_vals,
        name='Urbain',
        marker_color='royalblue'
    ))

    fig.add_trace(go.Bar(
        x=statut_labels,
        y=rural_vals,
        name='Rural',
        marker_color='orange'
    ))

    fig.update_layout(
        barmode='group',
        title="Statut d'occupation du logement : Urbain vs Rural",
        xaxis_title="Statut d'occupation",
        yaxis_title="Pourcentage (%)",
        xaxis_tickangle=-45,
        legend_title="Milieu",
        height=500,
        width=800
    )

    st.plotly_chart(fig)
        
# ====================================
# --- PARTIE 5: comparaison de la disponibilité des éléments de confort : Urbain vs Rural
# ====================================
if choix_partie == "Comparaison de la disponibilité des éléments de confort : Urbain vs Rural":

    # -- Interprétation  --
    with st.expander(" Interprétation - Comparaison de la disponibilité des éléments de confort : Urbain vs Rural"):
        st.markdown("""
        Ce graphique compare l’accès aux équipements de confort de base entre les milieux **urbain** et **rural**, en s’intéressant à cinq éléments clés : **Cuisine, W.-C., Pièce d’eau, Électricité**, et **Eau courante**. Voici les points saillants de cette comparaison :

        ### 1.  Un accès globalement élevé en milieu urbain
        - Les ménages **urbains** bénéficient d’un accès **quasi généralisé** à tous les équipements de confort :
            - **Cuisine**, **W.C.**, **Électricité**, et **Eau courante** dépassent tous **93 %** de disponibilité.
        - Cela traduit un **niveau élevé d’équipement standardisé**, souvent garanti par la réglementation en logement urbain et l’accès aux réseaux publics.

        ### 2.  Des écarts marqués dans le rural, surtout pour l’eau et la salle d’eau
        - En **rural**, on observe un **déficit important** sur certains éléments :
            - **Eau courante** : seulement environ **55 %** des ménages y ont accès, contre **97 %** en urbain.
            - **Pièce d’eau** : autour de **41 %** de disponibilité, bien en dessous du niveau urbain (~75 %).
        - Ces chiffres témoignent d’un **retard d’équipement** ou d’un **mode de vie encore partiellement traditionnel**, parfois en dehors des standards d’urbanisation.

        ### 3.  L’électricité et les sanitaires mieux diffusés
        - L’**électricité** et les **W.-C.** sont relativement bien présents même en **milieu rural** (près de **90–95 %**).
        - Cela montre que certains **services de base** ont été largement étendus, même si d’autres éléments essentiels restent inégalement accessibles.

        ### 4.  Implications sociales et sanitaires
        - Le manque d’accès à une **pièce d’eau** ou à **l’eau courante** en zone rurale soulève des **enjeux de santé publique**, d’hygiène et de **dignité de vie**.
        - Ces disparités renforcent le **sentiment d’exclusion ou de marginalisation** des territoires ruraux par rapport aux standards de vie urbains.

        ### Conclusion
        Cette visualisation révèle une **inégalité persistante** dans l’accès aux équipements essentiels entre villes et campagnes.  
        Alors que l’urbain incarne un **modèle d’habitat moderne et bien équipé**, le rural affiche encore des **déficits d’infrastructure**, notamment en ce qui concerne l’eau et l’hygiène.
        """)
    
    # === visualisation ===



    # Colonnes confort
    confort_cols = [
        "Disponibilité des éléments essentiels de confort (%)_Cuisine",
        "Disponibilité des éléments essentiels de confort (%)_W.-C.",
        "Disponibilité des éléments essentiels de confort (%)_Pièce d'eau",
        "Disponibilité des éléments essentiels de confort (%)_Électricité",
        "Disponibilité des éléments essentiels de confort (%)_Eau courante"
    ]


    confort_labels = [col.replace("Disponibilité des éléments essentiels de confort (%)_", "") for col in confort_cols]

    # Filtrer selon milieu
    df_urbain = df_national[df_national["Milieu"] == "Urbain"]
    df_rural = df_national[df_national["Milieu"] == "Rural"]

    # Moyennes des colonnes pour chaque milieu
    urbain_vals = [df_urbain[col].mean() for col in confort_cols]
    rural_vals = [df_rural[col].mean() for col in confort_cols]

    # Création du graphique
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=confort_labels,
        y=urbain_vals,
        name='Urbain',
        marker_color='royalblue'
    ))

    fig.add_trace(go.Bar(
        x=confort_labels,
        y=rural_vals,
        name='Rural',
        marker_color='orange'
    ))

    fig.update_layout(
        barmode='group',  
        title="Disponibilité des éléments essentiels de confort : Urbain vs Rural",
        xaxis_title="Éléments de confort",
        yaxis_title="Pourcentage (%)",
        xaxis_tickangle=-45,
        legend_title="Milieu",
        height=500,
        width=900
    )
    st.plotly_chart(fig)      


# ====================================
# --- PARTIE 6 : Infrastructure & environnement
# ====================================
if choix_partie == "Infrastructure & environnement des ménages":
    # -- Interprétation  --  
    with st.expander(" Interprétation - Infrastructure & environnement"):
        st.markdown("""
        Ce graphique compare différents indicateurs d'infrastructure et d’environnement entre les milieux **urbain** et **rural** à l’aide de bulles proportionnelles à la fréquence (ou proportion).

        ### 1. Milieu Urbain
        - **Très bonne couverture en infrastructures modernes :**
        - **Réseau d’assainissement**, **bac à ordures commune**, et **gaz** ont des bulles très grandes.
        - **Peu d’utilisation d’alternatives rudimentaires :**
        - Faible proportion pour **fosses septiques**, **déchets dans la nature**, **charbon**, **bois énergie**, etc.


        ### 2. Milieu Rural
        - **Infrastructure plus rudimentaire :**
        - Forte utilisation des **fosses septiques**, **autres évacuations eaux/déchets**, **déchets dans la nature**.
        - **Énergie :**
        - **Gaz** et **électricité** sont présents mais en moindre proportion.
        - Usage notable de **bois énergie**.
        - **Transport et accès :**
        - Plus grande distance à une **route goudronnée**, illustrant l’isolement relatif.


        ### Résumé
        Le graphique montre un **clivage clair** entre les milieux urbains et ruraux :
        - Les **urbains** ont accès à des infrastructures modernes et organisées.
        - Les **ruraux** dépendent davantage de solutions locales, rudimentaires ou alternatives.
        """)
    # === visualisation ===
    categories = {
        # Évacuation eaux usées
        "Mode d’évacuation des eaux usées (%)_Réseau public d'assainissement": "Réseau assainissement",
        "Mode d’évacuation des eaux usées (%)_Fosse septique": "Fosse septique",
        "Mode d’évacuation des eaux usées (%)_Autre": "Autre évacuation eaux",
        # Évacuation déchets ménagers
        "Mode d’évacuation des déchets ménagers (%)_Bac à ordures de la commune": "Bac ordures commune",
        "Mode d’évacuation des déchets ménagers (%)_Camion de la commune / Camion privé": "Camion ordures",
        "Mode d’évacuation des déchets ménagers (%)_Dans la nature": "Déchets dans nature",
        "Mode d’évacuation des déchets ménagers (%)_Autre": "Autre évacuation déchets",
        # Combustible de cuisson
        "Combustible de cuisson utilisé (%)_Gaz": "Gaz",
        "Combustible de cuisson utilisé (%)_Électricité": "Électricité",
        "Combustible de cuisson utilisé (%)_Charbon": "Charbon",
        "Combustible de cuisson utilisé (%)_Bois énergie": "Bois énergie",
        "Combustible de cuisson utilisé (%)_Autre": "Autre combustible",
        # Distance moyenne
        "Distance moyenne des logements à la route goudronnée (Km)": "Distance route goudronnée (Km)"
    }

    milieux = ["Urbain", "Rural"]

    data_bulles = []

    # Filter national data (Code_geographique == 0)
    df_national = df_total[df_total["Code_geographique"] == 0]

    for milieu in milieux:
        df_milieu = df_national[df_national["Milieu"] == milieu]
        if df_milieu.empty:
            continue
        
        row = df_milieu.iloc[0]

        for col, label in categories.items():
            if col not in df_milieu.columns:
                continue
            val = pd.to_numeric(row[col], errors='coerce')
            if pd.isna(val):
                continue
            data_bulles.append({
                "Milieu": milieu,
                "Catégorie": label,
                "Valeur": val
            })

    df_bulles = pd.DataFrame(data_bulles)

    

    fig = px.scatter(
        df_bulles,
        x="Catégorie",
        y="Milieu",
        size="Valeur",
        color="Milieu",
        size_max=40,
        title="Comparaison des infrastructures et environnement par Milieu (sans moyenne)",
        labels={"Valeur": "Pourcentage (%) ou Km", "Catégorie": "Indicateur", "Milieu": "Milieu de résidence"},
        hover_data={"Valeur": ':.2f'}
    )

    fig.update_layout(
        yaxis={'categoryorder':'array', 'categoryarray':milieux[::-1]},  # Rural en bas
        xaxis_tickangle=-45,
        height=600,
        width=900
    )

    st.plotly_chart(fig)

