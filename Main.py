import streamlit as st 
import pandas as pd
from io import BytesIO
from datetime import datetime, date, timedelta


from sklearn.preprocessing import MinMaxScaler

pd.options.display.float_format = '{:.2f}'.format
df = pd.read_csv('./pages/data/한국지역난방공사_인버터별 분단위 태양광발전 정보_20211031.csv', encoding='cp949')

data = df[['인버터아이디', '장소', '측정일시', '경사면일사량(인버터단위)','수평면일사량(인버터단위)',
           '외부온도(인버터단위)','모듈온도(인버터단위)','인버팅후 금일발전량']]

data.columns = ['인버터아이디', '장소', '측정일시', '경사면일사량', '수평면일사량', '외부온도', '모듈온도', '금일발전량']

def scaling(df):
    lst =['경사면일사량', '수평면일사량', '외부온도', '모듈온도', '금일발전량']
    
    df_tmp = df[lst].to_numpy()
    transformer = MinMaxScaler()
    transformer.fit(df_tmp)
    df_tmp = transformer.transform(df_tmp)
    
    df1 = df[['인버터아이디', '장소', '시간대']].set_index('시간대')
    df2 = pd.DataFrame(df_tmp, index=df['시간대'], columns=lst)
    
    return pd.concat([df1, df2], axis=1)

st.set_page_config(layout="wide")
st.title("📊 Trend & Report")

st.caption('여러 항목들에 대해서 비교 분석해 동향을 쉽게 파악할 수 있는 모니터링 시스템 메인 화면입니다.')
st.caption('Monitoring system that compares and analyzes multiple items : :blue[_trend & report_]')

places = data['장소'].unique()
option1 = st.sidebar.selectbox(
    '장소 선택',
    places, help='태양광 발전소 장소')


인버터id = data[data['장소']==option1]['인버터아이디'].unique()
option2 = st.sidebar.selectbox(
    '인터버 아이디 선택',
    인버터id, help='인버터(Inverter) : 태양전지 패널에서 발생한 가변 직류(variable DC)를 상용 전력망 혹은 지역의 비계통연계망에서 사용할 수 있도록 전력 계통 주파수 교류(AC)로 변환해 주는 장치')

option3 = st.sidebar.multiselect(
    '그래프에 표시할 항목 선택',
    ['금일발전량', '외부온도', '모듈온도', '수평면일사량', '경사면일사량'],
    ['금일발전량', '외부온도', '모듈온도', '수평면일사량', '경사면일사량'], help="중복 선택해서 비교가능")

tmp_data = data[(data['장소']==option1) & (data['인버터아이디']==option2)]
tmp_data['시간대'] = tmp_data['측정일시'].apply(lambda x:x[-5:])
tmp_data = tmp_data.set_index('시간대').reset_index()


def  calculate(string, df):
    lst = ['금일발전량','경사면일사량','수평면일사량','외부온도','모듈온도']
    if string == 'Mean':
        a,b,c,d,e = df[lst].mean()
        return a,b,c,d,e
    elif string == 'Max':
        a,b,c,d,e = df[lst].max()
        return a,b,c,d,e
    elif string == 'Min':
        a,b,c,d,e, = df[lst].min()
        return a,b,c,d,e
    
str_to_convert1 = tmp_data.loc[0, '측정일시'][:10]
str_to_convert2 = tmp_data.loc[len(tmp_data)-1, '측정일시'][:10]

start = datetime.strptime(str_to_convert1, '%Y-%m-%d')
end = datetime.strptime(str_to_convert2, '%Y-%m-%d')


selected_date = st.sidebar.date_input(
    "날짜 선택",
    start+timedelta(days=1), min_value=start, max_value=end)
string_date = selected_date.strftime('%Y-%m-%d')
cur_data = tmp_data[tmp_data['측정일시'].str.contains(string_date)]


if selected_date.day != 1:
    pre_date = selected_date - timedelta(days=1)
    pre_date = pre_date.strftime('%Y-%m-%d')
    pre_data = tmp_data[tmp_data['측정일시'].str.contains(pre_date)]
    A1,B1,C1,D1,E1 = calculate('Mean', pre_data)
    A2,B2,C2,D2,E2 = calculate('Max', pre_data)
    A3,B3,C3,D3,E3 = calculate('Min', pre_data)
else:
    A1,B1,C1,D1,E1 = calculate('Mean', cur_data)
    A2,B2,C2,D2,E2 = calculate('Max', cur_data)
    A3,B3,C3,D3,E3 = calculate('Min', cur_data)
    
# print(tmp_data)
st.sidebar.markdown('---')

tab1, tab2, tab3 = st.tabs([ "Mean", "Max", "Min"])
# 전일 대비 변화량은?? 어떻게 구하면 될까 생각해보기
st.caption("▲: 전일대비 상승  ▼: 전일대비 하락")
with tab1:
    col1, col2, col3, col4, col5 = st.columns(5)
    a,b,c,d,e = calculate('Mean', cur_data)
    if a < 1000000:
        col1.metric("금일발전량", f"{a:.2f} Wh", f"{a-A1:.2f} Wh")
    else:
        col1.metric("금일발전량", f"{a/1000:.2f} kWh", f"{(a-A1)/1000:.2f} kWh")
    
    col2.metric("경사면일사량", f"{b:.2f} W/m", f"{b-B1:.2f} W/m")
    col3.metric("수평면일사량", f"{c:.2f} W/m", f"{c-C1:.2f} W/m")
    col4.metric("외부온도", f"{d:.2f} °C", f"{d-D1:.2f} °C")
    col5.metric("모듈온도", f"{e:.2f} °C", f"{e-E1:.2f} °C")
with tab2:
    col1, col2, col3, col4, col5 = st.columns(5)
    a,b,c,d,e = calculate('Max', cur_data)
    if a < 1000000:
        col1.metric("금일발전량", f"{a:.2f} Wh", f"{a-A2:.2f} Wh")
    else:
        col1.metric("금일발전량", f"{a/1000:.2f} kWh", f"{(a-A2)/1000:.2f} kWh")
    col2.metric("경사면일사량", f"{b:.2f} W/m", f"{b-B2:.2f} W/m")
    col3.metric("수평면일사량", f"{c:.2f} W/m", f"{c-C2:.2f} W/m")
    col4.metric("외부온도", f"{d:.2f} °C", f"{d-D2:.2f} °C")
    col5.metric("모듈온도", f"{e:.2f} °C", f"{e-E2:.2f} °C")
with tab3:
    col1, col2, col3, col4, col5 = st.columns(5)
    a,b,c,d,e = calculate('Min', cur_data)
    if a < 1000000:
        col1.metric("금일발전량", f"{a:.2f} Wh", f"{a-A3:.2f} Wh")
    else:
        col1.metric("금일발전량", f"{a/1000:.2f} kWh", f"{(a-A3)/1000:.2f} kWh")
    col2.metric("경사면일사량", f"{b:.2f} W/m", f"{b-B3:.2f} W/m")
    col3.metric("수평면일사량", f"{c:.2f} W/m", f"{c-C3:.2f} W/m")
    col4.metric("외부온도", f"{d:.2f} °C", f"{d-D3:.2f} °C")
    col5.metric("모듈온도", f"{e:.2f} °C", f"{e-E3:.2f} °C")
    
st.markdown(" ")
st.markdown(" ")

st.subheader(f"[{string_date}] {option1} 추세 그래프1")
st.caption("선택한 장소, 인버터 아이디를 바탕으로 여러 항목의 변화량 비교를 하루 단위로 한눈에 알아 볼수 있는 그래프 입니다.")
st.info("🔔 금일발전량 같은 경우 누적값으로 측정되기 때문에 그래프가 일정하다는 것은 발전량이 생산되지 않았다는 뜻입니다.")

chart_df = scaling(cur_data)[option3]
st.line_chart(chart_df)
# print(chart_df)

# print(scaling(tmp_data)[option3])
st.warning("비정상적으로 급격하게 값이 감소하는 경우  측정 오류, 기계 고장 등일 가능성이 높습니다.", icon="⚠️")

# 인버터아이디별 시간별 금일 발전량 비율 그래프 데이터 만들기

data = data[data['장소']==option1]
data =data[data['측정일시'].str.contains(string_date)]
data['시간대'] = data['측정일시'].apply(lambda x:x[-5:])
data = data.set_index('시간대').reset_index()

df_tmp = pd.DataFrame()
for i in 인버터id:
    df_tmp = pd.concat([df_tmp, data[data['인버터아이디']==i].set_index('시간대')['금일발전량']], axis=1)
df_tmp.columns = 인버터id


st.subheader(f"[{string_date}] {option1} 비율 그래프2")
st.caption('하루동안 인버터 아이디별 생산 발전량 비율을 한눈에 파악 할 수있는 그래프 입니다.')

st.bar_chart(df_tmp)
    
st.markdown(" ")
st.subheader(f"[{string_date}] {option1} 데이터 확인")
st.caption('테이블 형식으로 데이터 일부분을 확인 할 수 있습니다.')

table_data = cur_data[['측정일시', '경사면일사량', '수평면일사량', '외부온도', '모듈온도', '금일발전량']].set_index('측정일시')
num = st.slider('데이터 확인할 개수', 0, len(table_data), 25)

table_columns = st.columns(2)
with table_columns[0]:
    st.caption('앞에서 부터 확인')
    st.dataframe(table_data.head(num))
with table_columns[1]:
    st.caption('뒤에서 부터 확인')
    st.dataframe(table_data.tail(num))



# 파일 다운로드
st.markdown(f"**{option1} 데이터 파일 다운로드**")
csv_data = table_data.to_csv().encode('cp949')

excel_data = BytesIO()
table_data.to_excel(excel_data)

columns = st.columns(2)
with columns[0]:
    st.download_button("🔽CSV 다운로드", csv_data, file_name=f'{option1}_data.csv')
with columns[1]:
    st.download_button("🔽엑셀 파일 다운로드", excel_data, file_name=f'{option1}_data.xlsx')

