FROM python:3.10-slim AS base
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
    
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

FROM base AS final
CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]