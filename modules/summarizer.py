import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 4. OpenAI GPT로 뉴스 요약 생성
def summarize_with_gpt(text, model="gpt-4.1-nano-2025-04-14"):
    prompt = f"""
    다음은 기술 뉴스 또는 논문의 본문 내용이야. 핵심 내용을 3줄 이내로 요약해줘:

    {text}
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"요약 실패: {e}"