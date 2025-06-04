FROM python:3.13-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install pipenv

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]