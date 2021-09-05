import streamlit as st 
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px 
import plotly.figure_factory as ff
import preprocessing, helper



df = pd.read_csv(r'data\athlete_events.csv')
regions_df = pd.read_csv(
    r'data\noc_regions.csv')


df = preprocessing.preprocessors(df, regions_df)

user_choice = st.sidebar.radio(
    
    'Enter Your Selection',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)


if user_choice == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    
    years, country = helper.year_list(df)
    selected_year = st.sidebar.selectbox('Selected Year', years)
    selected_country = st.sidebar.selectbox('Selected Country', country)
    
    medal_tally = helper.fetch_medal_tally(df, selected_year,selected_country)
    
    if selected_country == 'Overall' and selected_year =='Overall':
        st.title('Overall Medal Tally')
    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title(f'Overall Medal Tally In Year {str(selected_year)}')
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(f'Medal Tally Of {selected_country} In Year {str(selected_year)}')
    
    st.table(medal_tally)




if user_choice == 'Overall Analysis':
    editions = df['Year'].nunique()
    host_cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()
    
    st.title('Top Olympics Stats')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.title('Editions')
        st.header(editions)
        
    with col2:
        st.title('Host Cities')
        st.header(host_cities)
        
    with col3:
        st.title('Sports')
        st.header(sports)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.title('Events')
        st.header(events)

    with col2:
        st.title('Athletes')
        st.header(athletes)

    with col3:
        st.title('Nations')
        st.header(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations Over Time')
    st.plotly_chart(fig)
    
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events Over Time')
    st.plotly_chart(fig)
    
    sports_over_time = helper.data_over_time(df, 'Sport')
    fig = px.line(sports_over_time, x='Edition', y='Sport')
    st.title('Number Of Sports Over Time')
    st.plotly_chart(fig)
    
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Numer Of Athletes Over Time')
    st.plotly_chart(fig)
    
    st.title("No. of Events Over Time With Respect To Every Sport")
    fig, ax = plt.subplots(figsize=(25, 35))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                     annot=True, cmap = 'coolwarm',annot_kws={'size': 20})
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=18)
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=22)
    st.pyplot(fig)


    st.title('Most Succesfull Athletes (By Sport)')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport',sport_list)
    athletes = helper.most_succesful(df, selected_sport)
    st.table(athletes)


if user_choice == 'Country-wise Analysis':
    
    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country',country_list)
    
    
    yearly_medal_tally = helper.year_wise_medals(df, selected_country)
    fig = px.line(yearly_medal_tally, x='Year', y='Medal')
    st.title(f'Year Wise Medal Tally Of {selected_country}')
    st.plotly_chart(fig)

    st.title(f'Performance Of {selected_country} In Particular Sports')
    event_heatmap = helper.event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(35, 35))
    ax = sns.heatmap(event_heatmap, annot = True,annot_kws={'size': 20}, cbar = False)
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=20)
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=26)

    st.pyplot(fig)

    st.title(f'Top 10 Athletes Of {selected_country}')
    top_athletes = helper.succesful_athletes(df, selected_country)
    st.table(top_athletes)
    
if user_choice == 'Athlete-wise Analysis':
    
    st.title('Distribution Of Athlete Age')
    athlete_df = df.drop_duplicates(subset= ['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age Distribution', 'Gold Medalists',
                       'Silver Medalists', 'Bronze Medalists'], show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)
    
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    selected_sport = st.selectbox('Select a sport', sport_list)
    
    st.title('Athletes Height and Weight Comparison')
    athletes = helper.athletes_attributes(df,selected_sport)
    fig = px.scatter(athletes, x='Weight', y='Height', color='Medal', symbol='Medal', facet_row="Sex")
    fig.update_layout(autosize = False, width = 800, height = 900)

    st.plotly_chart(fig)
    
    st.title('Gender Participation Over The Years')
    participation = helper.gender_participation(df) 
    fig = px.line(participation, x = 'Year', y =['Men', 'Women'])
    fig.update_layout(autosize = False, width = 1000, height = 600)

    st.plotly_chart(fig)
