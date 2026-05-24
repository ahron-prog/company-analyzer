import os
import sys
import json
import argparse
from serpapi import GoogleSearch
import anthropic

def get_secrets():
    secrets_path = "/home/ubuntu/.nanobot/workspace/secrets.json"
    with open(secrets_path, "r") as f:
        return json.load(f)

def research_company(company_name):
    secrets = get_secrets()
    serp_key = secrets.get("SERP_API_KEY")
    anthropic_key = secrets.get("ANTHROPIC_API_KEY")
    
    if not serp_key or not anthropic_key:
        print("Error: Missing API keys in secrets.json")
        sys.exit(1)

    # 1. Search for company info
    search_queries = [
        f"{company_name} company profile careers Israel",
        f"{company_name} Glassdoor reviews Israel",
        f"{company_name} recent news layoffs funding",
        f"{company_name} engineering culture tech stack"
    ]
    
    search_results = []
    for query in search_queries:
        search = GoogleSearch({
            "q": query,
            "api_key": serp_key,
            "num": 5
        })
        res = search.get_dict()
        if "organic_results" in res:
            for r in res["organic_results"]:
                search_results.append({
                    "title": r.get("title"),
                    "link": r.get("link"),
                    "snippet": r.get("snippet")
                })

    # 2. Analyze with LLM
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    system_prompt = """You are a senior tech job market analyst helping Israeli senior engineers evaluate companies before applying.
Return ONLY valid JSON (no markdown, no explanation)."""

    user_prompt = f"""Research this company for a senior Israeli tech engineer: {company_name}
    
Search Results:
{json.dumps(search_results, indent=2)}

Return JSON in this exact structure:
{{
  "name": "Company Name",
  "tagline": "One sentence what they do",
  "founded": "Year",
  "employees": "e.g. 1,200 globally / 400 in Israel",
  "hq": "City, Country",
  "type": "Public / Private / Startup",
  "stage": "e.g. Series C / Public / Bootstrapped",
  "sector": "e.g. Cybersecurity / SaaS / Fintech",
  "israeliRD": true,
  "summary": "2-3 sentences about what the company does",
  "future": "2-3 sentences about growth trajectory",
  "culture": {{
    "score": 1-10,
    "description": "2-3 sentences about work culture",
    "tags": ["Fast-paced", "Autonomous"] 
  }},
  "workload": {{
    "score": 1-10,
    "description": "2-3 sentences about work hours",
    "tags": ["Stable hours"] 
  }},
  "remote": {{
    "score": 1-10,
    "policy": "Hybrid 2 days/week",
    "description": "1-2 sentences about flexibility"
  }},
  "team": {{
    "description": "2-3 sentences about team composition",
    "tags": ["Strong seniors"]
  }},
  "compensation": {{
    "seniorRange": "40,000–55,000 NIS/month",
    "equity": "RSUs typical",
    "benefits": "Key benefits"
  }},
  "pros": ["Pro 1", "Pro 2"],
  "cons": ["Con 1", "Con 2"],
  "verdict": "good or mixed or bad",
  "verdictText": "1-2 sentence overall verdict",
  "glassdoor": 3.5,
  "sources": ["brief notes"]
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("company", help="Company name to analyze")
    args = parser.parse_args()
    
    result = research_company(args.company)
    print(result)