FROM python:3.12-alpine
WORKDIR /app
COPY cli.py .
RUN chmod +x /app/cli.py
ENTRYPOINT ["python3", "/app/cli.py"]
