#-------------------imports-----------------------------
#-------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#-------------------data inladen-----------------------
#-------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("airline_passenger_satisfaction.csv")
    # Maak total delay
    df["Total Delay"] = df["Departure Delay"].fillna(0) + df["Arrival Delay"].fillna(0)
    return df

df = load_data()  # nu overal beschikbaar

#-------------------sidebar-----------------------------
#-------------------------------------------------------
page = st.sidebar.selectbox("Selecteer een pagina", ["Overzicht", "Dashboard", "Data Analyse", "Page blank"])

#-------------------page 1-----------------------------
#-------------------------------------------------------
if page == "Overzicht":
    # Logo in sidebar
    st.sidebar.image("Vertrekbord Team HV0009.png", use_container_width=True)

    # Titel
    st.title("Overzicht - Klanttevredenheid KLM")
    # Witregel
    st.write("")
    # Introductie tekst onder de titel
    st.markdown("**Welkom!**")
    st.write("Op dit dashboard vind je uitgebreide informatie over de tevredenheid van klanten van KLM.")
    st.write("Gebruik het dropdown menu om de verschillende pagina's te bezoeken.")
    # Witregel
    st.write("")
    # Introductie tekst onder de titel
    st.markdown("**Snel overzicht**")
    st.write("Hieronder zijn een aantal simpele KPI's (Key Performance Indicators) te zien.")
    st.write("Klik op de afbeeldingen om ze beter te bekijken.")

    # ======================
    # Extra filtersectie - Afhankelijke sliders
    # ======================
    st.markdown("### 🎚️ Leeftijdsfilter")

    col_min, col_max = st.columns(2)
    with col_min:
        min_age = st.slider(
            "Minimum leeftijd",
            int(df["Age"].min()),
            int(df["Age"].max()),
            int(df["Age"].min()),
            key="min_age_slider"
        )
    with col_max:
        max_age = st.slider(
            "Maximum leeftijd",
            int(df["Age"].min()),
            int(df["Age"].max()),
            int(df["Age"].max()),
            key="max_age_slider"
        )

    # Zorg dat de sliders logisch aan elkaar gekoppeld zijn
    if min_age > max_age:
        st.warning("⚠️ Minimum leeftijd kan niet groter zijn dan maximum. Waarden zijn aangepast.")
        min_age, max_age = max_age, min_age

    # Filter de data op leeftijd
    df_filtered = df[(df["Age"] >= min_age) & (df["Age"] <= max_age)]

    # ======================
    # KPI berekeningen (nu op df_filtered)
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

    # ======================
    # Visualisaties (2x2 grid)
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        # KPI totaal passagiers
        fig1 = go.Figure(go.Indicator(
            mode="number",
            value=total_passengers,
            title={"text": "Totaal Passagiers"}
        ))
        st.plotly_chart(fig1, use_container_width=True, key="fig1")

    with col2:
        # KPI avg satisfaction (gauge 0-5)
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_satisfaction,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Gem. Tevredenheid (0-5)"},
            gauge={
                'axis': {'range': [0, 5]},
                'bar': {'color': "royalblue"},
                'steps': [
                    {'range': [0, 2], 'color': "lightcoral"},
                    {'range': [2, 4], 'color': "lightyellow"},
                    {'range': [4, 5], 'color': "lightgreen"}
                ],
            }
        ))
        st.plotly_chart(fig2, use_container_width=True, key="fig2")

    col3, col4 = st.columns(2)

    with col3:
        # KPI avg departure delay
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_dep_delay,
            title={'text': "Gem. Vertrekvertraging (min)"},
            gauge={
                'axis': {'range': [0, max(60, avg_dep_delay*2)]},
                'bar': {'color': "orange"},
            }
        ))
        st.plotly_chart(fig3, use_container_width=True, key="fig3")

    with col4:
        # KPI avg arrival delay
        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_arr_delay,
            title={'text': "Gem. Aankomstvertraging (min)"},
            gauge={
                'axis': {'range': [0, max(60, avg_arr_delay*2)]},
                'bar': {'color': "red"},
            }
        ))
        st.plotly_chart(fig4, use_container_width=True, key="fig4")

#-------------------page 2-----------------------------
#-------------------------------------------------------
elif page == "Dashboard":
    st.title("📊 Dashboard klanttevredenheid KLM")
    st.write("This is Page 1 content.")

    #---------------------grafiek 1----------------------------------
    # Checkbox voor delay filter
    delay_30 = st.checkbox("Filter op vertraagde vluchten (>30 minuten vertraging)")
    delay_60 = st.checkbox("Filter op vertraagde vluchten (>60 minuten vertraging)")

    # Pas filters toe
    df_filtered = df.copy()
    if delay_30:
        df_filtered = df_filtered[df_filtered["Total Delay"] > 30]

    if delay_60:
        df_filtered = df_filtered[df_filtered["Total Delay"] > 60]

    # Groeperen
    agg = df_filtered.groupby(["Customer Type", "Type of Travel", "Satisfaction"]).size().reset_index(name="count")

    # Maak een gecombineerde X-label (CustomerType + TravelType)
    agg["Group"] = agg["Customer Type"] + " - " + agg["Type of Travel"]

    # Grouped bar chart
    fig = px.bar(
        agg,
        x="Group",
        y="count",
        color="Satisfaction",
        barmode="group",
        text_auto=True,
        title="Satisfaction per Customer Type en Type of Travel"
    )

    fig.update_layout(
        xaxis_title="Customer Type & Type of Travel",
        yaxis_title="Aantal passagiers",
        legend_title="Satisfaction"
    )

    st.plotly_chart(fig, use_container_width=True)

#-------------------page 3-----------------------------
#-------------------------------------------------------
elif page == "Data Analyse":
    st.title("📝 Data Analyse")
    st.write("text.")

#-------------------page 4-----------------------------
#-------------------------------------------------------
elif page == "Page blank":
    st.title("⚙️ Page blank")
    st.write("text.")
