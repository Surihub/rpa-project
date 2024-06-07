import streamlit as st
import base64
from openai import OpenAI

st.title("비슷한 이미지 생성하기")

api_key = st.sidebar.text_input("OpenAI API를 입력해주세요. ", type='password')
client = OpenAI(api_key=api_key)

# 이미지 인코딩 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 이미지 파일 업로드
uploaded_file = st.file_uploader("이미지를 업로드해주세요.")

if uploaded_file is not None:
    # 업로드된 파일을 base64로 인코딩
    base64_image = encode_image(uploaded_file)
    # 업로드된 이미지 표시
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the essence of the image and write a message."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }]
    )

    # 응답 처리
    image_explanation = response.choices[0].message.content
    st.write(image_explanation)

    # DALL-E 모델을 사용하여 이미지 생성
    response2 = client.images.generate(
        model="dall-e-3",
        prompt=image_explanation,
        size="1024x1024",
        n=1, 
        quality="hd",
        style = 'vivid'
    )

    image_url = response2.data[0].url
    st.image(image_url, caption='Generated Image')