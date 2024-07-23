import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("olympics Analysis")
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise-analysis', 'Athlete-wise-analysis')
)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", country)
    selected_country = st.sidebar.selectbox("Select Country", years)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'overall' and selected_country == 'overall':
        st.header('overall tally')
    if selected_year != 'overall' and selected_country == 'overall':
        st.header('Medal tally in ' + str(selected_year) + ' olympics')
    if selected_year == 'overall' and selected_country != 'overall':
        st.header(selected_country + ' overall performance')
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + ' performance in ' + str(selected_year) + ' olympics')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.header("Top statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')

    fig = px.line(nations_over_time, x="Edition", y='region')
    st.title("Participation over time")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')

    fig = px.line(events_over_time, x="Edition", y='Event')
    st.title("Events over time")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')

    fig = px.line(athletes_over_time, x="Edition", y='Name')
    st.title("Athletes over time")
    st.plotly_chart(fig)

    st.title("No of events over time(Every sport")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
                     , annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    selected_sport = st.selectbox("Select Sport", sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise-analysis':
    st.sidebar.title('country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select the country', country_list)

    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title("Medal Tally over the year")
    st.plotly_chart(fig)

    st.title('Countries Excels')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_country_wise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise-analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['overall', 'Gold', 'Silver', 'Bronze'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

