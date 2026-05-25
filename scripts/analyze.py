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

def get_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "SYSTEM_PROMPT.md")
    with open(prompt_path, "r") as f:
        return f.read()

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
        f"{company_name} engineering culture tech stack",
        f"{company_name} salary range senior software engineer Israel"
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
    
    system_prompt = get_system_prompt()

    user_prompt = f"""Research this company for a senior Israeli tech engineer: {company_name}
    
Search Results:
{json.dumps(search_results, indent=2)}

Follow the instructions in the system prompt and return the JSON object."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2500,
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
