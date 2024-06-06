import streamlit as st
import requests
import json
import datetime
import pandas as pd

# 학교 조회하는 함수
@st.cache_data
def find_my_school(school_name, url):
    params = {
        'KEY': st.secrets['neis']['key'],
        # 'KEY': neis_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'SCHUL_NM': school_name
    }

    response = requests.get(url, params=params)
    contents = response.text
    data = json.loads(contents)
    
    schools_by_district = {}
    for item in data["schoolInfo"][1]["row"]:
        district = item["ATPT_OFCDC_SC_NM"]
        district_code = item['ATPT_OFCDC_SC_CODE']
        school_name = item["SCHUL_NM"]
        school_code = item['SD_SCHUL_CODE']
        schools_by_district.setdefault(district, []).extend([school_name, school_code, district_code])
    return schools_by_district

# 급식 정보를 조회하는 함수
@st.cache_data
def give_me_meal(district_code, school_code, date):
    mealurl = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    params = {
        'KEY': st.secrets['neis']['key'],
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'ATPT_OFCDC_SC_CODE': district_code,
        'SD_SCHUL_CODE': school_code,
        'MLSV_YMD': date
    }

    response = requests.get(mealurl, params=params)
    contents = response.text
    data = json.loads(contents)
    
    try:
        menu = data["mealServiceDietInfo"][1]['row'][0]['DDISH_NM'].split('<br/>')
    except:
        st.error("정보를 불러올 수 없습니다. 날짜를 다시 확인해주세요! 급식이 없던 날 같아요.")
        menu = []
    return menu
