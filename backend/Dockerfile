FROM python:3.13
WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
EXPOSE 8000

RUN useradd app
USER app

WORKDIR ./app/

CMD ["sh", "-c", "python3 creaTable.py && uvicorn main:app --host 0.0.0.0"]
