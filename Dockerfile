FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p uploads results

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

ENV MONGO_URL=mongodb://host.docker.internal:27017/

CMD ["python", "app.py"]