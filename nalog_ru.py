import pandas as pd
import streamlit as st
import requests
import time
import openpyxl



uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )
if uploaded_file is not None:
      file_container = st.expander("Посмотри на свой файл")
      shows = pd.read_excel(uploaded_file)
      uploaded_file.seek(0)
      file_container.write(shows)

else:
      st.info(
            f"""
                👆 Выберите файл, пример файла: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
                """
        )

      st.stop()

shows = shows.sample(3)

df_b = pd.DataFrame({'ИНН': [], 'ОГРН': [], 'Наименование': [], 'ОКВЭД': [], 'ФИО': [], 'паспорт': [], 'договор': [], 'предмент': [], 'цена': [], 'срок': [], 'иные': [], 'ИНН': [], 'ОГРН': [], 'ФИО': [], 'адрес': [], 'паспорт': [], 'руководитель': [], 'иные': [], 'паспорт': [], 'менеджер': []})
df_b['ИНН']= shows['ИНН']
df_b['договор']= shows['Наименование договора']
df_b['менеджер']= shows['Ответственный менеджер']


    	
response = requests.get('https://api.github.com')
print(response.status_code)

# функция для выгрузки ОГРН
def find_ogrn(str):
  try:
    url = 'https://egrul.nalog.ru'
    url_1 = 'https://egrul.nalog.ru/search-result/'
    inn = str
    r = requests.post(url, data={'query': inn})
    time.sleep(1)  
    r1 = requests.get(url_1 + r.json()['t'])
    return(int(r1.json()['rows'][0]['o']))
    
  except:
    try:
      time.sleep(1) 
      return(r1.json()['rows'][0]['o'])
      
    except:
      return str

# функция для выгрузки Названия клиента
def find_name(str):
  try:
    url = 'https://egrul.nalog.ru'
    url_1 = 'https://egrul.nalog.ru/search-result/'
    inn = str
    r = requests.post(url, data={'query': inn})

    time.sleep(1)
    r1 = requests.get(url_1 + r.json()['t'])
    return(r1.json()['rows'][0]['c'])
    time.sleep(1)
  except:
    return(r1.json()['rows'][0]['n'])
    time.sleep(1)



# функция для выгрузки ФИО директора
def find_dir(str):
  try:
    url = 'https://egrul.nalog.ru'
    url_1 = 'https://egrul.nalog.ru/search-result/'
    inn = str
    r = requests.post(url, data={'query': inn})

    time.sleep(1)
    r1 = requests.get(url_1 + r.json()['t'])
    return(r1.json()['rows'][0]['g'].split(':')[1])
    time.sleep(1)
  except:
    try:
      return(r1.json()['rows'][0]['n'])
      time.sleep(1)
    except:
      print('ошибка')

# функция для выгрузки адреса
def find_adress(str):
  try:
    url = 'https://egrul.nalog.ru'
    url_1 = 'https://egrul.nalog.ru/search-result/'
    inn = str
    r = requests.post(url, data={'query': inn})

    time.sleep(1)
    r1 = requests.get(url_1 + r.json()['t'])
    return(r1.json()['rows'][0]['a'])
    time.sleep(1)
  except:
    try:
      return('У ИП нет адреса')
      time.sleep(1)
    except:
      print('ошибка')


