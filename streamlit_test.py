#-------------------imports-----------------------------
#-------------------------------------------------------
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
#-------------------sidebar-----------------------------
#-------------------------------------------------------
# Sidebar menu
page = st.sidebar.selectbox("Select a page", ["Home", "Page 1", "Page 2", "Page 3", "Page 4"])
#-------------------page 1-----------------------------
#-------------------------------------------------------
if page == "Home":
    st.title("🏠 Home Page")
    st.write("Welcome to the home page!")

elif page == "Page 1":
    st.title("📊 Page 1 - Analytics")
    st.write("This is Page 1 content.")
#---------------------grafiek 1----------------------------------

#Inladen datasets
airline_satisfaction=pd.read_csv('airline_passenger_satisfaction.csv')
airline_data=pd.read_csv('airlines_flights_data.csv')

# Load data
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

#-------------------page 2-----------------------------
#-------------------------------------------------------
elif page == "Page 2":
    st.title("📝 Page 2 - Reports")
    st.write("This is Page 2 content.")

#-------------------page 3-----------------------------
#-------------------------------------------------------

elif page == "Page 3":
    st.title("⚙️ Page 3 - Settings")
    st.write("This is Page 3 content.")

#-------------------page 4-----------------------------
#-------------------------------------------------------
elif page == "Page 4":
    st.title("📌 Page 4 - Notes")
    st.write("This is Page 4 content.")






















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