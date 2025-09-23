import streamlit as st
import pandas as pd
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
        /*  couleur du titre principal */
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
#=== Bouton retour au menu principal ; direct à section statistiques ===
if st.button("🔙 Retour "):
    st.query_params["menu"] = "Statistiques"
    st.switch_page("main.py")




# === PAGE: STATISTIQUES population 1===

st.title("Analyse Statistique de la Population")
# --- Filtrage des données nationales ---
df_total = data["Population"]
df_national = df_total[df_total["Code_geographique"] == 0]


# --- Sélecteur de partie ---
choix_partie = st.sidebar.selectbox(
"Choisir une partie à explorer :",
[
    "Population légale & municipale par Milieu",
    "Répartition par sexe et milieu",
    "Répartition urbaine/rurale par région",
    "Indicateurs du marché du travail",
    "Statut professionnel",
    "Analphabétisme",
    "Niveau éducationnel",
    
]
)


# ====================================
# --- PARTIE 1 : Population par Milieu
# ====================================
if choix_partie == "Population légale & municipale par Milieu":
    # -- Interprétation  --   

    with st.expander(" Interprétation-Population légale & municipale par Milieu"):

        st.markdown("""
        ##  Définition des concepts

        - **Population légale** : Il s'agit de l'ensemble des personnes recensées de manière officielle dans une zone, selon les critères nationaux du recensement. Elle inclut toutes les personnes vivant de manière permanente, qu'elles soient enregistrées ou non dans les registres administratifs locaux.

        - **Population municipale** : C'est une sous-catégorie de la population légale, composée uniquement des personnes **enregistrées administrativement** dans une commune, un quartier ou une localité reconnue.

        ###  Pourquoi ces indicateurs sont importants

        - La **population légale** est utilisée pour des décisions à l'échelle nationale : planification budgétaire, sièges au parlement, grands projets d'infrastructure, etc.
        - La **population municipale** est cruciale pour les **services de proximité** : santé, école, sécurité, collecte des ordures, etc.
        - Comprendre la différence entre les deux permet d'identifier les zones **où les citoyens sont mal recensés ou administrativement invisibles**.

        ## Analyse générale

        - La **population urbaine** est presque **deux fois plus élevée** que la population rurale :
            ```python
            ratio_urbain_rural = 23_110_108 / 13_718_222 ≈ 1.68
            ```
            Cela montre un **fort niveau d'urbanisation**, probablement lié à :
            - L'attractivité économique des villes.
            - La migration des jeunes vers les zones urbaines.
            - Une concentration des services et des infrastructures en ville.

        ###  Différences internes : légale vs municipale

        - Dans **chaque milieu (ensemble, urbain, rural)**, on observe un **écart** entre la population légale et municipale.
        - Mais c'est en **milieu urbain** que cet écart est **le plus fort**, avec un **déficit de 811 097 personnes** :
            ```python
            ecart_urbain = 23.110.108 - 22.921.202 = 811.097
            ```

        ###  Raisons potentielles de cet écart urbain

        Plusieurs hypothèses peuvent expliquer ce grand écart :
        - **Mobilité résidentielle élevée** : de nombreuses personnes emménagent en ville sans avoir encore modifié leur enregistrement administratif.
        - **Habitat non déclaré** : logements informels, squats ou quartiers non reconnus officiellement.
        - **Migrants ou personnes non enregistrées volontairement**, parfois par méfiance ou par oubli.
        - **Défaillance ou lenteur dans les procédures administratives** des villes face à l'afflux massif de populations.

        ## Conclusion

        - Le **suivi administratif est plus complexe en milieu urbain**.
        - Cet écart de plus de **800 000 personnes** en ville mérite une attention particulière.
        - Il serait pertinent de compléter cette analyse par une étude **par région**, pour identifier les zones à fort déséquilibre, et ainsi améliorer les politiques publiques.

        """)
    # === visualisation ===
    milieux = ["Ensemble", "Urbain", "Rural"]
    pop_legale, pop_municipale = [], []

    for milieu in milieux:
        df_m = df_national[df_national["Milieu"] == milieu]
        pop_legale.append(int(df_m["Sexe : Ensemble_Population légale"].values[0]))
        pop_municipale.append(int(df_m["Sexe : Ensemble_Population municipale"].values[0]))

    st.markdown(f"""
        <div class="ensemble-card">
            <div class="card">
                <h3>{milieux[0]}</h3>
                <p><strong>Population légale :</strong><br> { "{:,}".format(pop_legale[0]).replace(",", " ") }</p>
                <p><strong>Population municipale :</strong><br> { "{:,}".format(pop_municipale[0]).replace(",", " ") }</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="milieu-line">
            <div class="card">
                <h3>{milieux[1]}</h3>
                <p><strong>Population légale :</strong><br> { "{:,}".format(pop_legale[1]).replace(",", " ") }</p>
                <p><strong>Population municipale :</strong><br> { "{:,}".format(pop_municipale[1]).replace(",", " ") }</p>
            </div>
            <div class="card">
                <h3>{milieux[2]}</h3>
                <p><strong>Population légale :</strong><br> { "{:,}".format(pop_legale[2]).replace(",", " ") }</p>
                <p><strong>Population municipale :</strong><br> { "{:,}".format(pop_municipale[2]).replace(",", " ") }</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# =========================================
# --- PARTIE 2 : Sexe × Milieu (Barplot)
# =========================================
elif choix_partie == "Répartition par sexe et milieu":
    # -- Interprétation  --
    with st.expander(" Interprétation-Répartition par sexe et milieu"):
        st.write("""
        Cette visualisation permet de comprendre la répartition des hommes, des femmes et de la population totale 
        dans les milieux **urbain**, **rural** et **ensemble**. 
                    
        Cela met en évidence d'éventuels déséquilibres de genre selon les zones.
        ###  Observations :
        - Dans **l'ensemble de la population**, les **femmes sont légèrement plus nombreuses** que les hommes, avec un écart proche de **100 000 individus**.
        - Dans le **milieu urbain**, ce déséquilibre persiste aussi en faveur des femmes.
        - En revanche, dans le **milieu rural**, on observe une **légère majorité d'hommes** par rapport aux femmes.

        ###  Hypothèse :
        Ce déséquilibre pourrait s'expliquer par une **préférence des femmes pour les zones urbaines**, où les **conditions de travail sont souvent moins pénibles** que dans les zones rurales, notamment en ce qui concerne l'agriculture ou les travaux physiques.
        
        Il est aussi possible que :
        - Les **femmes migrent plus facilement vers les villes** pour accéder à l'éducation, aux soins ou à des emplois dans les services.
        - Le **travail informel ou domestique urbain** attire davantage une population féminine.
                    
        """)
    # === visualisation ===
    genres = ["Masculin", "Féminin", "Ensemble"]
    couleurs = {
        "Masculin": "#1f4e79",
        "Féminin": "#f0c05a",
        "Ensemble": "#6B0039"
    }
    milieu_labels = ["Ensemble", "Urbain", "Rural"]

    bars = []
    for genre in genres:
        values = []
        for milieu in milieu_labels:
            val = df_national[df_national["Milieu"] == milieu][f"Sexe : {genre}_Population municipale"].values[0]
            values.append(val)
        bars.append(go.Bar(name=genre, x=milieu_labels, y=values, marker_color=couleurs[genre]))

    fig_sexe_milieu = go.Figure(data=bars)
    fig_sexe_milieu.update_layout(barmode='group', height=400, plot_bgcolor='white',
        title='Population municipale par Sexe et Milieu',
        xaxis_title="Milieu", yaxis_title="Population", legend_title="Sexe")

    st.plotly_chart(fig_sexe_milieu, use_container_width=True)


# ===========================================
# --- PARTIE 3 : Population par Région
# ===========================================
elif choix_partie == "Répartition urbaine/rurale par région":
    #-- interprétation --
    with st.expander(" Interprétation-Répartition urbaine/rurale par région"):
        st.write("""
        Cette représentation compare la population municipale **urbaine** et **rurale** dans chaque région du Maroc.  
        Elle permet d'identifier les zones à **forte urbanisation** ou à **dominante rurale**.

        ###  Observations générales :
        - Globalement, la **population urbaine est presque deux fois plus importante** que la population rurale à l'échelle nationale.
        - Dans **presque toutes les régions**, la population **urbaine dépasse la population rurale**.
        - Ce phénomène est particulièrement **marqué dans les régions qui abritent les grandes villes** (comme Casablanca-Settat, Rabat-Salé-Kénitra, Marrakech-Safi, etc.), où l'on observe un **écart net de plusieurs dizaines de milliers d'habitants**, voire bien plus.

        ###  Exception notable :
        - Une seule région présente une situation inversée : la **population rurale y est environ deux fois plus élevée** que la population urbaine.
        - Toutefois, la **population totale de cette région reste relativement modeste**, avec environ **1 643 144 habitants**.
        
        ###  Interprétation :
        Ces données reflètent :
        - Une **forte concentration des activités économiques et des services** dans les grandes agglomérations.
        - Un **exode rural continu** vers les villes à la recherche d'emploi et de meilleures conditions de vie.
        - Des **écarts de développement** importants entre certaines régions du Maroc.
        """)
    # === visualisation ===
    df_regions = df_total[df_total["Code_geographique"] != 0]
    region_map = {
        1: "Tanger-Tétouan-Al Hoceïma", 2: "L'Oriental", 3: "Fès-Meknès", 4: "Rabat-Salé-Kénitra",
        5: "Béni Mellal-Khénifra", 6: "Casablanca-Settat", 7: "Marrakech-Safi", 8: "Drâa-Tafilalet",
        9: "Souss-Massa", 10: "Guelmim-Oued Noun", 11: "Laâyoune-Sakia El Hamra", 12: "Dakhla-Oued Ed Dahab"
    }

    urbains, ruraux, region_names = [], [], []
    for code in sorted(region_map):
        region_data = df_regions[df_regions["Code_geographique"] == code]
        urbains.append(region_data[region_data["Milieu"] == "Urbain"]["Sexe : Ensemble_Population municipale"].values[0])
        ruraux.append(region_data[region_data["Milieu"] == "Rural"]["Sexe : Ensemble_Population municipale"].values[0])
        region_names.append(region_map[code])

    
    urbains.append(df_national[df_national["Milieu"] == "Urbain"]["Sexe : Ensemble_Population municipale"].values[0])
    ruraux.append(df_national[df_national["Milieu"] == "Rural"]["Sexe : Ensemble_Population municipale"].values[0])
    region_names.append("Maroc")

    fig_region = go.Figure(data=[
        go.Bar(name="Urbain", x=region_names, y=urbains, marker_color="#1f4e79"),
        go.Bar(name="Rural", x=region_names, y=ruraux, marker_color="#f0c05a"),
    ])
    fig_region.update_layout(barmode='group', height=500, plot_bgcolor='white',
        title="Population municipale par Région",
        xaxis_title="Région", yaxis_title="Population municipale",
        legend_title="Milieu")

    st.plotly_chart(fig_region, use_container_width=True)
# ===========================================
# --- PARTIE 4 : Indicateurs du marché du travail
# ===========================================
elif choix_partie == "Indicateurs du marché du travail":
    # -- Interprétation  --
    with st.expander(" Interprétation – Activité et Chômage"):
        st.markdown("""
        Cette section analyse la **population active**, la **population inactive**, ainsi que les **taux d'activité** et **de chômage** pour les personnes âgées de **15 ans et plus**, selon le milieu de résidence (**ensemble**, **urbain**, **rural**).

        ###  Observations basées sur les données :
        - Le **taux d'activité** est le plus élevé en **milieu urbain** (43.8 %), suivi du niveau **national** (41.6 %), puis du **milieu rural** (37.6 %). Contrairement à ce qu'on observe parfois, **le milieu urbain présente ici une plus forte participation économique**, probablement liée à une meilleure offre d'emploi ou à un accès facilité aux opportunités.
        - Le **taux de chômage** est élevé dans les **trois milieux**, dépassant les **21 %**, avec une très faible variation : 21.2 % en urbain, 21.4 % en rural et 21.3 % au niveau national. Cela montre une **tension généralisée sur le marché du travail**, indépendamment du milieu de résidence.
        - La **population inactive** est particulièrement importante en **zone urbaine** (plus de 9,6 millions), ce qui peut s'expliquer par :
            - la poursuite des études,
            - le travail domestique non rémunéré,
            - ou le découragement face au marché du travail urbain très compétitif.

        ###  Remarques et interprétations :
        - Un **taux d'activité élevé** traduit une meilleure intégration de la population dans les circuits économiques.
        - Un **taux de chômage élevé dans tous les milieux** souligne une **problématique structurelle** du marché de l'emploi.
        - L'écart entre **population active** et **inactive** reste important, ce qui montre **un fort réservoir de main-d'œuvre** non mobilisé, notamment en milieu urbain.
        """)
    # === visualisation ===
    # Milieux
    milieux = ["Ensemble", "Urbain", "Rural"]

    # Initialisation des listes
    taux_chomage, pop_active, pop_inactive, taux_activite = [], [], [], []

    for milieu in milieux:
        df_m = df_national[df_national["Milieu"] == milieu]
        taux_chomage.append(float(df_m["Sexe : Ensemble_Taux de chômage (%)"].values[0]))
        pop_active.append(int(df_m["Sexe : Ensemble_Population active de 15 ans et plus"].values[0]))
        pop_inactive.append(int(df_m["Sexe : Ensemble_Population inactive de 15 ans et plus"].values[0]))
        taux_activite.append(float(df_m["Sexe : Ensemble_Taux d'activité des 15 ans et plus (%)"].values[0]))

    # Carte centrale : Ensemble
    st.markdown(f"""
        <div class="ensemble-card">
            <div class="card">
                <h3>{milieux[0]}</h3>
                <p><strong>Taux d'activité :</strong><br> {taux_activite[0]:.1f} %</p>
                <p><strong>Taux de chômage :</strong><br> {taux_chomage[0]:.1f} %</p>
                <p><strong>Population active :</strong><br> { "{:,}".format(pop_active[0]).replace(",", " ") }</p>
                <p><strong>Population inactive :</strong><br> { "{:,}".format(pop_inactive[0]).replace(",", " ") }</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Cartes : Urbain & Rural
    st.markdown(f"""
        <div class="milieu-line">
            <div class="card">
                <h3>{milieux[1]}</h3>
                <p><strong>Taux d'activité :</strong><br> {taux_activite[1]:.1f} %</p>
                <p><strong>Taux de chômage :</strong><br> {taux_chomage[1]:.1f} %</p>
                <p><strong>Population active :</strong><br> { "{:,}".format(pop_active[1]).replace(",", " ") }</p>
                <p><strong>Population inactive :</strong><br> { "{:,}".format(pop_inactive[1]).replace(",", " ") }</p>
            </div>
            <div class="card">
                <h3>{milieux[2]}</h3>
                <p><strong>Taux d'activité :</strong><br> {taux_activite[2]:.1f} %</p>
                <p><strong>Taux de chômage :</strong><br> {taux_chomage[2]:.1f} %</p>
                <p><strong>Population active :</strong><br> { "{:,}".format(pop_active[2]).replace(",", " ") }</p>
                <p><strong>Population inactive :</strong><br> { "{:,}".format(pop_inactive[2]).replace(",", " ") }</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ===========================================
# --- PARTIE 5 : Statut professionnel
# ===========================================
elif choix_partie == "Statut professionnel":

    # -- Interprétation  --
    with st.expander(" Interprétation – Statuts professionnels des actifs occupés"):
        st.markdown("""
        Cette visualisation montre la répartition des **actifs occupés âgés de 15 ans et plus** selon leur **statut professionnel**, dans les milieux **urbain** et **rural**.

        ###  Observations :
        - La **forme de la structure professionnelle** (l'ordre des métiers les plus fréquents) est **similaire entre les deux milieux** : on retrouve globalement les **mêmes types de professions dominants**.
        - Cependant, ce sont les **effectifs relatifs** (les pourcentages) qui **diffèrent fortement**.
            - Exemple : le **secteur public** est présent dans les deux milieux, mais il représente **17.6 % en urbain** contre seulement **7.3 % en rural**.
        - Les statuts les plus fréquents restent les mêmes :
            - Le **salariat dans le secteur privé** domine dans les deux cas (**49.2 % urbain** vs **49.3 % rural**).
            - Suivent les **indépendants**, puis les **salariés du secteur public**.

        ### Interprétation :
        - Bien que la **hiérarchie des métiers** soit similaire, leur **poids dans chaque milieu** reflète des **réalités socio-économiques distinctes**.
        - L'urbain est plus marqué par l'emploi **formel (public/privé)**, tandis que le rural affiche une part plus forte d'**indépendants** et d'**aides familiaux**, souvent liés à l'agriculture ou à des activités informelles.
        """)

    # === visualisation ===

    # Colonnes à utiliser
    colonnes_statut = [
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Employeur",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Indépendant",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Salarié du secteur public",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Salarié du secteur privé",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Aide familial",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Apprenti",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Coopérateur/Associé",
        "Sexe : Ensemble_Statut professionnel des actifs occupés de 15 ans et plus (%)_Autre"
    ]

    noms_statut = [
        "Employeur", "Indépendant", "Salarié public", "Salarié privé",
        "Aide familial", "Apprenti", "Coopérateur", "Autre"
    ]

    milieux = ["Ensemble", "Urbain", "Rural"]
    couleurs = ["#2E86C1", "#B62596", "#FBFF0E"]  # couleurs pour chaque milieu

    # Subplots : 1 ligne, 3 colonnes
    fig = make_subplots(rows=1, cols=3, subplot_titles=milieux)

    for i, milieu in enumerate(milieux):
        df_m = df_national[df_national["Milieu"] == milieu]
        valeurs = [float(df_m[col].values[0]) for col in colonnes_statut]

        fig.add_trace(
            go.Bar(
                x=noms_statut,
                y=valeurs,
                marker_color=couleurs[i],
                name=milieu,
                hovertemplate="%{x}<br>%{y:.1f} %<extra></extra>"
            ),
            row=1,
            col=i+1
        )

    fig.update_layout(
        height=500,
        width=1200,
        showlegend=False,
        title_text="Répartition des statuts professionnels des actifs occupés (15 ans+)",
        margin=dict(t=60, b=50),
    )

    fig.update_yaxes(title_text="Pourcentage (%)")

    st.plotly_chart(fig, use_container_width=True)

# ===========================================
# --- PARTIE 6 : Taux d'analphabétisme
# ===========================================
elif choix_partie == "Analphabétisme":
    # -- Interprétation  --
    with st.expander(" Interprétation – Alphabétisation"):
        st.markdown("""
        Cette section présente les **taux d'analphabétisme** pour les personnes de **10 ans et plus** et de **15 ans et plus**, selon le **milieu de résidence** (urbain, rural, ensemble). Elle affiche également la **population alphabétisée** correspondante.

        ###  Observations :
        - En **milieu rural**, le taux d'analphabétisme atteint **38.0 %** chez les 10+ et **43.4 %** chez les 15+, ce qui est **très élevé** et **considéré comme grave** selon les normes internationales (UNESCO).
        - En **milieu urbain**, bien que les taux soient plus bas (**17.3 %** pour les 10+ et **19.3 %** pour les 15+), ils **restent élevés** et préoccupants. Cela signifie qu'un **citadin sur cinq âgé de 15 ans et plus ne sait ni lire ni écrire**.
        - En **total national**, le Maroc affiche **24.8 %** (10+) et **27.9 %** (15+), des chiffres indiquant que **plus d'un quart de la population adulte est analphabète**.

        ### Interprétation :
        - Au Maroc, **le taux d'analphabétisme**, qui approche les 25 %, est considéré comme grave, car il limite l'accès à l'emploi, à l'information, aux services publics et à la participation citoyenne.
        - La **population alphabétisée** reste importante (par exemple, **13,9 millions** de personnes alphabétisées en milieu urbain, 15+), mais l'**écart rural/urbain reste très marqué**.
        - L'analphabétisme est **lié au sous-développement**, à la pauvreté, au genre et à l'accès à l'éducation, particulièrement en milieu rural.

        """)

    # === visualisation ===
    milieux = ["Ensemble", "Urbain", "Rural"]
    taux_analph_10, taux_analph_15 = [], []
    pop_10, pop_15 = [], []
    alpha_10, alpha_15 = [], []

    for milieu in milieux:
        df_m = df_national[df_national["Milieu"] == milieu]
        t10 = float(df_m["Sexe : Ensemble_Taux d'analphabétisme des 10 ans et plus (%)"].values[0])
        t15 = float(df_m["Sexe : Ensemble_Taux d'analphabétisme des 15 ans et plus (%)"].values[0])
        p10 = int(df_m["Sexe : Ensemble_Population de 10 ans et plus"].values[0])
        p15 = int(df_m["Sexe : Ensemble_Population de 15 ans et plus"].values[0])

        taux_analph_10.append(t10)
        taux_analph_15.append(t15)
        pop_10.append(p10)
        pop_15.append(p15)

        alpha_10.append(int(p10 * (1 - t10 / 100)))
        alpha_15.append(int(p15 * (1 - t15 / 100)))

    # Carte centrale : Ensemble
    st.markdown(f"""
        <div class="ensemble-card">
            <div class="card">
                <h3>{milieux[0]}</h3>
                <p><strong>Taux analphabétisme (10+):</strong><br> {taux_analph_10[0]:.1f} %</p>
                <p><strong>Population alphabétisée (10+):</strong><br> { "{:,}".format(alpha_10[0]).replace(",", " ") }</p>
                <p><strong>Taux analphabétisme (15+):</strong><br> {taux_analph_15[0]:.1f} %</p>
                <p><strong>Population alphabétisée (15+):</strong><br> { "{:,}".format(alpha_15[0]).replace(",", " ") }</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="milieu-line">
            <div class="card">
                <h3>{milieux[1]}</h3>
                <p><strong>Taux analphabétisme (10+):</strong><br> {taux_analph_10[1]:.1f} %</p>
                <p><strong>Population alphabétisée (10+):</strong><br> { "{:,}".format(alpha_10[1]).replace(",", " ") }</p>
                <p><strong>Taux analphabétisme (15+):</strong><br> {taux_analph_15[1]:.1f} %</p>
                <p><strong>Population alphabétisée (15+):</strong><br> { "{:,}".format(alpha_15[1]).replace(",", " ") }</p>
            </div>
            <div class="card">
                <h3>{milieux[2]}</h3>
                <p><strong>Taux analphabétisme (10+):</strong><br> {taux_analph_10[2]:.1f} %</p>
                <p><strong>Population alphabétisée (10+):</strong><br> { "{:,}".format(alpha_10[2]).replace(",", " ") }</p>
                <p><strong>Taux analphabétisme (15+):</strong><br> {taux_analph_15[2]:.1f} %</p>
                <p><strong>Population alphabétisée (15+):</strong><br> { "{:,}".format(alpha_15[2]).replace(",", " ") }</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
# ===========================================
# --- PARTIE 7 : Niveau d'éducation
# ===========================================
elif choix_partie == "Niveau éducationnel":
    # -- Interprétation  --
    with st.expander(" Interprétation – Niveau d'éducation"):
        st.markdown("""
        Cette section présente la **répartition des niveaux d'éducation** pour les personnes de **10 ans et plus**, selon le milieu de résidence (urbain, rural, ensemble).

        ###  Observations :
        - Le **niveau d'éducation** est globalement **plus élevé en milieu urbain** qu'en milieu rural.
        - En milieu urbain, on observe une **forte proportion de personnes ayant au moins un niveau secondaire** (collégial ou qualifiant), tandis que le milieu rural reste majoritairement concentré sur l'**enseignement primaire**.
        - Le taux d'**analphabétisme** est également plus élevé en milieu rural, ce qui reflète les **inégalités d'accès à l'éducation**.

        ### Interprétation :
        - Ces données soulignent l'importance de l'**urbanisation dans l'accès à l'éducation**.
        - Elles mettent en évidence la nécessité de politiques ciblées pour améliorer l'accès à l'éducation dans les zones rurales, où les taux d'analphabétisme restent préoccupants.
        """)

    # === visualisation ===
    
    # Colonnes à utiliser
    colonnes_niveau = [
        "Sexe : Ensemble_Niveau d'études dans l'enseignement général (%)_Aucun niveau d'études",
        "Sexe : Ensemble_Niveau d'études dans l'enseignement général (%)_Préscolaire",
        "Sexe : Ensemble_Niveau d'études dans l'enseignement général (%)_Primaire",
        "Sexe : Ensemble_Niveau d'études dans l'enseignement général (%)_Secondaire collégial",
        "Sexe : Ensemble_Niveau d'études dans l'enseignement général (%)_Secondaire qualifiant",
        "Sexe : Ensemble_Niveau d'études dans l'enseignement général (%)_Supérieur"
    ]

    noms_niveau = [
        "Aucun niveau", "Préscolaire", "Primaire", "Secondaire collégial",
        "Secondaire qualifiant", "Supérieur"
    ]

    milieux = ["Ensemble", "Urbain", "Rural"]
    couleurs = ["#2E86C1", "#B62596", "#FBFF0E"]
    # Subplots : 1 ligne, 3 colonnes
    fig = make_subplots(rows=1, cols=3, subplot_titles=milieux)
    for i, milieu in enumerate(milieux):
        df_m = df_national[df_national["Milieu"] == milieu]
        valeurs = [float(df_m[col].values[0]) for col in colonnes_niveau]

        fig.add_trace(
            go.Bar(
                x=noms_niveau,
                y=valeurs,
                marker_color=couleurs[i],
                name=milieu,
                hovertemplate="%{x}<br>%{y:.1f} %<extra></extra>"
            ),
            row=1,
            col=i+1
        )
    fig.update_layout(
        height=500,
        width=1200,
        showlegend=False,
        title_text="Niveau d'éducation des personnes de 10 ans et plus",
        margin=dict(t=60, b=50),
    )
    fig.update_yaxes(title_text="Pourcentage (%)")
    st.plotly_chart(fig, use_container_width=True)


