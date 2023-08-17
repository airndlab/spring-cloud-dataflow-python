import logging
from datetime import datetime

import psycopg2
from py_spring_dataflow.spring import datasource_props
from py_spring_dataflow.spring.cloud.task import task_props

logger = logging.getLogger('TaskStatus')


class TaskStatus:
    """
    For working with table task_execution
    """

    def __init__(self, task_id, parent_id, db_host, db_port, db_name, db_username, db_password):
        logger.info(f'Create status for task_execution_id={task_id} (parent_execution_id={parent_id})')
        self.task_id = task_id
        self.parent_id = parent_id
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password

    def start(self):
        """Set the task_execution's start_time """
        logger.info('Set status as started')
        with psycopg2.connect(
                host=self.db_host, port=self.db_port, dbname=self.db_name,
                user=self.db_username, password=self.db_password) as connection:
            with connection.cursor() as cursor:
                now = datetime.now()
                sql = 'UPDATE task_execution ' \
                      'SET start_time=%s, ' \
                      '    last_updated=%s, ' \
                      '    parent_execution_id=%s, ' \
                      '    exit_code=null, ' \
                      '    exit_message=null, ' \
                      '    error_message=null ' \
                      'WHERE task_execution_id=%s'
                cursor.execute(sql, (now, now, self.parent_id, self.task_id))

    def complete(self):
        """Set the task_execution's end_time, exist_code=0 and exist_message/error_message must be null """
        logger.info('Set status as completed')
        with psycopg2.connect(
                host=self.db_host, port=self.db_port, dbname=self.db_name,
                user=self.db_username, password=self.db_password) as connection:
            with connection.cursor() as cursor:
                now = datetime.now()
                sql = 'UPDATE task_execution ' \
                      'SET end_time=%s, ' \
                      '    last_updated=%s, ' \
                      '    exit_code=0, ' \
                      '    exit_message=null, ' \
                      '    error_message=null ' \
                      'WHERE task_execution_id=%s'
                cursor.execute(sql, (now, now, self.task_id))

    def fail(self, short_message, stack_message=''):
        """Set the task_execution's end_time,
        exist_code is the error code and exist_message/error_message describe the error """
        logger.info('Set status as failed')
        with psycopg2.connect(
                host=self.db_host, port=self.db_port, dbname=self.db_name,
                user=self.db_username, password=self.db_password) as connection:
            with connection.cursor() as cursor:
                now = datetime.now()
                max_message_length = 2499
                exit_message = short_message[:max_message_length]
                error_message = stack_message[:max_message_length]
                sql = 'UPDATE task_execution ' \
                      'SET end_time=%s, ' \
                      '    last_updated=%s, ' \
                      '    exit_code=1, ' \
                      '    exit_message=%s, ' \
                      '    error_message=%s ' \
                      'WHERE task_execution_id=%s'
                cursor.execute(sql, (now, now, exit_message, error_message, self.task_id))


def new():
    task_id = task_props.get_execution_id()
    parent_id = task_props.get_parent_execution_id()
    # jdbc:postgresql://host:port/name?params
    db_url = datasource_props.get_url()
    # host:port/name
    host_port_name = db_url.partition('jdbc:postgresql://')[2].partition('?')[0]
    db_host = host_port_name.partition(':')[0]
    db_port = host_port_name.partition(':')[2].partition('/')[0]
    db_name = host_port_name.partition('/')[2]
    db_username = datasource_props.get_username()
    db_password = datasource_props.get_password()
    return TaskStatus(task_id, parent_id, db_host, db_port, db_name, db_username, db_password)
