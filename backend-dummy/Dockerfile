FROM debian:8.4
MAINTAINER Etsuji Nakai <enakai@google.com>
ENV REFRESHED_AT 2016/08/11

RUN apt-get -qq update
RUN apt-get -qq -y upgrade
RUN apt-get -qq -y install \
        curl python python-dev python-pip \
        python-flask python-requests
RUN pip install --upgrade gcloud

ADD src /opt/gobang/bin
EXPOSE 8081
CMD ["/opt/gobang/bin/backend.py"]
