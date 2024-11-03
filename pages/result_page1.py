import streamlit as st
import time
import requests
import get_info
import os

os.environ["api_key"] = os.getenv("api_key")

####
# [전역적으로 관리하는 데이터]
# stop_regenerate = 해당 phase의 재생성 여부 선택 (아니요 버튼을 누르면 container 숨기기 위해서 정의)
if 'stop_regenerate' not in st.session_state:
    st.session_state.stop_regenerate = [False, False, False, False, False]
def changeRegenerateState(idx, b_state): st.session_state.stop_regenerate[idx] = b_state

# current_phase_num = 현재 몇번째 phase인지 저장하는 변수
if 'current_phase_num' not in st.session_state:
    st.session_state.current_phase_num = 0
def prevPhase():
    if st.session_state.current_phase_num > 0:
        st.session_state.current_phase_num -= 1
def nextPhase():
    if st.session_state.current_phase_num < 4:
        st.session_state.current_phase_num += 1

# download_button_clicked = 마지막 다운로드 버튼 관련 진행 척도를 보여주는 변수
if 'download_button_clicked' not in st.session_state:
    st.session_state.download_button_clicked = False
def on_download_button_click(): # 버튼을 클릭했을 때 실행되는 함수
    st.session_state.download_button_clicked = True  # 버튼 클릭 상태 변경

# result_data = 서버로부터 받은 데이터를 저장하는 변수
if 'result_data' not in st.session_state:
    st.session_state.result_data = [None, None, None, None, None]
def setResultData(idx, result): st.session_state.result_data[idx] = result
def getResultData(idx): return st.session_state.result_data[idx]

#####

# 현재 페이지 타이틀 지정
st.set_page_config(page_title="Financial Analyst", page_icon="📈")

# 페이지 번호/데이터 확인용
# st.write(st.session_state.current_phase_num)
# print(st.session_state.current_phase_num)
# print("RESULT_PAGE 저장된 기업명:", st.session_state.search_keyword)

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
sub_title = ["\# Phase1. 재무데이터 요약", "\# Phase2. 기업관련 뉴스 수집 및 요약", 
             "\# Phase3. 시장 및 산업관련 뉴스 수집 및 요약", "\# Phase4. 종합보고서 작성", 
             "\# Phase5. 데이터 시각화 및 추가분석 방향 제공"]

st.subheader(sub_title[st.session_state.current_phase_num], divider='gray')

if st.session_state.result_data[st.session_state.current_phase_num] is None:
    datas = {
        'phaseNum': st.session_state.current_phase_num
    }
    result_data = requests.post(st.session_state.request_url+"getNextAnalysis", data=datas)
    # st.write("main")
    setResultData(st.session_state.current_phase_num, result_data)


# 생성형 답변 입력 공간
with st.container(height=450):
    # st.write_stream("생성형 답변 넣는 곳")
    data = getResultData(st.session_state.current_phase_num)
    st.write(data)
    get_info.main(data,"Claude", os.environ["api_key"],"claude-3-5-sonnet-20240620")

# 페이지 이동 버튼
left, middle, right = st.columns(3)
st.markdown("""
            <style>
            .stButton {
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)
left.button("이전", on_click=prevPhase)

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
        
        for idx, page in enumerate(pageList):
            if idx == st.session_state.current_phase_num:
                page.write(":red[o]")
            else:
                page.write("o")
        
        charP.write(":green[P]")
        
right.button("다음", on_click=nextPhase)


# 추가 생성 여부 선택 버튼
if st.session_state.stop_regenerate[st.session_state.current_phase_num] == False:
    x = st.empty()

    with st.container():
        st.text("")
        st.text("")
        st.text("")

        col_q, col_y, col_n = st.columns([2,0.2,0.4], vertical_alignment="center")         
        
        col_q.write("해당 Phase의 분석을 다시 진행할까요?")

        if col_y.button("네",type="primary", on_click=lambda:changeRegenerateState(st.session_state.current_phase_num, False)):
            print(f"{st.session_state.current_phase_num+1} phase 답변 재생성")
            result_data = requests.post(st.session_state.request_url+"retryAnalysis")
            setResultData(st.session_state.current_phase_num, result_data)

        if col_n.button("아니요",type="secondary", on_click=lambda:changeRegenerateState(st.session_state.current_phase_num, True)):
            print(f"{st.session_state.current_phase_num+1} phase 답변 재생성 기능 차단")
            
            
# [기능삭제] 마지막 페이지인 경우 다운로드 버튼 생성
# if st.session_state.current_phase_num == 4:
#     with st.container():
#         col_q, col_btn = st.columns([2,0.5], vertical_alignment="center")         
        
#         col_q.write("지금까지의 분석보고서를 저장할까요?")
        
#         def generate_pdf():
#             """Generate an example pdf file and save it to example.pdf"""
#             from fpdf import FPDF

#             pdf = FPDF()
#             pdf.add_page()
#             pdf.set_font("Arial", size=12)
#             pdf.cell(200, 10, txt="Welcome to Streamlit!", ln=1, align="C")
#             pdf.output(f"{st.session_state.search_keyword}_example.pdf")
#             time.sleep(1) #스피너 확인용 시간지연
            
#         # 버튼 상태에 따라 UI 변경         
#         if st.session_state.download_button_clicked:
#             with st.spinner("작업을 수행 중입니다... 잠시만 기다려 주세요."):
#                 generate_pdf()
#             with open(f"{st.session_state.search_keyword}_example.pdf", "rb") as f:
#                 col_btn.download_button("Download pdf", f, f"{st.session_state.search_keyword}_example.pdf")
#         else:
#             if col_btn.button("Generate PDF", on_click=on_download_button_click):
#                 pass