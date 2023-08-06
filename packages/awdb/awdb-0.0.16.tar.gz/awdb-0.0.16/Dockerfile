from ubuntu:bionic

copy . /awdb

RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            python3-wheel \
            python3-setuptools \
            python3-pip \
            python3-yarl \
            python3-multidict \
            python3 \
        && rm -rf /var/lib/apt/lists/* \
        && cd /awdb \
        && pip3 install -e . \
        && pip3 install -U aiohttp==3.4 multidict==4.1.0 yarl==1.1.0

CMD ["awdb-server"]
