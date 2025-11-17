FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/
COPY data/ /app/data/

EXPOSE 8050

CMD ["python", "app.py"]
