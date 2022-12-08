import streamlit as st
import pandas as pd
import altair as alt

#Import the data set
fps = pd.read_csv("fps/fatal-police-shootings-data.csv")

#Dictionary for Race
race_dict = {
    "A":'Asian',
    "B":'Black',
    "H":'Hispanic',
    "N":'Native American',
    "O":'Other',
    "W":'White'
}

#Filter to drop null in race
fps_race = fps[fps['race'].notna()]
fps_race.info()

fps_race = fps_race.replace({"race":race_dict})


st.header('Who were the victims?')
st.markdown("Representation of Deaths Reported")

#creating tabs
tab1, tab2, tab3 = st.tabs(['By Gender','By Age','By Race'])

with tab1:
    data = pd.DataFrame([dict(id=i) for i in range(1, 96)])

    person = (
        "M1.7 -1.7h-0.8c0.3 -0.2 0.6 -0.5 0.6 -0.9c0 -0.6 "
        "-0.4 -1 -1 -1c-0.6 0 -1 0.4 -1 1c0 0.4 0.2 0.7 0.6 "
        "0.9h-0.8c-0.4 0 -0.7 0.3 -0.7 0.6v1.9c0 0.3 0.3 0.6 "
        "0.6 0.6h0.2c0 0 0 0.1 0 0.1v1.9c0 0.3 0.2 0.6 0.3 "
        "0.6h1.3c0.2 0 0.3 -0.3 0.3 -0.6v-1.8c0 0 0 -0.1 0 "
        "-0.1h0.2c0.3 0 0.6 -0.3 0.6 -0.6v-2c0.2 -0.3 -0.1 "
        "-0.6 -0.4 -0.6z"
    )

    males = alt.Chart(data).transform_calculate(
        row="ceil(datum.id/10)"
    ).transform_calculate(
        col="datum.id - datum.row*10"
    ).mark_point(
        filled=True,
        size=50, color='#01A6EA'
    ).encode(
        x=alt.X("col:O", axis=None),
        y=alt.Y("row:O", axis=None),
        shape=alt.ShapeValue(person)
    )

    data2 = pd.DataFrame([dict(id=i) for i in range(1, 101)])

    females = alt.Chart(data2).transform_calculate(
        row="ceil(datum.id/10)"
    ).transform_calculate(
        col="datum.id - datum.row*10"
    ).mark_point(
        filled=True,
        size=50, color='#FFB1CB'
    ).encode(
        x=alt.X("col:O", axis=None),
        y=alt.Y("row:O", axis=None),
        shape=alt.ShapeValue(person)
    )

    gender = alt.layer(females + males, title={"text":['Fatal Police Shootings by Gender'], "subtitle": [" "]}).configure_title(
        fontSize=20
    ).properties(
        width=400,
        height=400
    ).configure_view(
        strokeWidth=0
    )

    tab1.altair_chart(gender, use_container_width=True)


    st.markdown("<h2 style='text-align: center;'>According to the genders reported, almost 95% of victims were male.</h1>", unsafe_allow_html=True)


with tab2:

    age_chart = alt.Chart(fps, title='Fatal Police Shootings by Age').mark_bar(color='red').encode(
        y=alt.Y('count():Q', title='Number of Fatal Police Shootings'),
        x=alt.X('age', title='Age Range', bin=True)
    ).configure_axis(
        labelFontSize=11,
        titleFontSize=16
    ).configure_title(
        fontSize=20
    ).properties(
        width=700,
        height=500
    )   
    tab2.altair_chart(age_chart, use_container_width=True)

    st.markdown("<h2 style='text-align: center;'>Most of the victims ages ranged from 20 to 50.</h1>", unsafe_allow_html=True)


with tab3:

    race_chart = alt.Chart(fps_race, title="Fatal Police Shootings by Race").mark_bar().encode(
        y=alt.Y('count():Q', title='Number of Fatal Police Shootings'),
        x=alt.X('race', title='Race', axis=alt.Axis(labelAngle=0), sort='-y'),
        color=alt.Color('race', legend=alt.Legend(title='Races'))
    ).configure_axis(
        labelFontSize=11,
        titleFontSize=16,
        grid=False
    ).configure_title(
        fontSize=20
    ).properties(
        width=700,
        height=500
    )

    tab3.altair_chart(race_chart, use_container_width=True)

    st.markdown("<h2 style='text-align: center;'>Of the races reported, a vast majority of the victims were White, Black, or Hispanic.</h1>", unsafe_allow_html=True)
   
