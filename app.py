import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit 앱 제목
st.title("죽음의 나스닥 선물")

# 나스닥 종목 예시
nasdaq_symbols = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta (Facebook)": "META"
}

# 종목 선택 드롭다운 (두 개 선택)
selected_stocks = st.multiselect("비교할 종목을 선택하세요 (최대 2개)", list(nasdaq_symbols.keys()), default=["Apple", "Microsoft"])

# 기간 선택
start_date = st.date_input("시작 날짜", pd.to_datetime("2022-01-01"))
end_date = st.date_input("종료 날짜", pd.to_datetime("today"))

# 선택된 종목이 두 개인지 확인
if len(selected_stocks) != 2:
    st.error("두 개의 종목을 선택해 주세요.")
else:
    stock_symbol_1 = nasdaq_symbols[selected_stocks[0]]
    stock_symbol_2 = nasdaq_symbols[selected_stocks[1]]

    # 주식 데이터 다운로드
    stock_data_1 = yf.download(stock_symbol_1, start=start_date, end=end_date)
    stock_data_2 = yf.download(stock_symbol_2, start=start_date, end=end_date)

    if stock_data_1.empty or stock_data_2.empty:
        st.error("선택한 기간에 데이터가 없습니다. 다른 기간을 선택해 주세요.")
    else:
        # 두 종목의 종가를 가져오기
        stock_data_1_close = stock_data_1['Close']
        stock_data_2_close = stock_data_2['Close']

        # 차트 그리기
        st.subheader(f"{selected_stocks[0]} vs {selected_stocks[1]} 주가 차트")
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(stock_data_1_close.index, stock_data_1_close, label=selected_stocks[0], color="blue")
        ax.plot(stock_data_2_close.index, stock_data_2_close, label=selected_stocks[1], color="green")
        ax.set_xlabel("날짜")
        ax.set_ylabel("주가 (USD)")
        ax.set_title(f"{selected_stocks[0]} vs {selected_stocks[1]} 주가 비교 ({start_date} ~ {end_date})")
        ax.legend()

        st.pyplot(fig)

        # 구간 수익률 계산
        def calculate_return(start_price, end_price):
            return ((end_price - start_price) / start_price) * 100

        return_1 = calculate_return(stock_data_1_close.iloc[0], stock_data_1_close.iloc[-1])
        return_2 = calculate_return(stock_data_2_close.iloc[0], stock_data_2_close.iloc[-1])

        # 수익률 비교 출력
        st.subheader("구간 수익률 비교")
        st.write(f"{selected_stocks[0]}의 구간 수익률: {return_1:.2f}%")
        st.write(f"{selected_stocks[1]}의 구간 수익률: {return_2:.2f}%")
        
        if return_1 > return_2:
            st.write(f"결과: {selected_stocks[0]}의 수익률이 더 높습니다.")
        elif return_1 < return_2:
            st.write(f"결과: {selected_stocks[1]}의 수익률이 더 높습니다.")
        else:
            st.write("결과: 두 종목의 수익률이 동일합니다.")

        # 주가 데이터 테이블 출력
        st.subheader(f"{selected_stocks[0]} 및 {selected_stocks[1]} 주가 데이터")
        combined_data = pd.DataFrame({
            f"{selected_stocks[0]} 종가": stock_data_1_close,
            f"{selected_stocks[1]} 종가": stock_data_2_close
        })
        st.dataframe(combined_data)
