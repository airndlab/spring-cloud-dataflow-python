FROM python:3.11.0-slim-buster as base

ENV TASK_HOME=/usr/src
ENV TASK_ENTRYPOINT_HOME=$TASK_HOME/task

ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

ENV POETRY_VERSION=1.4.2
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_PATH=$TASK_HOME/.venv

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

RUN pip install poetry==$POETRY_VERSION

RUN poetry install --only main


FROM base AS runtime

COPY --from=builder $POETRY_VIRTUALENVS_PATH $POETRY_VIRTUALENVS_PATH

COPY . .

RUN rm pyproject.toml poetry.lock

# $POETRY_VIRTUALENVS_PATH/bin/python $TASK_HOME/task.py
ENTRYPOINT ["/usr/src/.venv/bin/python", "/usr/src/task.py"]

CMD []
