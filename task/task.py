import py_spring_dataflow.args
import py_spring_dataflow.params
from py_spring_dataflow.spring import datasource_props
from py_spring_dataflow.spring.cloud.task import task_props

from spring.spring_cloud_task_status import TaskStatus

debug = py_spring_dataflow.params.get_flag('debug', False)

if debug:
    print(f'Arguments: {py_spring_dataflow.args.get_args()}')

task_id = task_props.get_execution_id()
print(f'Task id={task_id}')
task_name = task_props.get_name()
print(f'Task name={task_name}')

db_url = datasource_props.get_url()
db_username = datasource_props.get_username()
db_password = datasource_props.get_password()

task_status = TaskStatus(task_id, db_url, db_username, db_password)

try:
    print('Starting')
    task_status.start()

    print('Execute main.py')
    main_file = open('main.py')
    main_code = main_file.read()
    exec(main_code)

    task_status.completed()
    print('Competed')

except Exception as exc:
    error_message = f'Failed: {exc}'
    print(error_message)
    task_status.failed(1, error_message, error_message)

finally:
    task_status.finish()
    print('Finished')
