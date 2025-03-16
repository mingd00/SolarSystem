## 태양광 모니터링 시스템


### **목표**

전국 태양광 발전소의 분단위 발전 데이터를 활용하여 시간대별 발전량을 분석하고, 이를 시각화하여 직관적으로 확인할 수 있는 웹 대시보드 구축.

### 활용 기술 스택

**`Python(pandas, numpy)`, `Streamlit`, `pydeck`**

### 데이터

한국지역난방공사에서 제공하는 태양광 발전 csv 데이터

### 실행 화면

- **메인 페이지**: 선택한 장소, 날짜에 맞는 평균값, 최대값, 최소값 확인 및 Sidebar에서 선택한 항목들의 상관관계 확인

![image.png](attachment:b8d8b13e-2d02-4b0f-bb55-0f41cf6278fd:image.png)

- **인버터 페이지**: 인버터 전압, 전류, 전력 데이터를 그래프와 표로 확인

![image.png](attachment:214e2d58-e492-4c7a-9730-40558508e40a:image.png)

- **지도 페이지**: 선택한 날짜의 금일 발전량을 한눈에 비교

![image.png](attachment:e9f860e4-4332-4bf3-aa95-41464770fd35:image.png)

- 실행

```python
streamlit run Main.py
```
