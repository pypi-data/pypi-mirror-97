#!/usr/bin/env python

import os
from   random import randint, choice

import radical.pilot as rp

# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'local.localhost',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 64,
                   'gpus'          : 8
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        umgr  = rp.UnitManager(session=session)

        pilot = pmgr.submit_pilots([pdesc])
        umgr.add_pilots(pilot)

        cuds = list()
        for i in range(20):

            cud = rp.ComputeUnitDescription()
            cud.uid = 'unit.%04d' % i
            if i == 0:
                cud.executable    = '/bin/ls'
                cud.arguments     = ['/tmp > out.dat']
            else:
                cud.executable    = '/bin/cp'
                cud.arguments     = ['-v', 'in.dat', 'out.dat']
                cud.input_staging = [{'source': 'unit.%04d:///out.dat' % (i-1),
                                      'target': 'in.dat',
                                      'action': rp.COPY}]
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()

    finally:
        session.close(download=False)


# ------------------------------------------------------------------------------

