# spring-cloud-dataflow-python-task

[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/airndlab/spring-cloud-dataflow-python-task?label=Docker%20Hub)](https://hub.docker.com/r/airndlab/spring-cloud-dataflow-python-task)

Use [poetry](https://python-poetry.org/docs/1.4/) for building.

> See [debug-task](../debug-task) for example.

## entrypoint.py

Create `entrypoint.py` file with `main` method:

```python
def main():
# your code
```

## Dockerfile

```dockerfile
FROM airndlab/spring-cloud-dataflow-python-task:${VERSION} as base


FROM base as builder

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==$POETRY_VERSION

RUN poetry install --only main


FROM base AS runtime

#RUN apt-get update \
#    && apt-get install --yes --no-install-recommends \
#                YOUR-LIB \
#                YOUR-ANOTHER-LIB \
#    && rm --recursive --force /var/lib/apt/lists/*

COPY --from=builder $POETRY_VIRTUALENVS_PATH $POETRY_VIRTUALENVS_PATH

WORKDIR $TASK_ENTRYPOINT_HOME

# Use .dockerignore
COPY . .

RUN rm pyproject.toml poetry.lock

RUN useradd taskuser

RUN chown -R taskuser:taskuser $TASK_ENTRYPOINT_HOME

RUN chmod 777 $TASK_ENTRYPOINT_HOME

USER taskuser
```
