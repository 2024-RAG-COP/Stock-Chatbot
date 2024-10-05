import openai
import config

# config.py 파일에서 OpenAI API 키 읽기
openai.api_key = config.OPENAI_API_KEY

# GPT 모델 호출
response = openai.ChatCompletion.create(
    model="gpt-4",  # 사용할 모델 (gpt-3.5-turbo, gpt-4 등)
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "gpt assistant 호출하는 코드 짜줘"},
    ]
)

# 응답 출력
print(response.choices[0].message["content"])
