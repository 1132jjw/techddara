import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from techddara.modules.tech_agent import collect_tech_insights
from modules.github_project_parser import extract_project_context_from_github

st.set_page_config(page_title="Tech지기: 기술 뉴스 적용 아이디어 제안기", layout="wide")
st.title("🧠 Tech지기")
st.markdown("""
최신 기술 뉴스와 논문을 수집하고, GitHub 프로젝트에 어떻게 적용할 수 있을지 GPT가 아이디어를 제안해드립니다.
""")

# .env 로드
load_dotenv()
def init_client(api_key):
    return OpenAI(api_key=api_key)

# OpenAI API 키 입력
api_key = st.text_input("🔑 OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")

# GitHub URL 입력
github_url = st.text_input("📎 분석할 GitHub 프로젝트 URL을 입력하세요")

if st.button("🚀 분석 시작"):
    if not api_key or not github_url:
        st.error("API 키와 GitHub URL을 모두 입력해주세요.")
    else:
        client = init_client(api_key)

        with st.spinner("프로젝트 맥락 분석 중..."):
            project_context = extract_project_context_from_github(github_url)
        st.subheader("🧾 프로젝트 요약")
        st.code(project_context, language="markdown")

        with st.spinner("기술 뉴스 수집 및 적용 아이디어 생성 중..."):
            insights = collect_tech_insights(project_context)

        st.subheader("📰 기술 뉴스 및 적용 아이디어")
        for item in insights:
            with st.expander(f"{item['title']} [{item['source']}]"):
                st.markdown(f"**링크:** [{item['link']}]({item['link']})")
                st.markdown("**요약:**")
                st.info(item.get("short_summary") or "(요약 없음)")
                st.markdown("**적용 아이디어:**")
                st.success(item.get("application_ideas") or "(아이디어 없음)")