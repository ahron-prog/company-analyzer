import os
import sys
import json
import argparse
from serpapi import GoogleSearch
from openai import OpenAI

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
    nvidia_key = secrets.get("NVIDIA_API_KEY")
    
    if not serp_key or not nvidia_key:
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
        try:
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
        except Exception as e:
            print(f"Search error for query '{query}': {e}")

    # 2. Analyze with LLM (using NVIDIA API)
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=nvidia_key
    )
    
    system_prompt = get_system_prompt()

    user_prompt = f"""Research this company for a senior Israeli tech engineer: {company_name}
    
Search Results:
{json.dumps(search_results, indent=2)}

Follow the instructions in the system prompt and return the JSON object."""

    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        top_p=0.7,
        max_tokens=2048,
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("company", help="Company name to analyze")
    args = parser.parse_args()
    
    result = research_company(args.company)
    # Clean up potential markdown code blocks
    if result.startswith("```json"):
        result = result[7:]
    if result.endswith("```"):
        result = result[:-3]
    print(result.strip())
