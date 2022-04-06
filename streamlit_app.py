# -*- coding: utf-8 -*-
"""Untitled39.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CfYTu5rc9-DtesrlmO9dXqfvsIH0V8y2
"""
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


st.set_page_config(page_title=" Панель продаж в текущем месяце", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    df = pd.read_parquet(
        'data_full.parquet',
        )
   
    return df    
    

df = get_data_from_excel()


# ---- SIDEBAR ----
st.sidebar.header("Тут може отфильтровать данные:")

otdel = st.sidebar.multiselect(
    "Выбери отделение:",
    options=df['Отделение'].unique(),
    default=df['Отделение'].unique()
)

df_selection_otdel = df.query(
    'Отделение in @otdel'
)
manager = st.sidebar.multiselect(
    "Выбери менеджера:",
    options=df_selection_otdel['Менеджер'].unique(),
    default=df_selection_otdel['Менеджер'].unique()
)
month = st.sidebar.multiselect(
    "Выбери месяц:",
    options=df['month'].unique(),
    default=df['month'].unique()
)
segment = st.sidebar.multiselect(
    "Выбери сегмент:",
    options=df['Сегмент'].unique(),
    default=df['Сегмент'].unique()
)
prod = st.sidebar.multiselect(
    "Выбери продукт:",
    options=df['НГ'].unique(),
    default=df['НГ'].unique()
)
df_selection = df.query(
    'Менеджер in @manager & month in @month & Сегмент in @segment & НГ in @prod & Отделение in @otdel'
)

t10 = df_selection.groupby(['Наименование_клиента'],as_index=False)['Тонны'].agg(['sum', 'mean','count']).reset_index().sort_values(
    by='sum', ascending=False).head(10)
t10.index = np.arange(1, len(t10)+1)
top_10 = t10.rename(columns={'sum':'Общее потребление', 'mean':'Среднее потребление', 'count':'Количество заправок'})
top_10 = top_10.style.background_gradient(axis=0, gmap=t10['sum'], cmap='PuBu')

# ---- MAINPAGE ----
st.title(":bar_chart: Показатели активности клиентов")
st.markdown("### Основные метрики")
total_sales = int(df_selection['Тонны'].sum())
average_rating = round(df_selection.groupby('Наименование_клиента')['Тонны'].mean().mean(), 1)
average_sale_by_transaction = round(df_selection['Наименование_клиента'].nunique())

col1, col2, col3 = st.columns(3)
col1.metric("Общая реализация: тонн", total_sales,)
col2.metric("Среднее потребление клиента: тонн", average_rating, )
col3.metric("Количество активных клиентов: клиентов", average_sale_by_transaction,)

st.markdown("""---""")
st.markdown("### :articulated_lorry: ТОП-10 клиентов")

st.table(top_10)
      
st.markdown("""---""")


t01 = df_selection.groupby(['Наименование_клиента'],as_index=False)['Тонны'].sum().nlargest(5,'Тонны')
t02 = t01['Наименование_клиента']
t13 = df_selection.query('Наименование_клиента in @t02').groupby(['month','Наименование_клиента',],as_index=False)['Тонны'].sum()

  
st.markdown("""---""")

df1 = df_selection.query('Наименование_клиента in @t02').groupby(['month','Наименование_клиента'],as_index=False)['Тонны'].sum().sort_values(by='month', ascending=False)
df1['Тонны'] = round(df1['Тонны'])

fig = px.line(df1, x="month", y="Тонны", color='Наименование_клиента', symbol="Наименование_клиента",hover_name="Наименование_клиента")
st.markdown('### Динамика ТОП клиентов')
st.plotly_chart(fig, use_container_width=True)

st.markdown("""---""")
st.markdown("### :articulated_lorry: Отток клиентов")

tt = df_selection.pivot_table(index='Наименование_клиента', columns='month', values='Тонны', aggfunc='sum').reset_index()

# функция для добавления нулей
def null(str):
  if  str < 15:
    return 0
  else:
    return str

tt[(tt.columns[1])] = tt[(tt.columns[1])].apply(null)

st.table(tt[tt[(tt.columns[1])] == 0])

st.markdown("""---""")
st.markdown("### :articulated_lorry:   Карта распределения заправок")

@st.cache(allow_output_mutation=True)
def get_data_from_par():
    df = pd.read_parquet(
        'data_tranz.parquet',
        )
   
    return df    
    

df2 = get_data_from_par()
st.table(df2.head(5))


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
