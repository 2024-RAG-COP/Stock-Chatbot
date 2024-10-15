import streamlit as st

# [전역적으로 관리하는 데이터]
# stop_regenerate = 해당 phase의 재생성 여부 선택 (아니요 버튼을 누르면 container 숨기기 위해서 정의)
if 'stop_regenerate' not in st.session_state:
    st.session_state.stop_regenerate = False
def changeRegenerateState(b_state): st.session_state.stop_regenerate = b_state

# stop_regenerate = 해당 phase의 재생성 여부 선택 (아니요 버튼을 누르면 container 숨기기 위해서 정의)
if 'current_phase_num' not in st.session_state:
    st.session_state.current_phase_num = 1
def changeCurrentPhaseNum(num): st.session_state.current_phase_num = num

# 현재 페이지 타이틀 지정
st.set_page_config(page_title="Financial Analyst", page_icon="📈")


# 로고, 검색한 기업명 배치
col1, col2 = st.columns([1, 6], vertical_alignment="center") 
with col1:
    st.image("images/title.svg", width=100)
with col2:
    st.markdown("""
    <style>

    .stTextInput label {
        display: none;
    }

    </style>
    """, unsafe_allow_html=True)
    st.text_input("", value=st.session_state.search_keyword, disabled=True)

# 현재 Phase 설명
st.subheader("\# Phase1. 재무데이터 요약", divider='gray')

# 생성형 답변 입력 공간
with st.container(height=450):
    long_text = "Lorem ipsum. " * 1000
    st.write(long_text)
    # st.write_stream("생성형 답변 넣는 곳")
    
    # 추가 생성 여부 선택 버튼
    if st.session_state.stop_regenerate == False:
        x = st.empty()

        with st.container():
            col_q, col_y, col_n = st.columns([2,0.2,0.4], vertical_alignment="center")         
            
            col_q.write("해당 Phase의 분석을 다시 진행할까요?")

            if col_y.button("네",type="primary"):
                changeRegenerateState(False)
                print("답변 재생성")
            if col_n.button("아니요",type="secondary"):
                changeRegenerateState(True)


# 페이지 이동 버튼
left, middle, right = st.columns(3)

left.button("이전")
with middle:
    page_container = st.container()
    with page_container:
        pageList = list()
        charC, page1, page2, page3, page4, page5, charP = st.columns([0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05], vertical_alignment="center") 

        pageList.append(page1)
        pageList.append(page2)
        pageList.append(page3)
        pageList.append(page4)
        pageList.append(page5)

        charC.write(":blue[C]")
        for page in pageList:
            page.write("o")
        charP.write(":green[P]")
right.button("다음")