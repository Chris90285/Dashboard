#-------------------imports-----------------------------
#-------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm

#-------------------data inladen-----------------------
#-------------------------------------------------------
#Main data set
@st.cache_data
def load_data():
    df = pd.read_csv("airline_passenger_satisfaction.csv")
    df["Total Delay"] = df["Departure Delay"].fillna(0) + df["Arrival Delay"].fillna(0)
    return df

df = load_data()

#Extra data set
@st.cache_data
def load_extra_data():
    df_extra = pd.read_csv("airlines_flights_data.csv")
    return df_extra

df_extra = load_extra_data()

#-------------------sidebar-----------------------------
#-------------------------------------------------------
# Zorg dat er altijd een default waarde is
if "stijl" not in st.session_state:
    st.session_state["stijl"] = "KLM Blauw"

with st.sidebar:
    # Huidige stijl bepalen
    huidige_stijl = st.session_state["stijl"]
    primary_color = "royalblue" if huidige_stijl == "KLM Blauw" else "goldenrod"

    # Titel bovenaan
    st.markdown(
        f"<h2 style='color:{primary_color}; margin: 0 0 8px 0;'>KLM Dashboard</h2>",
        unsafe_allow_html=True,
    )

    # Radio button onder de titel
    st.radio("Kies een stijl:", ["KLM Blauw", "Geel"], key="stijl")

    st.markdown("---")

    # overige sidebar-elementen
    page = st.selectbox("Selecteer een pagina", ["Snel Overzicht", "Dashboard", "Data Overzicht", "Werkwijze"])

    # witregel
    st.write("")  

    # Afbeelding
    st.image("Vertrekbord Team HV0009.png", use_container_width=True)

    # witregels
    st.write("") 
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Voeg laatst geupdate datum toe
    st.write("Voor het laatst geupdate op:")
    st.write("*23:39 - 23 sep 2025*")

#-------------------stijlinstellingen-------------------
#-------------------------------------------------------
stijl = st.session_state["stijl"]  # veilige kopie uit session_state

if stijl == "KLM Blauw":
    primary_color = "royalblue"
    secondary_color = "orange"
    gauge_steps = [
        {'range': [0,2], 'color': 'lightcoral'},
        {'range': [2,4], 'color': 'lightyellow'},
        {'range': [4,5], 'color': 'lightgreen'}
    ]
else:  # Geel
    primary_color = "goldenrod"
    secondary_color = "darkorange"
    gauge_steps = [
        {'range': [0,2], 'color': 'orangered'},
        {'range': [2,4], 'color': 'gold'},
        {'range': [4,5], 'color': 'lightyellow'}
    ]

#-------------------page 1-----------------------------
#-------------------------------------------------------
if page == "Snel Overzicht":

    # Titel in thema-kleur
    st.markdown(f"<h1 style='color:{primary_color}'>📊 Snel Overzicht - Klanttevredenheid KLM</h1>", unsafe_allow_html=True)
    st.write("")
    st.markdown("**Welkom!**")
    st.write("Op dit dashboard vind je uitgebreide informatie over de tevredenheid van klanten van KLM.")
    st.write("Gebruik het dropdown menu om de verschillende pagina's te bezoeken.")
    st.write("")
    st.markdown("**Snel overzicht**")
    st.write("Hieronder zijn een aantal simpele KPI's (Key Performance Indicators) te zien.")
    st.write("Klik op de afbeeldingen om ze beter te bekijken.")

    # ======================
    # Dropdown filter: Class
    # ======================
    st.markdown("### Selecteer een klasse")
    class_options = ["Alle Klassen"] + df["Class"].unique().tolist()
    selected_class = st.selectbox("Kies een klasse:", class_options)

    # Pas filter toe op df_filtered
    if selected_class != "Alle Klassen":
        df_filtered = df[df["Class"] == selected_class]
    else:
        df_filtered = df.copy()

    # ======================
    # Extra filtersectie - Afhankelijke sliders
    # ======================
    st.markdown("###  Leeftijdsfilter")
    st.write("Pas hier de minimale en maximale leeftijd aan.")
    st.write("Let op! Zorg dat de maximale leeftijd niet kleiner is dan de minimale leeftijd!")

    col_min, col_max = st.columns(2)
    with col_min:
        min_age = st.slider(
            "Minimum leeftijd",
            int(df_filtered["Age"].min()),
            int(df_filtered["Age"].max()),
            int(df_filtered["Age"].min()),
            key="min_age_slider"
        )
    with col_max:
        max_age = st.slider(
            "Maximum leeftijd",
            int(df_filtered["Age"].min()),
            int(df_filtered["Age"].max()),
            int(df_filtered["Age"].max()),
            key="max_age_slider"
        )

    if min_age > max_age:
        st.warning("⚠️ Minimum leeftijd kan niet groter zijn dan maximum. Waarden zijn aangepast.")
        min_age, max_age = max_age, min_age

    df_filtered = df_filtered[(df_filtered["Age"] >= min_age) & (df_filtered["Age"] <= max_age)]

    # ======================
    # KPI berekeningen
    # ======================
    total_passengers = df_filtered["ID"].nunique()
    satisfaction_cols = [
        "On-board Service", "Seat Comfort", "Leg Room Service", "Cleanliness",
        "Food and Drink", "In-flight Service", "In-flight Wifi Service",
        "In-flight Entertainment", "Baggage Handling"
    ]
    avg_satisfaction = df_filtered[satisfaction_cols].mean().mean()
    avg_dep_delay = df_filtered["Departure Delay"].mean()
    avg_arr_delay = df_filtered["Arrival Delay"].mean()
    delayed_percentage = (df_filtered[df_filtered["Total Delay"] > 15].shape[0] / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0

    # ======================
    # Visualisaties (2x3 grid)
    # ======================
    col1, col2, col5 = st.columns(3)

    with col1:
        fig1 = go.Figure(go.Indicator(
            mode="number",
            value=total_passengers,
            title={"text": "Totaal Passagiers"},
            number={'font': {'color': primary_color}}
        ))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_satisfaction,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Gem. Tevredenheid (0-5)"},
            gauge={
                'axis': {'range': [0, 5]},
                'bar': {'color': primary_color},
                'steps': gauge_steps
            }
        ))
        st.plotly_chart(fig2, use_container_width=True)

    with col5:
        fig5 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=delayed_percentage,
            title={'text': "Vertraagde vluchten (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': secondary_color},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 60], 'color': "lightyellow"},
                    {'range': [60, 100], 'color': "lightcoral"}
                ]
            },
            number={'suffix': "%"}
        ))
        st.plotly_chart(fig5, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_dep_delay,
            title={'text': "Gem. Vertrekvertraging (min)"},
            gauge={'axis': {'range': [0, max(60, avg_dep_delay*2)]}, 'bar': {'color': secondary_color}}
        ))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_arr_delay,
            title={'text': "Gem. Aankomstvertraging (min)"},
            gauge={'axis': {'range': [0, max(60, avg_arr_delay*2)]}, 'bar': {'color': "red"}}
        ))
        st.plotly_chart(fig4, use_container_width=True)

#-------------------page 2-----------------------------
#-------------------------------------------------------
elif page == "Dashboard":
    st.markdown(f"<h1 style='color:{primary_color}'>📊 Dashboard klanttevredenheid KLM</h1>", unsafe_allow_html=True)
    # Witregel
    st.write("")

    # Titel
    st.title("Tevredenheid per klanttype en reisdoel")
    #-------------------Grafiek Chris-------------------------
    #---------------------------------------------------------
    st.markdown("### ✈️ Vertragingfilters")
    delay_30 = st.checkbox("Alleen vertraagde vluchten (>30 minuten vertraging)")
    delay_60 = st.checkbox("Alleen zwaar vertraagde vluchten (>60 minuten vertraging)")

    df_filtered = df.copy()
    if delay_30 and delay_60:
        st.warning("⚠️ Beide filters geselecteerd. De strengste filter (>60 minuten) is toegepast.")
        df_filtered = df_filtered[df_filtered["Total Delay"] > 60]
    elif delay_30:
        df_filtered = df_filtered[df_filtered["Total Delay"] > 30]
    elif delay_60:
        df_filtered = df_filtered[df_filtered["Total Delay"] > 60]
    else:
        st.info("ℹ️ Geen filter geselecteerd. Alle vluchten worden getoond.")

    agg = df_filtered.groupby(["Customer Type", "Type of Travel", "Satisfaction"]).size().reset_index(name="count")
    agg["Group"] = agg["Customer Type"] + " - " + agg["Type of Travel"]

    fig = px.bar(
        agg,
        x="Group",
        y="count",
        color="Satisfaction",
        barmode="group",
        text_auto=True,
        color_discrete_sequence=[primary_color, "lightcoral"]
    )
    fig.update_layout(
        xaxis_title="Customer Type & Type of Travel",
        yaxis_title="Aantal passagiers",
        legend_title="Satisfaction"
    )

    # Afwisselend blauw/geel voor de x-as labels
    groups = agg["Group"].unique().tolist()
    colors = ["royalblue", "goldenrod"]  # wisselkleur
    tickvals = list(range(len(groups)))
    ticktext = [
        f"<span style='color:{colors[i % 2]}'>{grp}</span>"
        for i, grp in enumerate(groups)
    ]

    fig.update_xaxes(
        tickvals=tickvals,
        ticktext=ticktext
    )

    st.plotly_chart(fig, use_container_width=True)

    #-------------------Grafiek Koen---------------------------
    #---------------------------------------------------------
    # Titel
    st.title("Tevredenheid per categorie")

    # Dropdown voor Class-selectie (met "Alle Klassen")
    class_options = ["Alle Klassen"] + sorted(df["Class"].dropna().unique())
    selected_class = st.selectbox("Kies een klasse:", class_options)

    # Start met hele dataset of filter op gekozen klasse
    if selected_class == "Alle Klassen":
      filtered_df = df.copy()
    else:
        filtered_df = df[df["Class"] == selected_class]

    # Filter voor vertraagde vluchten (fallback op Total Delay > 15 als 'Flight Status' niet bestaat)
    delay_filter = st.checkbox("Toon alleen vertraagde vluchten ✈️", value=False)
    if delay_filter:
        if "Flight Status" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Flight Status"] == "Delayed"]
        elif "Total Delay" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Total Delay"] > 15]
        else:
            st.warning("Geen 'Flight Status' of 'Total Delay' kolom gevonden; vertraagde filter niet toegepast.")

    # Verwachte aspecten (labels)
    expected_aspects = [
    "Ease of Online booking", "Checkin service", "Online boarding",
    "Gate location", "On-board service", "Seat comfort",
    "Leg room service", "Cleanliness", "Food and drink",
    "Inflight service", "Inflight wifi service", "Inflight entertainment",
    "Baggage handling"
    ]

    # Normaliseer kolomnamen voor robuuste matching
    import re
    def normalize(s: str) -> str:
        return re.sub(r'[^a-z0-9]', '', str(s).lower())

    norm_to_col = {normalize(col): col for col in df.columns}
    available_aspects = [(asp, norm_to_col[normalize(asp)]) for asp in expected_aspects if normalize(asp) in norm_to_col]

    # UI: multiselect voor aspecten
    labels = [label for label, _ in available_aspects]
    cols_map = {label: col for label, col in available_aspects}

    if not labels:
        st.warning("Geen satisfaction-aspecten gevonden in de dataset. Controleer kolomnamen.")
    else:
        st.write("Kies de aspecten die je wilt zien:")
        selected_labels = st.multiselect("Aspects", options=labels, default=labels)

        selected_cols = [cols_map[label] for label in selected_labels]

        # Alleen numerieke kolommen meenemen
        valid_cols = [c for c in selected_cols if c in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[c])]

        if valid_cols and len(filtered_df) > 0:
            mean_values = filtered_df[valid_cols].mean()
            # Zet index terug naar de gebruiksvriendelijke labels
            idx_to_label = {col: label for label, col in available_aspects}
            mean_values.index = [idx_to_label.get(col, col) for col in mean_values.index]
            st.bar_chart(mean_values)
        else:
            st.warning("Geen geldige numerieke aspecten geselecteerd, of er is geen data na filtering.")
    #-------------------Grafiek Ann---------------------------
    #---------------------------------------------------------
    st.title("Boxplot: Leeftijdsverdeling per Geslacht en Klasse")

    # Filteropties in de sidebar of direct boven de grafiek
    gender_options = ["Alle Geslachten"] + df["Gender"].dropna().unique().tolist()
    selected_gender = st.selectbox("Kies een geslacht:", gender_options)

    class_options = ["Alle Klassen"] + df["Class"].dropna().unique().tolist()
    selected_class = st.selectbox("Kies een klasse:", class_options)

    # Maak een filterkopie
    df_box = df.copy()

    if selected_gender != "Alle Geslachten":
        df_box = df_box[df_box["Gender"] == selected_gender]

    if selected_class != "Alle Klassen":
        df_box = df_box[df_box["Class"] == selected_class]

    # Alleen boxplot tekenen als er data is
    if df_box.empty:
        st.warning("Geen data beschikbaar voor deze selectie.")
    else:
        fig_box = px.box(
            df_box,
            x="Class",
            y="Age",
            color="Gender",
            title="Leeftijdsverdeling per klasse en geslacht",
            color_discrete_map={"Male": "royalblue", "Female": "lightcoral"}
        )
        fig_box.update_layout(
            xaxis_title="Klasse",
            yaxis_title="Leeftijd"
        )
        st.plotly_chart(fig_box, use_container_width=True)




#-------------------page 3-----------------------------
#-------------------------------------------------------
elif page == "Data Overzicht":
    st.markdown(f"<h1 style='color:{primary_color}'>✎ Data Overzicht</h1>", unsafe_allow_html=True)
    st.write("Op deze pagina zijn de gebruikte datasets te vinden. Onder ieder dataset staat de bijbehorende bron.")
    st.write("Hieronder is het  dataframe *airline_passenger_satisfaction.csv* te zien:")
    # Main dataframe laten zien
    st.dataframe(df)
    st.write("*Bron: Ahmad Bhat, M. (n.d.). Airline passenger satisfaction [Data set]. Kaggle.*")
    st.write("*https://www.kaggle.com/datasets/mysarahmadbhat/airline-passenger-satisfaction*")
    
    # Witregels
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.write("Hieronder is het dataframe *airlines_flights_data.csv* te zien:")
    # Extra dataframe laten zien
    st.dataframe(df_extra)
    st.write("*Bron: Grewal, R. (n.d.). Airlines flights data [Data set]. Kaggle.*")
    st.write("*https://www.kaggle.com/datasets/rohitgrewal/airlines-flights-data*")

#-------------------page 4-----------------------------
#-------------------------------------------------------
elif page == "Werkwijze":
    st.markdown(f"<h1 style='color:{primary_color}'>✎ Werkwijze</h1>", unsafe_allow_html=True)
    st.write("Hier komt een beschrijving van hoe wij te werk zijn gegaan.")
