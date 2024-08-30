import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 구글 서비스 계정 키 파일 경로 설정
SERVICE_ACCOUNT_FILE = 'summer-foundry-429504-e6-600d272ac3fc.json'  # 🟦'path_to_your_service_account.json' 부분 수정 필요

# Google Sheets API 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)

# 스프레드시트 열기
spreadsheet = client.open("rockyrocky")  # 🟦'Your Spreadsheet Name' 부분 수정 필요
worksheet = spreadsheet.sheet1

# Streamlit UI 설정
st.title('데이터 입력 예제')

# 사용자 입력 받기
name = st.text_input('이름을 입력하세요:')
age = st.number_input('나이를 입력하세요:', min_value=0, max_value=100)

# 제출 버튼
if st.button('제출'):
    # 스프레드시트에 데이터 추가
    worksheet.append_row([name, age])
    st.success('데이터가 스프레드시트에 추가되었습니다!')
