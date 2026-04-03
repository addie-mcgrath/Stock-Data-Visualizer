from __future__ import annotations

from pathlib import Path

import plotly.express as px


def build_chart(rows: list[dict], symbol: str, chart_type: str, output_dir: Path) -> Path:
    timestamps = [row["timestamp"] for row in rows]
    close_prices = [row["close"] for row in rows]

    if chart_type == "bar":
        figure = px.bar(
            x=timestamps,
            y=close_prices,
            labels={"x": "Date", "y": "Closing Price (USD)"},
            title=f"{symbol.upper()} Closing Prices",
        )
    else:
        figure = px.line(
            x=timestamps,
            y=close_prices,
            labels={"x": "Date", "y": "Closing Price (USD)"},
            title=f"{symbol.upper()} Closing Prices",
        )

    figure.update_layout(xaxis_title="Date", yaxis_title="Closing Price (USD)")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{symbol.lower()}_{chart_type}_chart.html"
    figure.write_html(str(output_path), auto_open=True)
    return output_path
