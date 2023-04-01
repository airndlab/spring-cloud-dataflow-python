FROM python:3.11.0-slim-buster as base

ENV TASK_HOME=/usr/src

ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

WORKDIR $TASK_HOME

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
                default-libmysqlclient-dev \
    && rm --recursive --force /var/lib/apt/lists/*


FROM base as builder

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
                build-essential

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry install --no-dev


FROM base AS runtime

COPY --from=builder $TASK_HOME/.venv .venv

COPY . .

RUN rm pyproject.toml poetry.lock

ENTRYPOINT [".venv/bin/python", "task.py"]

CMD []
