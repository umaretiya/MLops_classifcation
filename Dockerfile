FROM python=3.10-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt 

EXPOSE $PORT

ENTRYPOINT [ "flask" ]

CMD [ "run" ]
