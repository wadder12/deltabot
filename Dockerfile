FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "bot.py"]

## - docker build -t deltabot .
## - docker run deltabot


##FIXME - SHIT DONT WORK LOL