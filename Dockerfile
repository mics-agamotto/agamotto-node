FROM python:3.9-bullseye

COPY . /agamotto-node
WORKDIR /agamotto-node
RUN pip install .
RUN tar xvzf dist.tar.gz dist

ENTRYPOINT [ "agamotto-node-prod" ]
