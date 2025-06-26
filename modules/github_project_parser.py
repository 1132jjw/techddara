import tempfile
import subprocess
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 6. GitHub 주소로부터 프로젝트 맥락 요약
def extract_project_context_from_github(github_url, model="gpt-4.1-nano-2025-04-14"):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(["git", "clone", github_url, tmpdir], check=True)
            readme_path = os.path.join(tmpdir, "README.md")
            req_path = os.path.join(tmpdir, "requirements.txt")
            tree = subprocess.run(["tree", tmpdir, "-L", "2"], capture_output=True, text=True).stdout

            readme = open(readme_path).read() if os.path.exists(readme_path) else ""
            requirements = open(req_path).read() if os.path.exists(req_path) else ""

            prompt = f"""
            [README.md]
            {readme}

            [requirements.txt]
            {requirements}

            [디렉토리 구조]
            {tree}

            위 정보를 기반으로 이 프로젝트가 어떤 목표를 가지고 어떤 기술로 구성되어 있는지 요약해줘. 핵심 기술 키워드도 함께 알려줘.
            """
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
    except Exception as e:
        return f"프로젝트 맥락 추출 실패: {e}"