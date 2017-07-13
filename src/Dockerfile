FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN groupadd -r unprivileged --gid=999 \
    && useradd -m -r -g unprivileged --uid=999 unprivileged

ENV GOSU_VERSION 1.9
RUN set -x \
    && apt-get update && apt-get install -y --no-install-recommends ca-certificates wget && rm -rf /var/lib/apt/lists/* \
    && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
    && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
    && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
    && export GNUPGHOME="$(mktemp -d)" \
    && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
    && rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu \
    && gosu nobody true

RUN apt-get update && apt-get install -y --no-install-recommends \
        vim \
        unzip \
        openssh-server \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app \
    && chown -R unprivileged:unprivileged /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY entrypoint.sh /app/

COPY . /app/

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["runserver"]
