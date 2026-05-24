# Company Analyzer

Analyze tech companies for senior engineers in Israel. Provides detailed profiles on culture, workload, remote policy, and compensation.

## Usage

```bash
python3 scripts/analyze.py "Company Name"
```

## Features

- **Comprehensive Research**: Uses SerpAPI to gather real-time data from Glassdoor, LinkedIn, and news.
- **Senior-Focused**: Tailored for senior engineers in the Israeli market.
- **Visual Profile**: Includes scores for culture, workload, and remote flexibility.
- **Verdict**: Provides a clear recommendation (Good/Mixed/Bad) for applicants.

## Configuration

Requires `SERP_API_KEY` and `ANTHROPIC_API_KEY` in `secrets.json`.

## UI

The `ui/index.html` file provides a clean, interactive interface for the analyzer.

<!-- Updated by Liloosh -->
