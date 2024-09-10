import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit 앱 제목
st.title("나스닥 주식 종목 차트 분석 도구")

# 나스닥 종목 예시 (간단하게 몇 가지 종목만 포함)
nasdaq_symbols = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta (Facebook)": "META"
}

# 종목 선택 드롭다운
selected_stock = st.selectbox("종목을 선택하세요", list(nasdaq_symbols.keys()))

# 기간 선택
start_date = st.date_input("시작 날짜", pd.to_datetime("2022-01-01"))
end_date = st.date_input("종료 날짜", pd.to_datetime("today"))

# 선택된 종목의 심볼
stock_symbol = nasdaq_symbols[selected_stock]

# 주식 데이터 다운로드
if st.button("차트 분석하기"):
    # yfinance를 통해 데이터 가져오기
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # 데이터가 존재하는지 확인
    if stock_data.empty:
        st.error("해당 기간에 데이터가 없습니다. 다른 기간을 선택해 주세요.")
    else:
        # 차트 그리기
        st.subheader(f"{selected_stock} ({stock_symbol}) 주가 차트")

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock_data.index, stock_data['Close'], label="종가", color="blue")
        ax.set_xlabel("날짜")
        ax.set_ylabel("주가 (USD)")
        ax.set_title(f"{selected_stock} 주가 차트 ({start_date} ~ {end_date})")
        ax.legend()

        st.pyplot(fig)

        # 주가 데이터 테이블 출력
        st.subheader(f"{selected_stock} 주가 데이터")
        st.dataframe(stock_data)
