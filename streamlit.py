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
    df["Total Delay"] = df["Departure Delay"].fillna(0) + df["Arrival Delay"].fillna(0)
    return df

df = load_data()

#-------------------sidebar-----------------------------
#-------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌍 KLM Dashboard") 
    theme = st.radio("Kies een thema:", ["Licht", "Donker"], index=0)
    st.markdown("---")  
    page = st.selectbox("Selecteer een pagina", ["Overzicht", "Dashboard", "Data Analyse", "Page blank"])

#-------------------HTML/CSS Theme Switch-----------------
if theme == "Donker":
    st.markdown(
        """
        <style>
        .css-18e3th9 {background-color: #0e1117;}
        .css-1d391kg {background-color: #0e1117;}
        .css-hi6a2p {background-color: #1c1f26;}
        .css-1d76goe, .css-1v3fvcr, .css-1v3fvcr p, .css-1d76goe p {color: #f5f5f5;}
        </style>
        """, unsafe_allow_html=True
    )
    primary_color = "lightblue"
    secondary_color = "orange"
    text_color = "white"
    gauge_steps = [
        {'range': [0, 2], 'color': "red"},
        {'range': [2, 4], 'color': "yellow"},
        {'range': [4, 5], 'color': "green"}
    ]
else:
    primary_color = "royalblue"
    secondary_color = "orange"
    text_color = "black"
    gauge_steps = [
        {'range': [0, 2], 'color': "lightcoral"},
        {'range': [2, 4], 'color': "lightyellow"},
        {'range': [4, 5], 'color': "lightgreen"}
    ]

#-------------------page 1-----------------------------
#-------------------------------------------------------
if page == "Overzicht":
    st.sidebar.image("Vertrekbord Team HV0009.png", use_container_width=True)

    st.title("Overzicht - Klanttevredenheid KLM")
    st.write("")
    st.markdown("**Welkom!**")
    st.write("Op dit dashboard vind je uitgebreide informatie over de tevredenheid van klanten van KLM.")
    st.write("Gebruik het dropdown menu om de verschillende pagina's te bezoeken.")
    st.write("")
    st.markdown("**Snel overzicht**")
    st.write("Hieronder zijn een aantal simpele KPI's (Key Performance Indicators) te zien.")
    st.write("Klik op de afbeeldingen om ze beter te bekijken.")

    # Leeftijdsfilter
    st.markdown("###  Leeftijdsfilter")
    col_min, col_max = st.columns(2)
    with col_min:
        min_age = st.slider("Minimum leeftijd", int(df["Age"].min()), int(df["Age"].max()), int(df["Age"].min()))
    with col_max:
        max_age = st.slider("Maximum leeftijd", int(df["Age"].min()), int(df["Age"].max()), int(df["Age"].max()))
    if min_age > max_age:
        st.warning("⚠️ Minimum leeftijd kan niet groter zijn dan maximum. Waarden zijn aangepast.")
        min_age, max_age = max_age, min_age

    df_filtered = df[(df["Age"] >= min_age) & (df["Age"] <= max_age)]

    # KPI berekeningen
    total_passengers = df_filtered["ID"].nunique()
    satisfaction_cols = ["On-board Service", "Seat Comfort", "Leg Room Service", "Cleanliness",
                         "Food and Drink", "In-flight Service", "In-flight Wifi Service",
                         "In-flight Entertainment", "Baggage Handling"]
    avg_satisfaction = df_filtered[satisfaction_cols].mean().mean()
    avg_dep_delay = df_filtered["Departure Delay"].mean()
    avg_arr_delay = df_filtered["Arrival Delay"].mean()
    delayed_percentage = (df_filtered[df_filtered["Total Delay"] > 15].shape[0] / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0

    # Visualisaties
    col1, col2, col5 = st.columns(3)
    with col1:
        fig1 = go.Figure(go.Indicator(mode="number", value=total_passengers, title={"text": "Totaal Passagiers"}, number={'font': {'color': primary_color}}))
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = go.Figure(go.Indicator(mode="gauge+number", value=avg_satisfaction, domain={'x':[0,1],'y':[0,1]},
                                      title={'text': "Gem. Tevredenheid (0-5)"},
                                      gauge={'axis':{'range':[0,5]}, 'bar':{'color': primary_color}, 'steps': gauge_steps}))
        st.plotly_chart(fig2, use_container_width=True)
    with col5:
        fig5 = go.Figure(go.Indicator(mode="gauge+number", value=delayed_percentage,
                                      title={'text': "Vertraagde vluchten (%)"},
                                      gauge={'axis':{'range':[0,100]}, 'bar':{'color': secondary_color},
                                             'steps':[{'range':[0,30],'color':'lightgreen'},{'range':[30,60],'color':'lightyellow'},{'range':[60,100],'color':'lightcoral'}]},
                                      number={'suffix':'%'}))
        st.plotly_chart(fig5, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig3 = go.Figure(go.Indicator(mode="gauge+number", value=avg_dep_delay, title={'text': "Gem. Vertrekvertraging (min)"},
                                      gauge={'axis':{'range':[0,max(60, avg_dep_delay*2)]}, 'bar':{'color': secondary_color}}))
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        fig4 = go.Figure(go.Indicator(mode="gauge+number", value=avg_arr_delay, title={'text': "Gem. Aankomstvertraging (min)"},
                                      gauge={'axis':{'range':[0,max(60, avg_arr_delay*2)]}, 'bar':{'color':'red'}}))
        st.plotly_chart(fig4, use_container_width=True)

#-------------------page 2-----------------------------
#-------------------------------------------------------
elif page == "Dashboard":
    st.title("📊 Dashboard klanttevredenheid KLM")
    st.write("Filter hier op vertraagde vluchten.")

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
        title="Satisfaction per Customer Type en Type of Travel",
        color_discrete_sequence=[primary_color, "lightcoral"]
    )
    fig.update_layout(xaxis_title="Customer Type & Type of Travel", yaxis_title="Aantal passagiers", legend_title="Satisfaction")
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
