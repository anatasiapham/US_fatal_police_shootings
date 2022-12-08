import streamlit as st
import pandas as pd


#Import the data set
fps = pd.read_csv("fps/fatal-police-shootings-data.csv")

st.header("US Fatal Police Shootings since 2015")
st.image('police_drawing.jpeg', use_column_width=True)
st.subheader('Purpose')
st.markdown('Using public data collected by the Washington Post, I wanted to visualize and learn about the victims of fatal police shootings in the United States. The entire project can be found by visiting the following **[Github](https://github.com/anatasiapham/US_Fatal_Police_Shootings)**.')

st.subheader('Brief Background')
st.markdown("The **[Washington Post](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/)** has been collecting data about fatal police encounters since 2015. The data used in this app was last updated on October 7th, 2022. These numbers reflect only the deaths that were reported by news or police departments. Oftentimes, these incidents are under reported and are therefore not accounted for in this data set.")

st.sidebar.markdown("US Fatal Police Shootings since 2015")

st.write(fps)
