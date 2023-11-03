import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Config
st.set_page_config(
    layout="wide",
    page_title="Immigration Analysis App",
    page_icon="🌍 "
)
years = list(range(1980,2014))
cols_to_drop=['Type','Coverage','AREA','DEV','REG']
rename_dict={'OdName':'Country',
             'AreaName': 'Continent',
             'RegName':'Region',
             'DevName':'Status'}
@st.cache_data()
def load_data(path):
    df = pd.read_excel('Canada.xlsx', sheet_name=1, skiprows=20, skipfooter=2)    
    df.drop(columns=cols_to_drop, inplace=True)
    df.rename(columns=rename_dict, inplace=True)
    df['Total'] = df[years].sum(axis=1)
    df.set_index('Country', inplace=True)
    return df

with st.spinner('Processing Immigration Data'):
    df=load_data('Canada.xlsx')
with st.container():
    st.image("https://www.tc-ww.com/wp-content/uploads/2022/09/Canada-Immigration.jpg",width=200)
    st.title("Immigration Analysis app")
    st.subheader("Data Summary")
c1,c2,c3,c4,c5,c6=st.columns(6)

total_countries=df.shape[0]
duration="1980-2013"
total_immigration=df['Total'].sum()

c1.metric("Total Countries",total_countries)
c2.metric("Year",duration)
c3.metric("Total Immigration",total_immigration)

st.header("Immigration Visualization")
fig=px.line(df,x=df.index,y='Total')
st.plotly_chart(fig,use_container_width=True)

top_countries=df.sort_values(by='Total',ascending=False).head(25)

c1, c2=st.columns([1,3])

limit=c2.slider("Select Number of Countries",1,25, value=5)
countries = top_countries.index.tolist()[:limit]
countries_df = df.loc[countries,years].T
fig2=px.area(countries_df,x=countries_df.index,y=countries_df.columns)


c1.dataframe(top_countries)
c2.plotly_chart(fig2 ,use_container_width=True)

st.subheader("Trend Comparison")
c1,c2=st.columns([1,3])
country_list=df.index.tolist()
countries=c2.multiselect("Select countries",country_list)
if countries:
    countries_df=df.loc[countries,years].T
    fig3=px.line(
        countries_df,
        x=countries_df.index,
        y=countries_df.columns
        )
    for country in countries:
        c1.info(f'{country}:{df.loc[country,"Total"]} Immigration')
    c2.plotly_chart(fig3,use_container_width=True)
    st.toast('Your graph has been loaded!',icon='🫡')