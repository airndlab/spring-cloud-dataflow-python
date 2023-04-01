import os

import py_spring_dataflow.args
import py_spring_dataflow.params

from spring import spring_cloud_task_status

if py_spring_dataflow.params.get_flag('debug', False):
    print(f'Arguments: {py_spring_dataflow.args.get_args()}')

task_status = spring_cloud_task_status.new()
try:
    print(f'Starting in "{os.getcwd()}"')
    task_status.start()
    print('Execute entrypoint.py')
    entrypoint_file = open('entrypoint.py')
    entrypoint_code = entrypoint_file.read()
    exec(entrypoint_code)
    task_status.completed()
    print('Competed')

except Exception as exc:
    error_message = f'Failed: {exc}'
    print(error_message)
    task_status.failed(1, error_message, error_message)

finally:
    task_status.finish()
    print('Finished')
