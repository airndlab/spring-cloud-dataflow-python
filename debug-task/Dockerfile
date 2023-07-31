FROM airndlab/spring-cloud-dataflow-python-task:1.1 as base


FROM base as builder

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==$POETRY_VERSION

RUN poetry install --only main


FROM base AS runtime

COPY --from=builder $POETRY_VIRTUALENVS_PATH $POETRY_VIRTUALENVS_PATH

WORKDIR $TASK_ENTRYPOINT_HOME

COPY . .

RUN rm pyproject.toml poetry.lock

RUN useradd taskuser

RUN chown -R taskuser:taskuser $TASK_ENTRYPOINT_HOME

RUN chmod 777 $TASK_ENTRYPOINT_HOME

USER taskuser
