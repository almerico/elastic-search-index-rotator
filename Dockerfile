FROM python:3

WORKDIR /usr/src/app
COPY . .
RUN apt-get update \
    && apt-get install -y --no-install-recommends  python-setuptools python-pip \
    python-wheel libpython-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir requests-aws4auth elasticsearch
RUN pip3 install --no-binary=:all:  elasticsearch-curator
CMD ["main.py"]
ENTRYPOINT ["python3"]
