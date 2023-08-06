#!/usr/bin/env python3

from radical.entk import Pipeline, Stage, Task, AppManager
import os

host = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))


def generate_pipeline():

    p = Pipeline()
    s = Stage()
    t = Task()
    t.executable = '/bin/date'
    t.cpu_reqs   = {'processes'           : 6,
                    'process_type'        : 'MPI',
                    'threads_per_process' : 1,
                    'thread_type'         : 'OpenMP'}
    t.gpu_reqs   = {'processes'           : 1,
                    'process_type'        : 'MPI',
                    'threads_per_process' : 1,
                    'thread_type'         : 'CUDA'}
    s.add_tasks(t)
    p.add_stages(s)

    return p


if __name__ == '__main__':

    appman   = AppManager(hostname=host, port=port)
    res_dict = {
        'resource': 'local.traverse',
        'walltime': 10,
        'cpus'    : 64,
        'gpus'    :  8
    }

    appman.resource_desc = res_dict
    appman.workflow = set([generate_pipeline()])
    appman.run()
