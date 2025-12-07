import gradio as gr
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_samples(n = 30):
    # 카드 이용 내역 샘플 데이터 생성
    np.random.seed(42)

    # 날짜 생성 (최근 30일)
    start_date = datetime.now() - timedelta(days=30)
    dates = [start_date + timedelta(days=x) for x in range(n)]

    # 카드 종류
    cards = ['신한카드', '삼성카드', '현대카드', 'KB국민카드', '우리카드']

    # 가맹점 종류
    merchants = ['스타벅스', 'GS25', '쿠팡', '네이버페이', '카카오페이', 
                 '이마트', '올리브영', 'CGV', '배달의민족', '카페베네',
                 'Apple', '11번가', '무신사', '다이소', '맥도날드']

    # 할부 옵션
    installments = ['일시불', '2개월', '3개월', '6개월', '12개월']

    # DataFrame 생성
    df = pd.DataFrame({
        '이용일': [d.strftime('%Y-%m-%d') for d in sorted(dates, reverse=True)],
        '이용카드': np.random.choice(cards, n),
        '이용가맹점': np.random.choice(merchants, n),
        '이용금액': np.random.randint(5000, 500000, n),
    })

    # 할부/회차
    df['할부/회차'] = np.random.choice(installments, n)

    # 적립/할인율 (0~5%)
    df['적립/할인율(%)'] = np.random.uniform(0.5, 5.0, n).round(2)

    # 예상적립/할인 = 이용금액 * 적립율
    df['예상적립/할인'] = (df['이용금액'] * df['적립/할인율(%)'] / 100).round(0).astype(int)

    # 결제원금 = 이용금액 - 예상적립/할인
    df['결제원금'] = df['이용금액'] - df['예상적립/할인']

    # 결제후잔액 (누적 계산)
    df['결제후잔액'] = df['결제원금'].cumsum()

    # 수수료(이자) - 할부일 경우만 발생
    df['수수료(이자)'] = 0
    installment_mask = ~df['할부/회차'].isin(['일시불'])
    df.loc[installment_mask, '수수료(이자)'] = np.random.randint(1000, 10000, installment_mask.sum())
    return df


def preprocess_rawdata(file):
    print(file)
    return generate_samples()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            input_files = gr.File(label="Upload Multiple Files Output", file_count="multiple")
        with gr.Column(scale=1):
            a = 1
    with gr.Row():
        df = gr.Dataframe(interactive=True)

    input_files.upload(preprocess_rawdata, input_files, df)

if __name__ == "__main__":
    demo.launch()
