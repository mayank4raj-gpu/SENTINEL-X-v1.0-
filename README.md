# SENTINEL-X 🛡️

Mobile-friendly Streamlit URL heuristic analyzer with optional AWS Strands Agent explanation. **Offline scanner is functional. AI requires your own AWS Bedrock account and credentials.** This is not a certified security scanner or a malware verdict.

## Run in GitHub Codespaces (Android browser)
1. Create a private GitHub repository; upload this project's extracted files (including `analyzer.py`, `app.py`, `ai_agent.py`, `requirements.txt`, `.streamlit/config.toml`). Do not upload secrets.
2. In GitHub repository: **Code → Codespaces → Create codespace**. Chrome Desktop site may help.
3. In terminal:
   ```bash
   python -m pip install -r requirements.txt
   python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```
4. Open forwarded **Port 8501** from Codespaces Ports tab. Keep port **Private**. Try `https://example.com`.
5. Stop app with Ctrl+C; stop Codespace when done to avoid quota use.

## Optional AWS Strands + Amazon Bedrock
Requires an eligible AWS account, permitted Bedrock model, region, credentials and potentially paid usage. Check age requirements and obtain guardian support if applicable. Never bypass verification. **AWS model requests may cost money.**

1. Install: `python -m pip install -r requirements-ai.txt`
2. Set `ENABLE_AWS_AI=1`, `BEDROCK_MODEL_ID=<your-enabled-model-id>`, and `AWS_DEFAULT_REGION=<your-region>` using **Codespaces Secrets** or a private environment. AWS SDK credentials should use an appropriate temporary role/session when possible. Never commit keys. Avoid long-lived IAM keys.
3. Restart Streamlit. Analyze URL, check explicit AWS consent, click **Generate AI explanation**.
4. Only hostname, scheme, score and findings are sent to the model. The agent has **no tools**; model output may be wrong. Do not treat it as authoritative.

### Tests
```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py analyzer.py ai_agent.py tests
```

## Threat model and limitations
- No URL fetching, DNS requests, website execution, or port scanning in offline analyzer; avoids URL-based SSRF and active scanning.
- Input length, scheme, credentials, hostnames, ports, whitespace and control characters are validated.
- URL path/query are not included in reports or sent to AWS; the hostname is sent only with explicit consent.
- Scores are simplistic heuristics with **false positives and false negatives**. HTTPS does not guarantee trust; a score of zero does not prove safety.
- AI prompt injection remains a risk even with system prompts; only structured heuristic data is supplied, and no agent tools are enabled.
- Do not publish Codespaces port publicly; use a private repository and secrets. Streamlit is not hardened for public multi-tenant deployment or authentication.
- No security assessment can guarantee zero vulnerabilities. This package includes unit tests but no live cloud penetration test or paid Bedrock integration test.
