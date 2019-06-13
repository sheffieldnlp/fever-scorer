FROM continuumio/miniconda3

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

RUN apt-get update
RUN apt-get install -y --no-install-recommends --allow-unauthenticated \
    zip \
    gzip \
    make \
    automake \
    gcc \
    build-essential \
    g++ \
    cpp \
    libc6-dev \
    man-db \
    autoconf \
    pkg-config \
    unzip \
    libffi-dev \
    software-properties-common

RUN mkdir /fever
WORKDIR /fever

ADD requirements.txt /fever/
RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt')"

RUN mkdir -pv src
RUN mkdir -pv configs

ADD src src
ADD configs configs

ADD predict.sh .

ENV PYTHONPATH src
ENV FLASK_APP sample_application:my_sample_fever

#ENTRYPOINT ["/bin/bash","-c"]
CMD ["flask", "run", "--host=0.0.0.0"]