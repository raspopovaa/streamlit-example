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
#import random
import openpyxl
import numpy as np

st.set_page_config(page_title=" Панель текущих продаж менеджеров", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    df = pd.read_parquet(
        'data_full.parquet',
        )
   
    return df    
    

df = get_data_from_excel()


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
manager = st.sidebar.multiselect(
    "Выбери менеджера:",
    options=df['Менеджер'].unique(),
    default=df['Менеджер'].unique()
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

otdel = st.sidebar.multiselect(
    "Выбери отделение:",
    options=df['Отделение'].unique(),
    default=df['Отделение'].unique()
)
df_selection = df.query(
    'Менеджер in @manager & month in @month & Сегмент in @segment & НГ in @prod & Отделение in @otdel'
)

t10 = df_selection.groupby(['Наименование_клиента'],as_index=False)['Тонны'].sum().sort_values(by='Тонны', ascending=False).head(11)
t11 = t10.rename(columns = {'Наименование_клиента':'Контрагент','Тонны':'Потребление:Тонны'}
).reset_index().drop('index',axis=1)
t11.index = np.arange(1,len(t10)+1)
t12 = df_selection.groupby(['Менеджер'],as_index=False)['Тонны'].sum().sort_values(by='Тонны', ascending=False)
t12['Тонны'] = t12['Тонны'].astype('int')

# ---- MAINPAGE ----
st.title(":bar_chart: Показатели активности клиентов")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection['Тонны'].sum())
average_rating = round(df_selection.groupby('Наименование_клиента')['Тонны'].mean().mean(), 1)
star_rating = ":bomb:" * 1
average_sale_by_transaction = round(df_selection['Наименование_клиента'].nunique(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Общая реализация:")
    st.subheader(f":moneybag: {total_sales} тонн")
with middle_column:
    st.subheader("Среднее потребление клиента:")
    st.subheader(f"{star_rating} {average_rating} тонн")
with right_column:
    st.subheader("Количество активных клиентов:")
    st.subheader(f":articulated_lorry: {average_sale_by_transaction} клиентов")

st.markdown("""---""")

col1, col2, col3 = st.columns(3)
col1.metric("Общая реализация: тонн", total_sales,)
col2.metric("Среднее потребление клиента: тонн", average_rating, )
col3.metric("Количество активных клиентов: клиентов", average_sale_by_transaction,)

st.markdown("""---""")
st.title(":articulated_lorry: ТОП-10 клиентов")
st.markdown("###")

st.table(t11.style.highlight_max(color='yellowgreen', subset='Потребление:Тонны'))
st.table(t11.style.highlight_max(color='yellowgreen', subset='Потребление:Тонны'
                                ).format("{:.1f}").background_gradient(cmap='Blues', axis=1)
        )
st.dataframe(t11.style.highlight_max(axis=0))
         
st.markdown("""---""")


c = alt.Chart(t11).mark_line().encode(
     x='Контрагент', y='Потребление:Тонны')

st.altair_chart(c, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
