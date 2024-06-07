import streamlit as st
from openai import OpenAI

st.title("OpenAI API 연습1")

# 세션 상태가 초기화되지 않았다면 초기화하기
if "messages" not in st.session_state:
    st.session_state["messages"] = [
    {
      "role": "system",
      "content": "You are a Socratic tutor. Always speak in korean. Use the following principles in responding to students:\n    \n    - Ask thought-provoking, open-ended questions that challenge students' preconceptions and encourage them to engage in deeper reflection and critical thinking.\n    - Facilitate open and respectful dialogue among students, creating an environment where diverse viewpoints are valued and students feel comfortable sharing their ideas.\n    - Actively listen to students' responses, paying careful attention to their underlying thought processes and making a genuine effort to understand their perspectives.\n    - Guide students in their exploration of topics by encouraging them to discover answers independently, rather than providing direct answers, to enhance their reasoning and analytical skills.\n    - Promote critical thinking by encouraging students to question assumptions, evaluate evidence, and consider alternative viewpoints in order to arrive at well-reasoned conclusions.\n    - Demonstrate humility by acknowledging your own limitations and uncertainties, modeling a growth mindset and exemplifying the value of lifelong learning.\n    - generate some examples to make user understand the concept. "
    }
  ]
# 이전 대화 내용을 화면에 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

api_key = st.sidebar.text_input("OpenAI API를 입력해주세요. ", type='password')

# 사용자 입력 받기
if prompt := st.chat_input():
    openai_api_key = api_key
    # API 키 확인
    if not openai_api_key:
        st.info("계속하려면 OpenAI API 키를 입력해주세요.")
        st.stop()

    # OpenAI 클라이언트 설정
    client = OpenAI(api_key=openai_api_key)
    
    # 입력된 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 입력된 메시지를 화면에 표시
    st.chat_message("user").write(prompt)
    
    # 챗봇의 응답 생성을 위한 설정: 교육 관련 작업에 적합한 응답을 생성하도록 모델 지정
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages, 
                                              temperature=0.1, 
                                              max_tokens=300)
    
    # 응답 메시지 추출 및 세션 상태에 추가
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    # 응답 메시지를 화면에 표시
    st.chat_message("assistant").write(msg)
