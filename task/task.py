import logging
import os
import traceback

import py_spring_dataflow.args
import py_spring_dataflow.params

from spring import spring_cloud_task_status
from task import entrypoint

logger = logging.getLogger('task')

if py_spring_dataflow.params.get_flag('debug', False):
    logger.info(f'Arguments: {py_spring_dataflow.args.get_args()}')

task_status = spring_cloud_task_status.new()
try:
    logger.info(f'Starting in "{os.getcwd()}"')
    task_status.start()
    logger.info('Execute entrypoint.main()')
    entrypoint.main()
    task_status.complete()
    logger.info('Completed')

except Exception as exc:
    exit_message = f'Failed: {exc}'
    error_message = ''.join(traceback.format_exception(exc))
    logger.info(error_message)
    task_status.fail(1, exit_message, error_message)

finally:
    logger.info('Finished')
