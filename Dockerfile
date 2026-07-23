FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

COPY requirements-dashboard.txt .
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements-dashboard.txt

COPY dashboard_panel_bokeh ./dashboard_panel_bokeh
COPY data/survey_data_cleaned_reduced.csv ./data/survey_data_cleaned_reduced.csv

EXPOSE 7860

CMD ["sh", "-c", "panel serve dashboard_panel_bokeh/app.py --address 0.0.0.0 --port ${PORT:-7860} --allow-websocket-origin='*' --use-xheaders --global-loading-spinner"]
