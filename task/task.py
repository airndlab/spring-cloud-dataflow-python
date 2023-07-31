import os
import traceback

import py_spring_dataflow.args
import py_spring_dataflow.params

from spring import spring_cloud_task_status
from task import entrypoint

if py_spring_dataflow.params.get_flag('debug', False):
    print(f'Arguments: {py_spring_dataflow.args.get_args()}')

task_status = spring_cloud_task_status.new()
try:
    print(f'Starting in "{os.getcwd()}"')
    task_status.start()
    print('Execute entrypoint.main()')
    entrypoint.main()
    task_status.complete()
    print('Completed')

except Exception as exc:
    exit_message = f'Failed: {exc}'
    error_message = ''.join(traceback.format_exception(exc))
    print(error_message)
    task_status.fail(1, exit_message, error_message)

finally:
    print('Finished')
