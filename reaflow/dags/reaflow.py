#! /usr/bin/env python3

import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from reaflow.utils.config import base_func, FlowParams
from reaflow.data import DEFAULT_CFG


PARAM_OBJ = FlowParams.fromfile(DEFAULT_CFG)


def load_rea_config(ds, **kwargs):
    '''Load project config file'''
    cfg_file = kwargs['dag_run'].conf.get('cfg')
    if cfg_file is not None:
        PARAM_OBJ = FlowParams.fromfile(cfg_file)
        return PARAM_OBJ


def dag_end(ds, **kwargs):
    with open('/home/lxgui/airflow.log', 'a') as af_test:
        af_test.write('DAG ends.')
    return 'DAG ends.'


def expression_filter_test(ds, **kwargs):
    print(ds)
    print(kwargs)


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='rnaseq_exp_analysis_workflow',
    default_args=args,
    schedule_interval=None
)

load_config = PythonOperator(
    task_id='load_rea_config',
    provide_context=True,
    python_callable=load_rea_config,
    dag=dag,
)

expression_filter = PythonOperator(
    task_id='exp_filter',
    provide_context=True,
    python_callable=base_func['expression_filter'],
    dag=dag,
    params=PARAM_OBJ.params(base_func['expression_filter']),
)

expression_filter_test = PythonOperator(
    task_id='exp_filter',
    provide_context=True,
    python_callable=expression_filter_test,
    dag=dag,
    params=PARAM_OBJ.params(base_func['expression_filter']),
)


# end_task = PythonOperator(
#     task_id='dag_end',
#     provide_context=True,
#     python_callable=dag_end,
#     dag=dag
# )

# end_task.set_upstream(load_config)
expression_filter_test.set_upstream(load_config)
