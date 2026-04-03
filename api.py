from __future__ import annotations

import os
from datetime import date, datetime
from typing import Iterable

import requests


BASE_URL = "https://www.alphavantage.co/query"
SUPPORTED_FUNCTIONS = {
    "1": "TIME_SERIES_INTRADAY",
    "2": "TIME_SERIES_DAILY",
    "3": "TIME_SERIES_WEEKLY",
    "4": "TIME_SERIES_MONTHLY",
}
SUPPORTED_CHARTS = {
    "1": "line",
    "2": "bar",
}


class StockAppError(Exception):
    """Raised when the stock visualization app encounters a user-facing error."""


def get_api_key() -> str:
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "").strip()
    if not api_key:
        raise StockAppError(
            "Missing Alpha Vantage API key. Set ALPHA_VANTAGE_API_KEY before running the app."
        )
    return api_key


def parse_date(date_text: str) -> date:
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError as exc:
        raise StockAppError(f"Invalid date '{date_text}'. Use YYYY-MM-DD format.") from exc


def validate_date_range(start_date: date, end_date: date) -> None:
    if end_date < start_date:
        raise StockAppError("End date cannot be before the begin date.")


def get_function_by_choice(choice: str) -> str:
    function_name = SUPPORTED_FUNCTIONS.get(choice)
    if not function_name:
        raise StockAppError("Invalid time series choice. Pick one of the listed options.")
    return function_name


def get_chart_by_choice(choice: str) -> str:
    chart_name = SUPPORTED_CHARTS.get(choice)
    if not chart_name:
        raise StockAppError("Invalid chart type choice. Pick one of the listed options.")
    return chart_name


def fetch_stock_data(symbol: str, function_name: str) -> dict:
    params = {
        "function": function_name,
        "symbol": symbol.upper(),
        "apikey": get_api_key(),
    }

    if function_name == "TIME_SERIES_INTRADAY":
        params["outputsize"] = "compact"

    if function_name == "TIME_SERIES_INTRADAY":
        params["interval"] = "60min"

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    

    if "Error Message" in payload:
        raise StockAppError("Alpha Vantage rejected the symbol or request parameters.")
    if "Note" in payload:
        raise StockAppError(payload["Note"])
    if "Information" in payload:
        raise StockAppError(payload["Information"])

    return payload


def _find_series_key(payload: dict) -> str:
    for key in payload:
        if "Time Series" in key:
            return key
    raise StockAppError("Could not find time series data in the Alpha Vantage response.")


def filter_stock_data(payload: dict, start_date: date, end_date: date) -> list[dict]:
    series_key = _find_series_key(payload)
    time_series = payload[series_key]
    filtered_rows = []

    for raw_timestamp, values in time_series.items():
        current_date = datetime.fromisoformat(raw_timestamp).date()
        if start_date <= current_date <= end_date:
            filtered_rows.append(
                {
                    "timestamp": raw_timestamp,
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": float(values["5. volume"]),
                }
            )

    filtered_rows.sort(key=lambda row: row["timestamp"])

    if not filtered_rows:
        raise StockAppError("No stock data was returned for that date range.")

    return filtered_rows


def prompt_menu(title: str, options: dict[str, str]) -> str:
    print(f"\n{title}")
    for key, label in options.items():
        print(f"{key}. {label}")
    return input("Enter your choice: ").strip()


def prompt_non_empty(prompt_text: str) -> str:
    value = input(prompt_text).strip()
    if not value:
        raise StockAppError("This value cannot be empty.")
    return value


def summarize_selection(
    symbol: str,
    chart_type: str,
    function_name: str,
    start_date: date,
    end_date: date,
) -> Iterable[str]:
    return (
        f"Symbol: {symbol.upper()}",
        f"Chart type: {chart_type}",
        f"Time series: {function_name}",
        f"Begin date: {start_date.isoformat()}",
        f"End date: {end_date.isoformat()}",
    )
