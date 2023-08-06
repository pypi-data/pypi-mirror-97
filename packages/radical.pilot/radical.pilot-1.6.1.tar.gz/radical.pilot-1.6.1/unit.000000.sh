#!/bin/sh


# Environment variables
export RADICAL_BASE="<Mock id='140635783301968'>"
export RP_SESSION_ID="sid0"
export RP_PILOT_ID="pid0"
export RP_AGENT_ID="aid0"
export RP_SPAWNER_ID="<Mock id='140635783301872'>"
export RP_UNIT_ID="unit.000000"
export RP_UNIT_NAME="cu.0000"
export RP_GTOD="<Mock id='140635783301920'>"
export RP_TMP="<Mock id='140635783302064'>"
export RP_PILOT_SANDBOX="<Mock id='140635783301968'>"
export RP_PILOT_STAGING="<Mock id='140635783301968'>"
export RP_PROF=".//unit.000000.prof"

prof(){
    if test -z "$RP_PROF"
    then
        return
    fi
    event=$1
    msg=$2
    now=$($RP_GTOD)
    echo "$now,$event,unit_script,MainThread,$RP_UNIT_ID,AGENT_EXECUTING,$msg" >> $RP_PROF
}
export OMP_NUM_THREADS="0"

prof cu_start

# Change to unit sandbox
cd ./

# Pre-exec commands
prof cu_pre_start
test_pre_exec ||  (echo "pre_exec failed"; false) || exit
prof cu_pre_stop

# The command to run
prof cu_exec_start
mpiexec echo hello
RETVAL=$?
prof cu_exec_stop

# Post-exec commands
prof cu_post_start
test_post_exec ||  (echo "post_exec failed"; false) || exit

prof cu_post_stop "$ret=RETVAL"

# Exit the script with the return code from the command
prof cu_stop
exit $RETVAL
