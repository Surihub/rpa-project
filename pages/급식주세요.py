import streamlit as st
import requests
import json
import datetime
import pandas as pd

neis_key = "f63baaa8bb1b4b0fa0b1b41d3a8747f8"

# 학교 조회하는 함수
@st.cache_data
def find_my_school(school_name, url):
    params = {
        # 'KEY': st.secrets['neis']['key'],
        'KEY': neis_key,
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
        'KEY': neis_key,
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

# Streamlit 앱 설정
st.title("😍급식타임")

url = "https://open.neis.go.kr/hub/schoolInfo"

st.subheader("학교 조회")
school_input = st.text_input("학교이름을 입력해주세요.")

if school_input:
    # 1. 학교 먼저 찾기
    schools_by_district = find_my_school(school_input, url)
    if schools_by_district:
        district = st.radio("학교가 소속된 교육청을 선택해주세요", options=schools_by_district.keys())
        school_name = schools_by_district[district][0]
        school_code = schools_by_district[district][1]
        district_code = schools_by_district[district][2]

        st.subheader(school_name + "의 급식을 찾아볼게요!")
        date = st.date_input("조회할 날짜를 입력해주세요:", datetime.date(2024, 4, 2)).strftime("%Y%m%d")

        # 2. 급식 검색하기
        menu = give_me_meal(district_code, school_code, date)
        if menu:
            st.table(menu)
    else:
        st.warning("해당 이름의 학교를 찾을 수 없습니다. 다시 입력해주세요.")
else:
    st.info("학교 이름을 입력하고 조회 버튼을 눌러주세요.")
