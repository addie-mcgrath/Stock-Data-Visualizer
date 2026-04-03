# Stock Data Visualization

This project is a Python application that queries the Alpha Vantage API, filters historical stock data by a user-selected date range, and opens a chart in the user's default browser.

## Features

- Prompts for a stock symbol
- Prompts for chart type
- Prompts for Alpha Vantage time series function
- Prompts for begin and end dates in `YYYY-MM-DD` format
- Validates that the end date is not before the begin date
- Generates an HTML chart and opens it in the default browser

## Project Structure

- `run_app.py`: simple entry point
- `stock_data_visualization/api.py`: Alpha Vantage requests, validation, and filtering
- `stock_data_visualization/charting.py`: chart generation with Plotly
- `stock_data_visualization/main.py`: command-line workflow
- `docs/use_cases.md`: use case descriptions for the report

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Alpha Vantage API key:

```bash
export ALPHA_VANTAGE_API_KEY=your_api_key_here
```

4. Run the app:

```bash
python run_app.py
```

## Time Series Options

1. `TIME_SERIES_INTRADAY`
2. `TIME_SERIES_DAILY`
3. `TIME_SERIES_WEEKLY`
4. `TIME_SERIES_MONTHLY`

## Chart Options

1. `line`
2. `bar`

## Suggested Git Workflow

- Create a shared GitHub repository for the project
- Use a `main` branch for stable work
- Have each teammate work from their own feature branch
- Open pull requests before merging
- Make frequent, descriptive commits so the history shows steady collaboration

## Suggested Team Deliverables

- Use case diagram
- Use case descriptions
- Jira scrum board screenshots
- Burndown chart screenshots
- Team communication plan
- Lessons learned narrative

## Notes

- Alpha Vantage free-tier usage can be rate-limited, so repeated test runs may require a short wait.
- Generated charts are saved into the `charts/` directory.
