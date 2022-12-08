import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data


#Import the data set
fps = pd.read_csv("fps/fatal-police-shootings-data.csv")

st.header('Overall in the United States')
st.markdown('Adjust chart settings in the sidebar')

#creating tabs
tab1, tab2 = st.tabs(['US Map','Bar Chart'])

#Dictionary for Race
race_dict = {
    "A":'Asian',
    "B":'Black',
    "H":'Hispanic',
    "N":'Native American',
    "O":'Other',
    "W":'White'
}

#change races to be not abbreviated
fps_race = fps.replace({"race":race_dict})

#create dataframe that only includes geocoding accurate records
geo = fps_race[fps_race['is_geocoding_exact']==True]
geo_mod = geo[geo['name'] != "Gary Brown"].dropna() #dropped Gary Brown due to inaccurate coordinate, entry error?
geo_mod = geo_mod[geo_mod['longitude'].notna()]

#list of names
names = geo_mod['name'].sort_values()

st.sidebar.header('US Map Settings')
selected = st.sidebar.selectbox('Search for specific person on the map:', names)
st.sidebar.markdown('')
st.sidebar.header('State Bar Chart Settings')
min_count = st.sidebar.slider('Minimum Count of Deaths',10,400,100,10)
label_button = st.sidebar.checkbox('Labels?')

#create dataframe that includes only the person selected
person_df = geo_mod[geo_mod['name'] == selected]

#create dataframe that filters for states that meet the minimum count
state_count = fps.groupby(['state'])['state'].count().reset_index(name='count')
state_count_mod = state_count[state_count['count'] > min_count]


with tab1:

    st.write('')

    states = alt.topo_feature(data.us_10m.url, feature='states')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=700,
        height=500
    )   

    points1 = alt.Chart(geo_mod, title='Victims of Fatal Police Encounters in the US').mark_circle(color='red').encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(10),
        tooltip=['name', 'race', 'date']
    ).project(
        'albersUsa'
    )

    total_map = alt.layer(background, points1).configure_title(
        fontSize=20
        )
    tab1.altair_chart(total_map, use_container_width=True)

    st.write('')
    st.markdown('These map charts visualize the locations of all the victims of fatal police shootings in the United States. Note that this map does not include the victims whose coordinates or names were not recorded (null).')
    st.write('')
    st.write('')


    points2 = alt.Chart(geo_mod, title={"text": ['Victims of Fatal Police Encounters in the US'], "subtitle": ['Victim: 'f'{selected}']}).mark_circle(color='yellow').encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(10),
        tooltip='name'
    ).project(
        'albersUsa'
    ).properties(
        width=700,
        height=500
    )   

    highlight = alt.Chart(person_df).mark_circle(color='red').encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(30),
        tooltip=['name', 'race', 'date']
    ).project(
        'albersUsa'
    )

    selected_map = alt.layer(background, points2, highlight).configure_title(
        fontSize=20,
        subtitleFontSize=16
        )
    tab1.altair_chart(selected_map, use_container_width=True)



with tab2:
    st.write('')

    if label_button:
        bar_chart = alt.Chart(state_count_mod, title="Total Fatal Police Shootings by State").mark_bar(color='red').encode(
            x=alt.X('count:Q', title='Number of Fatal Police Shootings'),
            y=alt.Y('state:N', title='States', sort = alt.EncodingSortField('count', op='sum', order='descending'))
        )

        text = bar_chart.mark_text(
        align='left',
        baseline='middle',
        dx=3,
        color='white'
        ).encode(
        text='count:Q'
        )

        bar = alt.layer(bar_chart, text).configure_axis(
        labelFontSize=12,
        titleFontSize=16
        ).configure_title(
        fontSize=24
        )
        tab2.altair_chart(bar, use_container_width=True)
    else:
        bar_chart = alt.Chart(state_count_mod, title="Total Fatal Police Shootings by State").mark_bar(color='red').encode(
            x=alt.X('count:Q', title='Number of Fatal Police Shootings'),
            y=alt.Y('state:N', title='States', sort = alt.EncodingSortField('count', op='sum', order='descending'))
        ).configure_axis(
            labelFontSize=11,
            titleFontSize=13
        ).configure_title(
            fontSize=20
        )

        tab2.altair_chart(bar_chart, use_container_width=True)



