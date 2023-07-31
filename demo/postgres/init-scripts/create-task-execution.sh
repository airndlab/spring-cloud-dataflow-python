#!/bin/bash

set -e
set -u

echo "Start executing create-table.sh"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	    CREATE TABLE public.task_execution
      (
          task_execution_id     BIGINT NOT NULL PRIMARY KEY,
          start_time            TIMESTAMP,
          end_time              TIMESTAMP,
          task_name             VARCHAR(100),
          exit_code             INTEGER,
          exit_message          VARCHAR(2500),
          error_message         VARCHAR(2500),
          last_updated          TIMESTAMP,
          external_execution_id VARCHAR(255),
          parent_execution_id   BIGINT
      );

      ALTER TABLE public.task_execution
          OWNER TO $POSTGRES_USER;

      INSERT INTO public.task_execution(task_execution_id)
      VALUES (100500);
EOSQL

echo "Finished executing create-table.sh"
