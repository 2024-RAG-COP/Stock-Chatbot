from openai import OpenAI
import config
import time

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=config.OPENAI_API_KEY)

# HTML 파일 업로드
def upload_html(file_path):
    """HTML 파일을 OpenAI에 업로드하고 파일 ID를 반환"""
    response = client.files.create(
        purpose='assistants',  # 파일의 용도를 지정
        file=open(file_path, "rb")
    )
    print(f"Uploaded HTML file with ID: {response.id}")
    return response.id

# 대화 쓰레드 생성 (HTML 파일 첨부)
def create_thread_with_html(assistant_id, html_file_id):
    """HTML 파일이 첨부된 대화 쓰레드를 생성"""
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Please analyze the attached HTML file.",
                "file_ids": [html_file_id]  # 업로드한 HTML 파일 ID 첨부
            }
        ]
    )
    print(f"Thread created with ID: {thread.id}")
    return thread

# Assistant 실행
def run_assistant_with_html(thread, assistant_id):
    """HTML 파일이 포함된 대화 쓰레드로 Assistant 실행"""
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        model="gpt-4-0613"  # 최신 모델 사용
    )
    print(f"Assistant run started with ID: {run.id}")
    return run

# 대화 쓰레드에 새로운 메시지 추가 및 Assistant 실행
def add_message_and_run(thread, assistant_id, user_message):
    """대화 쓰레드에 사용자 메시지 추가 및 Assistant 실행"""
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        model="gpt-4-0613"  # 최신 모델 사용
    )
    return run

# 대화 쓰레드의 응답 메시지 가져오기
def get_messages(thread_id):
    """대화 쓰레드의 모든 메시지를 가져와서 출력"""
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for message in messages.data:
        for content_item in message.content:
            if hasattr(content_item, "text"):
                print(f"{message.role}: {content_item.text.value}")

# 메인 실행 함수
def main():
    # HTML 파일 경로 및 Assistant ID 설정
    html_file_path = "nvda-20240728.html"  # 분석할 HTML 파일 경로
    assistant_id = "asst_KFWoVs5ISpfiI7aTvzD5b9Ag"  # 미리 생성한 Assistant ID 사용

    # HTML 파일 업로드 및 파일 ID 가져오기
    html_file_id = upload_html(html_file_path)

    # HTML 파일이 포함된 대화 쓰레드 생성
    thread = create_thread_with_html(assistant_id, html_file_id)

    # Assistant 실행 및 결과 확인
    run = run_assistant_with_html(thread, assistant_id)

    # Assistant 응답이 완료될 때까지 대기
    while run.status not in ['completed', 'failed']:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Current status: {run.status}")
        time.sleep(1)

    # 대화 메시지 출력
    get_messages(thread.id)

    # 사용자와 지속적인 상호작용을 위한 반복문
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        # 사용자 메시지 추가 및 Assistant 실행
        run = add_message_and_run(thread, assistant_id, user_input)

        # Assistant 응답이 완료될 때까지 대기
        while run.status not in ['completed', 'failed']:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Current status: {run.status}")
            time.sleep(1)

        # 응답 메시지 가져오기 및 출력
        get_messages(thread.id)

# 메인 함수 실행
if __name__ == "__main__":
    main()
