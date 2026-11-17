#!/usr/bin/env python3
"""
Financial Statement Ratio Extractor
Extracts key figures from yfinance and calculates standard ratios.
Configurable via command-line arguments.
"""

import argparse
import json
import os
from datetime import datetime, timezone
import yfinance as yf
import pandas as pd

def get_latest_annual(df):
    """Return the most recent annual column as a Series."""
    if df is None or df.empty:
        return None
    # yfinance annual statements are usually sorted with newest first
    return df.iloc[:, 0]

def extract_figures(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info or {}

    income = get_latest_annual(ticker.financials)
    balance = get_latest_annual(ticker.balance_sheet)
    cashflow = get_latest_annual(ticker.cashflow)

    figures = {
        "ticker": ticker_symbol,
        "company_name": info.get("longName", ticker_symbol),
        "currency": info.get("currency", "USD"),
        "retrieval_time": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "yfinance",
        "period_type": "annual",
    }

    # Income statement items
    if income is not None:
        figures["revenue"] = income.get("Total Revenue")
        figures["gross_profit"] = income.get("Gross Profit")
        figures["operating_income"] = income.get("Operating Income")
        figures["net_income"] = income.get("Net Income")
        figures["interest_expense"] = income.get("Interest Expense")
        figures["income_period"] = str(income.name) if hasattr(income, "name") else None

    # Balance sheet items
    if balance is not None:
        figures["total_assets"] = balance.get("Total Assets")
        figures["total_equity"] = balance.get("Stockholders Equity") or balance.get("Total Stockholder Equity")
        figures["current_assets"] = balance.get("Current Assets")
        figures["current_liabilities"] = balance.get("Current Liabilities")
        figures["total_debt"] = balance.get("Total Debt")
        figures["cash"] = balance.get("Cash And Cash Equivalents")
        figures["balance_period"] = str(balance.name) if hasattr(balance, "name") else None

    # Simple unit note (yfinance returns raw numbers, usually in full units)
    figures["units"] = "full currency units (not thousands or millions)"
    figures["unit_warning"] = "Verify against company filings; yfinance may scale differently by company."

    return figures

def calculate_ratios(figures):
    ratios = {}
    rev = figures.get("revenue")
    gp = figures.get("gross_profit")
    oi = figures.get("operating_income")
    ni = figures.get("net_income")
    assets = figures.get("total_assets")
    equity = figures.get("total_equity")
    ca = figures.get("current_assets")
    cl = figures.get("current_liabilities")
    debt = figures.get("total_debt")
    interest = figures.get("interest_expense")

    if rev and rev != 0:
        if gp is not None:
            ratios["gross_margin"] = gp / rev
        if oi is not None:
            ratios["operating_margin"] = oi / rev
        if ni is not None:
            ratios["net_margin"] = ni / rev

    if equity and equity != 0 and ni is not None:
        ratios["roe"] = ni / equity
    if assets and assets != 0 and ni is not None:
        ratios["roa"] = ni / assets
    if cl and cl != 0 and ca is not None:
        ratios["current_ratio"] = ca / cl
    if equity and equity != 0 and debt is not None:
        ratios["debt_to_equity"] = debt / equity
    if interest and interest != 0 and oi is not None:
        ratios["interest_coverage"] = oi / abs(interest)

    return ratios

def main():
    parser = argparse.ArgumentParser(description="Extract financial figures and calculate ratios")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol")
    parser.add_argument("--output-dir", default="outputs", help="Directory to save results")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Extracting data for {args.ticker}...")
    figures = extract_figures(args.ticker)
    ratios = calculate_ratios(figures)

    # Combine
    result = {
        "figures": figures,
        "ratios": ratios,
        "notes": [
            "All figures from latest annual period available via yfinance.",
            "Missing values are omitted or null.",
            "Always cross-check critical figures with official filings."
        ]
    }

    # Save files
    figures_path = os.path.join(args.output_dir, "figures_and_ratios.json")
    with open(figures_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    # Also save a simple CSV of ratios
    if ratios:
        pd.DataFrame([ratios]).to_csv(
            os.path.join(args.output_dir, "ratios.csv"), index=False
        )

    print(f"Results saved to {args.output_dir}")
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()