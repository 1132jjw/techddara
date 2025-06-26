from modules.fetch_news import (
    fetch_arxiv_rss,
    fetch_hackernews_rss,
    get_article_text)
from modules.summarizer import summarize_with_gpt
from modules.idea_generator import suggest_application_idea
from modules.github_project_parser import extract_project_context_from_github

# 7. 전체 뉴스 수집 + 요약 + 아이디어 생성까지
def collect_tech_insights(project_context):
    arxiv_items = fetch_arxiv_rss(limit=3)
    for item in arxiv_items:
        item["short_summary"] = summarize_with_gpt(item["summary"])
        item["application_ideas"] = suggest_application_idea(item["short_summary"], project_context)

    hn_items = fetch_hackernews_rss(limit=3)
    for item in hn_items:
        raw = get_article_text(item["link"])
        item["raw_text"] = raw
        if raw:
            item["short_summary"] = summarize_with_gpt(raw)
        else:
            item["short_summary"] = summarize_with_gpt(item["title"])
        item["application_ideas"] = suggest_application_idea(item["short_summary"], project_context)

    return arxiv_items + hn_items

if __name__ == "__main__":
    github_url = "https://github.com/user/project"
    project_context = extract_project_context_from_github(github_url)

    all_insights = collect_tech_insights(project_context)
    for item in all_insights:
        print("\n===", item['source'].upper(), "===")
        print("[Title]", item['title'])
        print("[Link]", item['link'])
        print("[Summary]\n", item.get("short_summary") or "(요약 없음)")
        print("[적용 아이디어]\n", item.get("application_ideas") or "(아이디어 없음)")
