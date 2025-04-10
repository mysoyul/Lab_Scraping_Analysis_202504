import streamlit as st
import pandas as pd
import plotly.express as px

import matplotlib
import matplotlib.font_manager as fm

font_path = 'C:\\windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path).get_name()
matplotlib.rc('font', family=font_prop)

# 데이터 로딩
df = pd.read_csv('data/인구현황.csv')

# 남초/여초 판별 컬럼 추가
df['성비판별'] = df['남여 비율'].apply(lambda x: '남초' if x > 1 else ('여초' if x < 1 else '비슷'))

st.title("대한민국 지역별 인구 통계 대시보드")

# 지역 선택 필터
region = st.selectbox("지역 선택", df['행정기관'].unique())

# 선택한 지역 데이터
selected = df[df['행정기관'] == region]

# KPI 카드
col1, col2, col3 = st.columns(3)
col1.metric("총 인구수", f"{int(selected['총인구수'].values[0]):,} 명")
col2.metric("세대수", f"{int(selected['세대수'].values[0]):,} 세대")
col3.metric("세대당 인구", f"{selected['세대당 인구'].values[0]} 명")

# 남초/여초 Pie Chart
fig = px.pie(df, names='성비판별', title='남초 vs 여초 지역 분포', hole=0.4)
st.plotly_chart(fig)

# 선택한 지역 남/여 비율
st.subheader(f"{region} 남/여 인구 비율")
fig2 = px.pie(selected.melt(id_vars=['행정기관'], value_vars=['남자 인구수', '여자 인구수']),
              names='variable', values='value', title=f'{region} 남/여 인구')
st.plotly_chart(fig2)

# 데이터 테이블
st.subheader("전체 데이터")
st.dataframe(df)

