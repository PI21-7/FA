FROM python:3.8

RUN mkdir -p /src/app/
WORKDIR /src/app/

COPY . /src/app/

RUN pip install --user --no-cache-dir -r requirements.txt

CMD ["python", "bot.py", "-i", "-s"]
