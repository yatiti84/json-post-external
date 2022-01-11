FROM logiqx/python-lxml:3.9-slim

COPY . /json-post-external
WORKDIR /json-post-external

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD python

#docker build . -t gcr.io/mirror-tv-275709/mirror-tv-cron/lite_5 && docker push gcr.io/mirror-tv-275709/mirror-tv-cron/lite_5