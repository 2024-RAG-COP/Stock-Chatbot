import requests

# API 엔드포인트 URL
url = "http://127.0.0.1:8000/getCompanyAnalysis/"

# 업로드할 파일 열기
file = {'file': open('example.txt', 'rb')}
form_data = {
    "company": "This is a company"
}
# POST 요청으로 파일 전송하기
response = requests.post(url, files=file, data=form_data)

# 응답 상태 코드 확인
print(f"Status Code: {response.status_code}")

# 응답 본문 확인
if response.status_code == 200:
    print("File uploaded successfully.")
else:
    print(f"Error: {response.status_code}")
