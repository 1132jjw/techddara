import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 5. OpenAI GPT로 내 프로젝트에 적용할 아이디어 생성
def suggest_application_idea(summary, project_context, model="gpt-4.1-nano-2025-04-14"):
    prompt = f"""
    [내 프로젝트 설명]
    {project_context}

    [요약된 기술 뉴스]
    {summary}

    위 기술을 내 프로젝트에 적용할 수 있는 방법을 3가지 제안해줘.
    각 아이디어는 한 문단으로, 적용 난이도(1~5)와 기대 효과도 함께 포함해줘.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"아이디어 생성 실패: {e}"