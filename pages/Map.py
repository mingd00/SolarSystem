import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime
from io import BytesIO
#데이터분석===========================================================

df = pd.read_csv("./pages/data/한국지역난방공사_인버터별 분단위 태양광발전 정보_20211031.csv",encoding='cp949')

#p값 = 장소 받아오는 값
jeong='정선한교'
secheon='서천'
ham='함백'
gwang='광양항'
pa='파주지사'
gwangg='광교지사'
sejong='세종지사'
mi='미래개발원'
pan='판교가압장'
bun='분당지사'

j_l=[]; s_l=[]; h_l=[]; g_l=[]; p_l=[]; gg_l=[]; ss_l=[]; m_l=[]; pp_l=[]; b_l=[]
def day(location,d,l):
    place=df[df["장소"].str.contains(location)] 
    for i in range(23):
        if d<10:
            a='2021-10-'+'0'+str(d)+' '+str(i)+':'
            b='2021-10-'+'0'+str(d)+' '+str(i)+':59'
        else:
            a='2021-10-'+str(d)+' '+str(i)+':'
            b='2021-10-'+str(d)+' '+str(i)+':59'
        c=place[place["측정일시"].between(a,b)].groupby('인버터아이디')['인버팅후 금일발전량'].max().sum()
        l.append(c)
    for i in range(22,1,-1):
        if l[i]==0 or l[i]<l[i-1]:
            continue
        else:       
            l[i]=l[i]-l[i-1]
      


#====================================================================

st.set_page_config(layout="wide")

with st.sidebar:
    # st.title("🌏Map")
    st.subheader("Choose the Map Style")
    mapstyle = st.sidebar.selectbox('지도 스타일을 선택하세요:', 
                                    options=['Basic', 'Road', 'Light', 'Dark'],)
    st.subheader("Choose the date")
    date = st.date_input("날짜를 선택하세요", datetime.date(2022, 10, 31))
    

st.title("🌏Map")

st.subheader(f"[{date}] 전국 태양광 발전 현황")

st.write('📅Date:', date,'🎨Map Style:', mapstyle)

#시간 선택 슬라이더
time=st.slider("⌚Time", 1, 23, 13)

#time_list 생성
day(jeong,date.day,j_l)
day(secheon,date.day,s_l)
day(ham,date.day,h_l)
day(gwang,date.day,g_l)
day(pa,date.day,p_l)
day(gwangg,date.day,gg_l)
day(sejong,date.day,ss_l)
day(mi,date.day,m_l)
day(pan,date.day,pp_l)
day(bun,date.day,b_l)

#위도 값만큼 값이 올라감
map=[]
def map_value():  
    #정선한교
    for _ in range(round(j_l[time-1]/1000)+1):
        map.append([37.3958, 128.8916])
    #서천
    for _ in range(round(s_l[time-1]/1000)+1):
        map.append([36.0964, 126.6911])
    #함백
    for _ in range(round(h_l[time-1])+1):
        map.append([37.2075, 128.8916])
    #광양항
    for _ in range(round(g_l[time-1])+1):
        map.append([34.9156, 127.6813])
    #파주지사
    for _ in range(round(p_l[time-1])+1):
        map.append([37.73729084, 126.7191354])
    #광교지사
    for _ in range(round(gg_l[time-1])+1):
        map.append([37.2997, 127.0582])
    #세종지사
    for _ in range(round(ss_l[time-1])+1):
        map.append([36.4663322, 127.2453064])
    #미래개발원
    for _ in range(round(m_l[time-1])+1):
        map.append([37.2484, 127.0941])
    #판교가압장
    for _ in range(round(p_l[time-1])+1):
        map.append([37.3997, 127.1142])
    #분당지사
    for _ in range(round(b_l[time-1])+1):
        map.append([37.3675, 127.1469])

map_value()

#지도 색
if mapstyle=='Basic':
    style=None
elif mapstyle=='Road':
    style=pdk.map_styles.CARTO_ROAD
elif mapstyle=='Light':
    style=pdk.map_styles.CARTO_LIGHT
elif mapstyle=='Dark':
    style=pdk.map_styles.CARTO_DARK

chart_data = pd.DataFrame(
np.array(map),
columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=style,
    initial_view_state=pdk.ViewState(
        #위도, 경도
        latitude=35.6,
        longitude=127.8063135,
        #확대, 축소
        zoom=7,
        #기울기
        pitch=50,
    ),
    layers=[
        #hist
        pdk.Layer(  
        'HexagonLayer',
        data=chart_data,
        get_position='[lon, lat]',
        #두께
        radius=4000,
        #길이
        elevation_scale=60,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
        ),

    ],
))

#테이블 생성 

df = pd.DataFrame(
        {
            "정선한교": j_l,
            "서천": s_l,
            "함백": h_l,
            "광양항": g_l,
            "파주지사": p_l,
            "광교지사": gg_l,
            "세종지사": ss_l,
            "미래개발원": m_l,
            "판교가압장": pp_l,
            "분당지사": b_l,
        }, index=[i+1 for i in range(23)]
    ).transpose()


st.dataframe(df, use_container_width=True)

# 파일 다운로드
st.markdown(f"**[{date}] 데이터 파일 다운로드**")
csv_data = df.to_csv().encode('cp949')

excel_data = BytesIO()
df.to_excel(excel_data)

columns = st.columns(2)
with columns[0]:
    st.download_button("🔽CSV 다운로드", csv_data, file_name=f'{date}_data.csv')
with columns[1]:
    st.download_button("🔽엑셀 파일 다운로드", excel_data, file_name=f'{date}_data.xlsx')
