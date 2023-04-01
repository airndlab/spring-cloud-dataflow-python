from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.sql import text


class TaskStatus:
    """
    For working with table TASK_EXECUTION
    """

    def __init__(self, task_id, url, username, password):
        self.task_id = task_id
        self.engine = create_engine(
            url
            .partition('?')[0]
            .replace('jdbc:mariadb://', f'mariadb://{username}:{password}@'))

    def start(self):
        """Set the TASK_EXECUTION's START_TIME """
        now = datetime.now()
        statement = text(
            "UPDATE TASK_EXECUTION "
            "SET START_TIME=:start_time, "
            "    LAST_UPDATED=:last_updated, "
            "    EXIT_CODE=null, "
            "    EXIT_MESSAGE=null, "
            "    ERROR_MESSAGE=null "
            "WHERE TASK_EXECUTION_ID=:task_id")
        params = {
            'start_time': now,
            'last_updated': now,
            'task_id': self.task_id}
        connection = self.engine.connect()
        connection.execute(statement, params)
        connection.commit()
        connection.close()

    def completed(self):
        """Set the TASK_EXECUTION's END_TIME, EXIST_CODE=0 and EXIST_MESSAGE/ERROR_MESSAGE must be null """
        now = datetime.now()
        statement = text(
            "UPDATE TASK_EXECUTION "
            "SET END_TIME=:end_time, "
            "    LAST_UPDATED=:last_updated, "
            "    EXIT_CODE=0, "
            "    EXIT_MESSAGE=null, "
            "    ERROR_MESSAGE=null "
            "WHERE TASK_EXECUTION_ID=:task_id")
        params = {
            'end_time': now,
            'last_updated': now,
            'task_id': self.task_id}
        connection = self.engine.connect()
        connection.execute(statement, params)
        connection.commit()
        connection.close()

    def failed(self, exit_code, exit_message, error_message=''):
        """Set the TASK_EXECUTION's END_TIME, EXIST_CODE is the error code and EXIST_MESSAGE/ERROR_MESSAGE describe
        the error """
        now = datetime.now()
        statement = text(
            "UPDATE TASK_EXECUTION "
            "SET END_TIME=:end_time, "
            "    LAST_UPDATED=:last_updated, "
            "    EXIT_CODE=:exit_code, "
            "    EXIT_MESSAGE=:exit_message, "
            "    ERROR_MESSAGE=:error_message "
            "WHERE TASK_EXECUTION_ID=:task_id")
        params = {
            'end_time': now,
            'last_updated': now,
            'exit_code': exit_code,
            'exit_message': exit_message,
            'error_message': error_message,
            'task_id': self.task_id}
        connection = self.engine.connect()
        connection.execute(statement, params)
        connection.commit()
        connection.close()

    def finish(self):
        self.engine.dispose()
