#!/usr/bin/env python

import os
import random

rand = random.choice

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    with rp.Session() as session:

        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'local.scale',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 1024 * 8
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)
        umgr  = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)

        n    = 1024 * 2
        cuds = list()
        for i in range(0, n):

            cud = rp.ComputeUnitDescription()
            cud.executable       = '%s/examples/hello_rp.sh' % os.getcwd()
            cud.arguments        = [rand([1, 2, 4, 8, 16, 32]) * 4]
            cud.gpu_processes    =  rand([0, 0, 0, 0, 0, 1, 1, 2])
            cud.cpu_processes    =  rand([1, 2, 4, 8, 16, 32] * 1)
            cud.cpu_threads      =  rand([1, 2, 4])
            cud.gpu_process_type = rp.MPI
            cud.cpu_process_type = rp.MPI
            cud.cpu_thread_type  = rp.OpenMP
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()


# ------------------------------------------------------------------------------

