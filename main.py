from __future__ import annotations

from pathlib import Path

from stock_data_visualization.api import (
    StockAppError,
    SUPPORTED_CHARTS,
    SUPPORTED_FUNCTIONS,
    fetch_stock_data,
    filter_stock_data,
    get_chart_by_choice,
    get_function_by_choice,
    parse_date,
    prompt_menu,
    prompt_non_empty,
    summarize_selection,
    validate_date_range,
)
from stock_data_visualization.charting import build_chart


def main() -> None:
    try:
        print("Stock Data Visualization")
        symbol = prompt_non_empty("Enter the stock symbol: ")
        chart_choice = prompt_menu("Select a chart type:", SUPPORTED_CHARTS)
        function_choice = prompt_menu("Select a time series function:", SUPPORTED_FUNCTIONS)
        start_date = parse_date(prompt_non_empty("Enter the beginning date (YYYY-MM-DD): "))
        end_date = parse_date(prompt_non_empty("Enter the end date (YYYY-MM-DD): "))
        validate_date_range(start_date, end_date)

        chart_type = get_chart_by_choice(chart_choice)
        function_name = get_function_by_choice(function_choice)

        print("\nPreparing request with:")
        for line in summarize_selection(symbol, chart_type, function_name, start_date, end_date):
            print(f"- {line}")

        payload = fetch_stock_data(symbol, function_name)
        rows = filter_stock_data(payload, start_date, end_date)
        output_path = build_chart(rows, symbol, chart_type, Path("charts"))

        print(f"\nChart created successfully: {output_path.resolve()}")
    except StockAppError as exc:
        print(f"\nError: {exc}")
    except KeyboardInterrupt:
        print("\nCancelled by user.")


if __name__ == "__main__":
    main()
