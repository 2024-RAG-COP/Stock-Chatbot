import requests
import re
import json
import base64
import streamlit as st


CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"


def analyze_and_structure_content(content, api_choice, api_key, model):
    prompt = f"""
다음 재무제표 또는 기업 정보를 분석하고 4-6개의 주요 포인트나 주제를 식별하세요: 
<content>
{content}
</content>
각 주요 포인트에 대해:
a) 핵심 재무 지표나 기업 정보를 2-3문장으로 요약하세요.
b) 관련된 하위 재무 항목이나 세부 정보를 2-3개 나열하세요.
c) 가능한 경우, 업계 평균이나 경쟁사와의 비교를 1-2개 제공하세요.
d) 관련된 재무 용어나 중요 비즈니스 개념을 1-2개 포함하세요.
e) 해당 포인트와 관련된 짧은 재무 분석, 주요 통계, 또는 투자 팁을 제안하세요.
각 포인트에 대해 200x150 픽셀 크기의 재무 차트나 그래프를 제안하세요. 데이터의 특성에 따라 적절한 시각화 방법(예: 막대 그래프, 선 그래프, 원 그래프, 트리맵 등)을 선택하세요.
포인트들을 재무제표의 논리적 순서(예: 수익, 비용, 이익, 자산, 부채, 자본)나 기업 정보의 중요도에 따라 배열하고, 각 포인트에 적절한 재무 아이콘이나 심볼을 제안하세요.
<thinking> 태그를 사용하여 당신의 재무 분석 과정과 선택한 시각화 방법에 대한 근거를 설명하세요. 특히 재무제표나 기업 정보에서 중요한 트렌드나 패턴을 어떻게 강조했는지 설명하세요.
최종 구조를 JSON 형식으로 제공하세요. 이 JSON은 복잡하고 정보가 풍부한 단일 페이지 재무 인포그래픽을 생성하는 데 사용될 것입니다.
목표는 주어진 재무제표나 기업 정보를 바탕으로 포괄적이고 시각적으로 매력적인 재무 인포그래픽 구조를 만드는 것입니다. 데이터의 복잡성과 깊이에 따라 적절히 조정하세요. 투자자나 이해관계자들이 한눈에 기업의 재무 상태나 성과를 이해할 수 있도록 정보를 구조화하고 시각화하세요.
"""
    if api_choice == "Claude":
        return call_claude_api(prompt, api_key, model)


def call_claude_api(prompt, api_key, model):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "anthropic-version": "2023-06-01",
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.9,
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        raise Exception(
            f"Claude API 호출 실패. 상태 코드 {response.status_code}: {response.text}"
        )


def generate_html_infographic(structure_json, api_choice, api_key, model):
    prompt = f"""
1. 다음 JSON 구조를 바탕으로 HTML 슬라이드를 생성하세요:
<json>
{structure_json}
</json>

2. 다음 사양에 따라 HTML 코드를 작성하세요:
   - Tailwind CSS를 스타일링에 사용하세요 (Tailwind CSS CDN 포함)
   - 1200x900 픽셀 크기의 고정 레이아웃으로 설계하세요. 필요한 경우 스크롤 가능하게 만드세요.
   - 에어비엔비 컬러 스타일을 적용하세요.
   - Lucide 아이콘을 적절히 활용하세요
   - 각 섹션에 제안된 시각적 요소(차트, 다이어그램, 아이콘 등)를 포함하세요
   - 내용의 복잡성에 따라 적절한 레이아웃과 디자인 복잡도를 선택하세요

3. 콘텐츠 가이드라인:
   - 주요 포인트를 명확하게 강조하세요
   - 텍스트와 시각적 요소의 균형을 맞추세요
   - 필요한 경우 계층 구조를 사용하여 정보를 조직화하세요
   - 슬라이드의 전체적인 흐름과 가독성을 고려하세요

4. 최종 HTML 코드를 제공하세요. 전체 HTML 코드를 <html_code> 태그 안에 넣으세요.

목표는 주어진 내용을 바탕으로 정보가 풍부하고 시각적으로 매력적인 슬라이드를 생성하는 것입니다. 내용의 성격과 복잡성에 따라 적절히 조정하세요.
"""
    if api_choice == "Claude":
        return call_claude_api(prompt, api_key, model)


def clean_html(html_content):
    html_content = re.sub(r"```html\s*", "", html_content)
    html_content = re.sub(r"```\s*$", "", html_content)
    return html_content.strip()


def get_binary_file_downloader_html(bin_file, file_label="File"):
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">다운로드 {file_label}</a>'
    return href


def main(content, api_choice="Claude", api_key="", model="claude-3-5-sonnet-20240620"):
    try:
        with st.spinner("내용 분석 및 구조화 중..."):
            structure_result = analyze_and_structure_content(
                content, api_choice, api_key, model
            )

        st.subheader("1단계: 내용 분석 및 구조화")
        st.write(structure_result)

        structure_json = re.search(r"\{.*\}", structure_result, re.DOTALL)
        if structure_json:
            structure_json = structure_json.group()

            with st.spinner("HTML 인포그래픽 생성 중..."):
                html_result = generate_html_infographic(
                    structure_json, api_choice, api_key, model
                )

            st.subheader("2단계: HTML 인포그래픽 생성")
            html_code = clean_html(html_result)
            st.code(html_code, language="html")

            st.components.v1.html(html_code, height=600, scrolling=True)

            # HTML 파일 저장 및 다운로드 링크 생성
            with open("infographic.html", "w", encoding="utf-8") as f:
                f.write(html_code)

            st.markdown(
                get_binary_file_downloader_html("infographic.html", "infographic.html"),
                unsafe_allow_html=True,
            )
        else:
            st.error("구조화된 JSON을 찾을 수 없습니다. 다시 시도해 주세요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
