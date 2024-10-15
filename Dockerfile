FROM python:3.10.13-slim-bookworm as base-python

FROM base-python as dependency-image

ARG INCLUDE_TEST_REQUIREMENTS=0

COPY ./requirements.txt /tmp/requirements.txt
COPY ./test_requirements.txt /tmp/test_requirements.txt

RUN apt-get update && \
    apt-get --yes install git build-essential libmemcached-dev zlib1g-dev libpq-dev && \
    pip install --upgrade pip && \
    if [ "${INCLUDE_TEST_REQUIREMENTS}" = "1" ]; then \
        pip install --requirement /tmp/test_requirements.txt --prefix=/install; \
    else \
        pip install --requirement /tmp/requirements.txt --prefix=/install; \
    fi

FROM base-python as intermediate

RUN useradd --create-home appuser && \
    apt-get update && \
    apt-get --yes upgrade && \
    apt-get --yes install --no-install-recommends tini git libmemcached-dev zlib1g libpq5 netcat-traditional vim

COPY --from=dependency-image /install /usr/local
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
COPY ./src /src-dist/src

ENTRYPOINT ["/usr/bin/tini", "--", "/docker-entrypoint.sh"]
CMD []


FROM intermediate as testable
COPY ./tests /src-dist/tests

FROM intermediate as release
USER appuser
