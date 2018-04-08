FROM debian:9.4
LABEL maintainer "Etsuji Nakai <enakai@google.com>"
ENV REFRESHED_AT 2017/02/28

RUN apt-get -qq update; \
    apt-get -qq -y upgrade; \
    apt-get -qq -y install \
        curl python python-dev python-pip \
        python-flask python-requests; \
    pip install --upgrade setuptools; \
    pip install --upgrade gcloud

ADD src /opt/gobang/bin
EXPOSE 8081
CMD ["/opt/gobang/bin/backend.py"]
