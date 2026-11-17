---
name: financial-ratio-extractor
description: Extract key financial statement figures for a ticker, calculate standard ratios, and run unit/period checks. Outputs source-linked JSON and CSV.
---

# Financial Statement Ratio Extractor

## Scope
For an equity research analyst or student. Takes a stock ticker, retrieves the latest annual financials via yfinance, extracts core figures, calculates ratios, and produces checked outputs.

## Inputs
- Ticker symbol (required)
- Output directory (optional, default `outputs/`)

## Procedure
1. Run the extraction script(located in this skill folder):