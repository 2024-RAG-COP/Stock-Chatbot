import streamlit as st
import os
from streamlit_extras.stylable_container import stylable_container

# API KEY 관리 (로컬/streamlit)
# os.environ["OPENAI_API_KEY"] = os.getenv("openai_api_key")
# os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]

# 언어모델 관련 import 정리
#
#



# 전역적으로 관리하는 데이터
# current_page = 현재 페이지 지칭
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"
    
# 페이지 이동 함수
def changepage(name): st.session_state.current_page = name

# 메인 사이트 이름
st.set_page_config(page_title="Financial Analyst", page_icon="📈")

# 메인 검색화면
if st.session_state.current_page == "main":
    # 제목 스타일 적용
    st.markdown("""
    <style>
    h1 {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    st.title(":blue[F]inancial :blue[A]nalyst")
    
    # 검색창 스타일 (세로정렬 스타일) 적용
    st.markdown("""
    <style>
    .block-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;  /* 요소들의 수직 정렬을 가운데로 */
    }
    .element-container {
        flex: 1;  /* 요소 크기 맞추기 */
        margin: 10px;  /* 요소 간 간격 추가 */
    }
    .stTextInput label {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1]) 
    with col1:
        search_text = st.text_input(" ", placeholder="분석하고 싶은 기업을 입력해주세요")
    with col2:
        st.button("🔍")
        


    col1, col2 = st.columns(2) 
    with col1:
        # HTML과 CSS를 사용하여 tooltip 스타일 정의
        st.markdown("""
            <style>
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
                top: -30px;
                /* color: blue; */
                /* text-decoration: underline; */
            }

            .tooltip .tooltiptext {
                visibility: hidden;
                padding: 100px;
                width: 400px;
                background-color: black;
                color: #fff;
                border-radius: 5px;
                padding: 20px;
                position: absolute;
                z-index: 1;
                left: 120%;
                opacity: 20%;
                transition: opacity 0.3s;
            }

            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            </style>
            """, unsafe_allow_html=True)

        # HTML로 tooltip을 포함한 텍스트 삽입
        st.markdown("""
            <div class="tooltip">❓무엇을 분석하나요?
                <span class="tooltiptext">
                    <b>다음과 같은 내용을 분석하고 제공합니다.</b> <br/>
                    <br/>
                    1. 재무데이터 요약<br/>
                    2. 기업관련 뉴스 수집 및 요약<br/>
                    3. 시장 및 산업관련 뉴스 수집 및 요약<br/>
                    4. 종합보고서 작성<br/>
                    5. 데이터 시각화 및 추가분석 방향 제공<br/>
                </span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
           
        col_title, col_btn = st.columns(2) 
        with col_title:
            st.write("➕재무재표 업로드")
            css = '''
            <style>
                p {
                    margin: 5px 0px 1rem;
                }
            </style>
            '''

            st.markdown(css, unsafe_allow_html=True)
        with col_btn:
            st.file_uploader("")

            css = '''
                <style>
                [data-testid='stWidgetLabel'] {
                    display: none;
                }
                [data-testid='stFileUploader'] {
                    width: max-content;
                }
                [data-testid='stFileUploader'] section {
                    padding: 0;
                    float: left;
                }
                [data-testid='stFileUploader'] section > input + div {
                    display: none;
                }
                [data-testid='stFileUploader'] section + div {
                    float: right;
                    padding-top: 0;
                }

            </style>
            '''

            st.markdown(css, unsafe_allow_html=True)


    # 스타일 적용 다른 방법 참고
    # st.markdown(
    #     '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
    #     unsafe_allow_html=True,
    # )
    # with stylable_container(
    #     key="container_with_border",
    #     css_styles=r"""
    #         button p:before {
    #             font-family: 'Font Awesome 5 Free';
    #             content: '\f1c1';
    #             display: inline-block;
    #             padding-right: 3px;
    #             vertical-align: middle;
    #             font-weight: 900;
    #         }
    #         """,
    # ):
    #     st.button("Button with icon")
        
    st.button("페이지이동", on_click=lambda :changepage("test"))


elif st.session_state.current_page == "test": 
    st.title("테스트")
    st.button("페이지이동", on_click=lambda :changepage("main"))