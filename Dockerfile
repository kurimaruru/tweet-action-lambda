FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip

COPY requirements.txt .

RUN mkdir /function && \
    pip install -r requirements.txt --target /function

COPY app.py /function/
COPY dynamodb /function/
COPY websocket /function/
COPY .env /function/

WORKDIR /function

COPY ./entry_script.sh /entry_script.sh

ADD ./aws-lambda-rie/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie && chmod 755 /entry_script.sh
ENTRYPOINT [ "/entry_script.sh" ]

CMD [ "app.handler" ]
