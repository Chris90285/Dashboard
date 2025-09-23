#-------------------imports-----------------------------
#-------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

#-------------------sidebar-----------------------------
#-------------------------------------------------------
# Sidebar menu
page = st.sidebar.selectbox("Selecteer een pagina", ["Overzicht", "Dashboard", "Data Analyse", "Page blank"])

#-------------------page 1-----------------------------
#-------------------------------------------------------
if page == "Overzicht":
    # Logo rechtsboven
    st.image("a321neo_profile_right", width=150)  # maak het groter, pas width aan naar wens

    # Titel
    st.title("🏠 Overzicht - Klanttevredenheid KLM")

    # Introductie tekst onder de titel
    st.markdown("**Welkom!**")
    st.write("Op dit dashboard vind je uitgebreide informatie over de tevredenheid van klanten van KLM.")
    st.write("Gebruik het dropdown menu om een pagina te bezoeken.")


#-------------------page 2-----------------------------
#-------------------------------------------------------

elif page == "Dashboard":
    st.title("📊 Dashboard klanttevredenheid KLM")
    st.write("This is Page 1 content.")

    #---------------------grafiek 1----------------------------------
    # Load data (cached)
    @st.cache_data
    def load_data():
        df = pd.read_csv("airline_passenger_satisfaction.csv")
        # Maak total delay
        df["Total Delay"] = df["Departure Delay"].fillna(0) + df["Arrival Delay"].fillna(0)
        return df

    df = load_data()

    # Checkbox voor delay filter
    delay_30 = st.checkbox("Filter op vertraagde vluchten (>30 minuten vertraging)")
    delay_60 = st.checkbox("Filter op vertraagde vluchten (>60 minuten vertraging)")

    # Pas filters toe
    if delay_30:
        df = df[df["Total Delay"] > 30]

    if delay_60:
        df = df[df["Total Delay"] > 60]

    # Groeperen
    agg = df.groupby(["Customer Type", "Type of Travel", "Satisfaction"]).size().reset_index(name="count")

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


