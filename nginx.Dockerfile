FROM nginx

COPY dist.tar.gz /
RUN tar xvzf /dist.tar.gz dist
