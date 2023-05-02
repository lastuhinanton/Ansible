FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y && apt-get install ssh -y

COPY ./script.sh .

ENTRYPOINT ["bash", "script.sh"]
