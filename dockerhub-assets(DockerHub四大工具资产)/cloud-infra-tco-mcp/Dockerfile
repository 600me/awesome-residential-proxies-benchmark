FROM python:3.12-alpine
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .
ENTRYPOINT ["python3", "-m", "cloud_infra_tco_mcp"]
