FROM python:3.9-bullseye

COPY . /agamotto-node
WORKDIR /agamotto-node
RUN pip install .

ENTRYPOINT [ "agamotto-node" ]
