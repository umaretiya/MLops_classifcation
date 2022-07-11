FROM python:3.10-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt 

EXPOSE $PORT

# ENTRYPOINT [ "python" ]

# CMD [ "main.py" ]
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT main:app

