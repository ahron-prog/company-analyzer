# Company Analyzer Skill

This skill researches a company and provides a detailed analysis for senior tech engineers in Israel.

## Usage

Run the analysis script with a company name:

```bash
python3.12 scripts/analyze.py "Company Name"
```

## Structure

- `SYSTEM_PROMPT.md`: The prompt used by the LLM to generate the analysis.
- `schema.json`: The JSON schema for the output.
- `scripts/analyze.py`: The main script that performs web search and LLM analysis.

## Output Format

The output is a JSON object containing:
- Basic info (name, tagline, founded, etc.)
- Summary and future outlook
- Culture, workload, and remote scores (1-10)
- Team composition and compensation details
- Pros, cons, and a final verdict

## Configuration

Requires `SERP_API_KEY` and `NVIDIA_API_KEY` in `secrets.json`.
Uses `meta/llama-3.1-70b-instruct` via NVIDIA API.
