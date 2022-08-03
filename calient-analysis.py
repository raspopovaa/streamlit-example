# -*- coding: utf-8 -*-

#pip install -r requirements.txt
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import altair as alt
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pydeck as pdk
from PIL import Image

st.set_page_config(page_title=" Показатели клиента", page_icon=":bar_chart:", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---- READ EXCEL ----
@st.cache(allow_output_mutation=True)
def get_data_from_parquet():
    df = pd.read_parquet(
        'one_client_tranz.parquet',
        )
   
    return df    
    

df = get_data_from_parquet()
df['month'] = df['Дата_транзакции'].dt.month
df['datehour'] = df['Время_транзакции'].dt.hour

# ---- SIDEBAR ----
st.sidebar.image(Image.open('logo.png'))
st.sidebar.header("Тут може отфильтровать данные:")



card = st.sidebar.multiselect(
    "Выбери карту:",
    options=df['Номер_карты'].unique(),
    default=df['Номер_карты'].unique()
)

df_selection_otdel = df.query(
    'Номер_карты in @card'
)
tovar = st.sidebar.multiselect(
    "Выбери вид топлива:",
    options=df_selection_otdel['Товар'].unique(),
    default=df_selection_otdel['Товар'].unique()
)
azs = st.sidebar.multiselect(
    "Выбери АЗС:",
    options=df['АЗС'].unique(),
    default=df['АЗС'].unique()
)
month = st.sidebar.multiselect(
    "Выбери месяц:",
    options=df['month'].unique(),
    default=df['month'].unique()
)

df_selection = df.query(
    'Товар in @tovar & АЗС in @azs & month in @month & Номер_карты in @card'
)

t10 = df_selection.groupby(['Номер_карты'],as_index=False)['Количество'].agg(['sum', 'mean','count']).reset_index().sort_values(
    by='sum', ascending=False).head(5)
t10.index = np.arange(1, len(t10)+1)
top_10 = t10.rename(columns={'sum':'Общее потребление', 'mean':'Среднее потребление', 'count':'Количество заправок'})
top_10 = top_10.style.background_gradient(axis=0, gmap=t10['sum'], cmap='PuBu')

# ---- MAINPAGE ----
st.title(":bar_chart: Показатели активности клиента")
st.markdown("### Основные метрики")
total_sales = int(df_selection['Количество'].sum())
average_rating = round(df_selection.groupby('Номер_карты')['Количество'].mean().mean(), 1)
average_sale_by_transaction = round(df_selection['Номер_карты'].nunique())

col1, col2, col3, = st.columns(3)

col1.metric("Общая реализация: тонн", total_sales,)
col2.metric("Среднее потребление клиента: тонн", average_rating, )
col3.metric("Количество активных клиентов: клиентов", average_sale_by_transaction,)

st.markdown("""---""")
st.markdown("### :articulated_lorry: ТОП-10 клиентов")

st.table(top_10)
      
st.markdown("""---""")


t01 = df_selection.groupby(['Номер_карты'],as_index=False)['Количество'].sum().nlargest(5,'Количество')
t02 = t01['Номер_карты']
t13 = df_selection.query('Номер_карты in @t02').groupby(['month','Номер_карты',],as_index=False)['Количество'].sum()

  
st.markdown("""---""")

df1 = df_selection.query('Наименование_клиента in @t02').groupby(['month','Номер_карты'],as_index=False)['Количество'].sum().sort_values(by='month', ascending=False)
df1['Количество'] = round(df1['Количество'])

fig = px.line(df1, x="month", y="Количество", color='Номер_карты', symbol="Номер_карты",hover_name="Номер_карты")
st.markdown('### Динамика по картам')
st.plotly_chart(fig, use_container_width=True)

st.markdown("""---""")
st.markdown("### :articulated_lorry: Отток клиентов")

tt = df_selection.pivot_table(index='Номер_карты', columns='month', values='Количество', aggfunc='sum').reset_index()


st.markdown("""---""")
st.markdown("### :articulated_lorry:   Карта распределения транзакций клиентов")

df['lot'] = df['Координаты'].apply(lambda x: x.split(',')[0])
df['lon'] = df['Координаты'].apply(lambda x: x.split(',')[1])

df[['lot','lon']] = (df[['lot','lon']]).astype('float')
st.map(df[['lot','lon']])


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
