import pandas as pd
import streamlit as st

airline_satisfaction=pd.read_csv('airline_passenger_satisfaction.csv')
airline_satisfaction.head()

airline_data=pd.read_csv('airlines_flights_data.csv')
airline_data.head()

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("airline_passenger_satisfaction.csv")
    # Maak total delay
    df["Total Delay"] = df["Departure Delay"].fillna(0) + df["Arrival Delay"].fillna(0)
    return df

df = load_data()

# Checkbox voor delay filter
delay_30 = st.checkbox("Filter op vertraagde vluchten (>30 minuten totaal)")
delay_60 = st.checkbox("Filter op vertraagde vluchten (>60 minuten totaal)")

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