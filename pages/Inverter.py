
import pandas as pd
import math
import streamlit as st

#--------------------------------------데이터 받기------------------------------------

df = pd.read_csv("./pages/data/한국지역난방공사_인버터별 분단위 태양광발전 정보_20211031.csv",
                encoding='cp949')
df.set_index("측정일시", inplace = True)

#--------------------------------------다운로드할때 csv로------------------------------------
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

#--------------------------------------페이지 최대로 늘리기------------------------------------

st.set_page_config(layout="wide")

#--------------------------------------사이드바------------------------------------
st.sidebar.markdown("## 장소선택")
add_selectbox = st.sidebar.selectbox(
    "장소를 선택하여 주세요",
    ('정선한교', '서천태양광발전소', '함백태양광발전소', 
                        '광양항 제1자전거도로 태양광발전소', '광양항 제2자전거도로 태양광발전소',
                        '광양항 제3자전거도로 태양광발전소', '파주지사 태양광발전소', '광교지사 태양광발전소',
                        '세종지사 제1호 태양광발전소', '미래개발원 태양광발전소', '판교가압장 태양광발전소',
                        '분당지사 제1호 주차장 태양광발전소', '분당지사 제2호 주차장 태양광발전소'), index=4
)

#--------------------------------------전압 RST상 구하기------------------------------------
df_place = df[df['장소'] == add_selectbox]

def maxd(date, tom):
    df_202110 = df[(df.index > f"2021-10-{date}") & (df.index < f"2021-10-{tom}")]
    df_maxs = df_202110[df_202110['장소'] == add_selectbox]
    df_chartr = df_tableR = df_maxs['인버터전압(R상)'].max()
    df_charts = df_tableS = df_maxs['인버터전압(S상)'].max()
    df_chartt = df_tableT = df_maxs['인버터전압(T상)'].max()
    df_chartr2 = df_tableR2 = df_maxs['인버터전류(R상)'].max()
    df_charts2 = df_tableS2 = df_maxs['인버터전류(S상)'].max()
    df_chartt2 = df_tableT2 = df_maxs['인버터전류(T상)'].max()
    df_charty3 = df_tabley3 = df_maxs['유효전력(종합)'].max()
    df_chartn3 = df_tablen3 = df_maxs['무효전력(종합)'].max()
    
    return df_chartr, df_charts, df_chartt, df_tableR, df_tableS, df_tableT, df_chartr2, df_charts2, df_chartt2, df_tableR2, df_tableS2, df_tableT2, df_charty3, df_tabley3, df_chartn3, df_tablen3
    

df_INPC = [[None,None,None]]
df_INPT = []
df_INWC = [[None, None, None]]
df_INWT = []
df_FINAL = []
df_ch = []
df_tb = []
for date in range(1,32,1):
    tom = date + 1
    if date < 9 != 0:
        date = '0' + str(date)
        tom = '0'+ str(tom)
        chartR, chartS, chartT, tableR, tableS, tableT, chartR2, chartS2, chartT2, tableR2, tableS2, tableT2, charty3, tabley3, chartn3, tablen3 = maxd(date,tom)
        p = tabley3**2 + tablen3**2
        df_p = math.sqrt(p)
        df_INPC.append([chartR, chartS, chartT])
        df_INPT.append([tableR, tableS, tableT])
        df_INWC.append([chartR2, chartS2, chartT2])
        df_INWT.append([tableR2, tableS2, tableT2])
        df_ch.append([charty3, chartn3, df_p])
        df_tb.append([tabley3, tablen3, df_p])

    elif date == 9:
        date = '0' + str(date)
        chartR, chartS, chartT, tableR, tableS, tableT, chartR2, chartS2, chartT2, tableR2, tableS2, tableT2, charty3, tabley3, chartn3, tablen3 = maxd(date,tom)
        p = tabley3**2 + tablen3**2
        df_p = math.sqrt(p)
        df_INPC.append([chartR, chartS, chartT])
        df_INPT.append([tableR, tableS, tableT])
        df_INWC.append([chartR2, chartS2, chartT2])
        df_INWT.append([tableR2, tableS2, tableT2])
        df_ch.append([charty3, chartn3, df_p])
        df_tb.append([tabley3, tablen3, df_p])
        
    elif tom == 32:
        df_20211031 = df_place.loc[df_place.index > "2021-10-31"]
        chartR = df_20211031['인버터전압(R상)'].max()
        chartS = df_20211031['인버터전압(S상)'].max()
        chartT = df_20211031['인버터전압(T상)'].max()

        tableR = df_20211031['인버터전압(R상)'].max()
        tableS = df_20211031['인버터전압(S상)'].max()
        tableT = df_20211031['인버터전압(T상)'].max()

        charty3 = tabley3 = df_20211031['유효전력(종합)'].max()
        chartn3 = tablen3 = df_20211031['무효전력(종합)'].max()

        p = tabley3**2 + tablen3**2
        df_p = math.sqrt(p)

        df_INPC.append([chartR, chartS, chartT])
        df_INPT.append([tableR, tableS, tableT])
        df_INWC.append([chartR2, chartS2, chartT2])
        df_INWT.append([tableR2, tableS2, tableT2])
        df_ch.append([charty3, chartn3, df_p])
        df_tb.append([tabley3, tablen3, df_p])

    else:
        chartR, chartS, chartT, tableR, tableS, tableT, chartR2, chartS2, chartT2, tableR2, tableS2, tableT2, charty3, tabley3, chartn3, tablen3 = maxd(date,tom)
        p = tabley3**2 + tablen3**2
        df_p = math.sqrt(p)
        df_INPC.append([chartR, chartS, chartT])
        df_INPT.append([tableR, tableS, tableT])
        df_INWC.append([chartR2, chartS2, chartT2])
        df_INWT.append([tableR2, tableS2, tableT2])
        df_ch.append([charty3, chartn3, df_p])
        df_tb.append([tabley3, tablen3, df_p])
       
st.title("INVERTER🧈")
st.subheader(f'{add_selectbox} Chart')

#--------------------------------------탭------------------------------------

tab1, tab2, tab3 = st.tabs(["인버터 전압", "인버터 전류", "유무전력"])

#--------------------------------------tab1그래프------------------------------------
with tab3:
    chart_data = pd.DataFrame(df_INPC, columns=['R상', 'S상', 'T상'])
    table_data = pd.DataFrame(df_INPT, columns=['R상(전압)', 'S상(전압)', 'T상(전압)'])

    st.line_chart(chart_data)
    
with tab2:
    chart_data2 = pd.DataFrame(df_INWC, columns=['R상', 'S상', 'T상'])
    table_data2 = pd.DataFrame(df_INWT, columns=['R상(전류)', 'S상(전류)', 'T상(전류)'])

    st.line_chart(chart_data2)

with tab1:
    chart_data3 = pd.DataFrame(df_ch, columns=['유효전력', '무효전력', '피상전력'])
    table_data3 = pd.DataFrame(df_tb, columns=['유효전력', '무효전력', '피상전력'])

    st.line_chart(chart_data3)

#-------------------------------------- tab1표 ------------------------------------
st.subheader(f'{add_selectbox} Table')
col1, col2, col3 = st.columns(3)
with col1:
    st.write('인버터 전압')
#st.checkbox("창 크기에 맞추기", value=False, key="use_container_width")
    st.dataframe(table_data, use_container_width=True)
with col2:
    st.write('인버터 전류')
    #st.checkbox("창 크기에 맞추기", value=False, key="use_container_width2")
    st.dataframe(table_data2, use_container_width=True)
with col3:
    st.write('유*무전력')
    #st.checkbox("창 크기에 맞추기", value=False, key="use_container_width2")
    st.dataframe(table_data3, use_container_width=True)
    
df_final = pd.concat([table_data, table_data2, table_data3], axis=1)   
csv = convert_df(df_final)

st.download_button(
    label="🔽CSV파일로 다운로드",
    help="Download data as CSV",
    data=csv,
    file_name=f'{add_selectbox}.csv',
    mime='text/csv',
)

