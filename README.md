\# Financial Statement Ratio Extractor



\## Finance user, task, and supported scope

For an equity research analyst or finance student.  

Extracts key financial-statement figures for a given ticker, calculates standard ratios, and runs unit/period checks.  

Supports the latest annual period via yfinance.



\## Required software / model access and tested versions

\- Python 3.11+ (virtual environment recommended)

\- workswarm (JiuwenSwarm)

\- Packages: yfinance, pandas, numpy

\- Model: DeepSeek or any OpenAI-compatible model configured in WorkSwarm



\## Input files / fields, units, sources, and data-access instructions

\- Input: stock ticker symbol (example: AAPL or MSFT)

\- Data source: yfinance (public Yahoo Finance data)

\- Units: full currency units (always verify against official filings)

\- Retrieval timestamp is saved automatically in the output JSON



\## How to start

1\. Start WorkSwarm.

2\. Import the Skill by uploading the zip from `skills/ratio-extractor` (or the folder that contains SKILL.md + the two Python scripts).

3\. In a new task, ask the agent to use the financial-ratio-extractor skill on a ticker.

&#x20;  Example request:

&#x20;  “Use the financial-ratio-extractor skill on ticker MSFT and write outputs to outputs/msft\_fresh.”



\## One small example and its expected checks

\- Example 1: ticker AAPL → outputs/aapl\_first\_run → check\_results.json shows "passed": true

\- Example 2 (fresh case): ticker MSFT → outputs/msft\_fresh → check\_results.json shows "passed": true



\## Output files and what they mean

\- figures\_and\_ratios.json — extracted figures + calculated ratios + metadata (source, period, currency, retrieval time)

\- ratios.csv — simple table of the calculated ratios

\- check\_results.json — arithmetic and period-alignment verification results



\## How to verify / reproduce the important result

Open figures\_and\_ratios.json and manually calculate:

\- Gross margin = gross\_profit / revenue

\- Current ratio = current\_assets / current\_liabilities

Compare the results with the values in ratios.csv. They should match within normal floating-point tolerance.



\## Known failures and limitations

\- Interest expense is sometimes missing (NaN) in yfinance, so interest coverage cannot be calculated.

\- yfinance data completeness and scaling can vary; always cross-check critical figures with official 10-K filings.

\- Only the latest annual period is supported in this version.

\- Some Python environments lack datetime.UTC; a one-line runtime compatibility shim was used during testing while leaving the original scripts unchanged.



\## Reused work, AI assistance, license, and attribution

\- Skill structure, scripts, and documentation created with AI assistance (Grok) and executed/verified inside WorkSwarm.

\- Financial data obtained via yfinance.

\- License: MIT



\## openJiuwen / JiuwenSwarm link

https://github.com/openJiuwen-ai/jiuwenswarm



\## Public project version

\[Paste the exact GitHub commit URL here after you push]

