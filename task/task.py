import logging
import traceback

import py_spring_dataflow.args
import py_spring_dataflow.params

from spring import spring_cloud_task_status
from task import entrypoint

is_debug = py_spring_dataflow.params.get_flag('debug', False)
logging.basicConfig(
    level=(logging.DEBUG if is_debug else logging.INFO),
    datefmt='%Y-%m-%dT%H:%M:%S',
    format="%(asctime)s %(levelname)s %(name)s : %(message)s"
)
logger = logging.getLogger('task')

logger.debug(f'Arguments: {py_spring_dataflow.args.get_args()}')

task_status = spring_cloud_task_status.new()
try:
    logger.info(f'Starting execution"')
    task_status.start()
    logger.info('Execute entrypoint.main()')
    entrypoint.main()
    task_status.complete()
    logger.info('Completed execution')

except Exception as exc:
    exit_message = f'Failed: {exc}'
    error_message = ''.join(traceback.format_exception(exc))
    logger.exception('Failed execution')
    task_status.fail(1, exit_message, error_message)
