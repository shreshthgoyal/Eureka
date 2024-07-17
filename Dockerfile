FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3015

ENV MODULE_NAME="src.main"
ENV VARIABLE_NAME="app"
ENV PORT="8000"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3015"]
