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

top_10 = df_selection.groupby(['Наименование_клиента'],as_index=False)['Тонны'].agg(['sum', 'mean','count'])



# ---- MAINPAGE ----
st.title(":bar_chart: Показатели активности клиентов")
st.markdown("### Основные метрики")
total_sales = int(df_selection['Тонны'].sum())
average_rating = round(df_selection.groupby('Наименование_клиента')['Тонны'].mean().mean(), 1)
average_sale_by_transaction = round(df_selection['Наименование_клиента'].nunique(), 0)

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

d = alt.Chart(t13).mark_trail().encode(
   x="month",
   y=alt.Y(
        'Тонны',
        scale=alt.Scale(type="log")  # Here the scale is applied
    ),
   color="Наименование_клиента",
   )

st.altair_chart(d, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
