#!/bin/sh


# Environment variables
export RADICAL_BASE="<Mock id='139819777008256'>"
export RP_SESSION_ID="sid0"
export RP_PILOT_ID="pid0"
export RP_AGENT_ID="aid0"
export RP_SPAWNER_ID="<Mock id='139819777008160'>"
export RP_TASK_ID="task.000000"
export RP_TASK_NAME="task.0000"
export RP_GTOD="<Mock id='139819777008208'>"
export RP_TMP="<Mock id='139819777008352'>"
export RP_PILOT_SANDBOX="<Mock id='139819777008256'>"
export RP_PILOT_STAGING="<Mock id='139819777008256'>"
export RP_PROF=".//task.000000.prof"

prof(){
    if test -z "$RP_PROF"
    then
        return
    fi
    event=$1
    msg=$2
    now=$($RP_GTOD)
    echo "$now,$event,task_script,MainThread,$RP_TASK_ID,AGENT_EXECUTING,$msg" >> $RP_PROF
}
export OMP_NUM_THREADS="0"

prof task_start

# Change to task sandbox
cd ./

# Pre-exec commands
prof task_pre_start
test_pre_exec ||  (echo "pre_exec failed"; false) || exit
prof task_pre_stop

# The command to run
prof task_exec_start
mpiexec echo hello
RETVAL=$?
prof task_exec_stop

# Post-exec commands
prof task_post_start
test_post_exec ||  (echo "post_exec failed"; false) || exit

prof task_post_stop "$ret=RETVAL"

# Exit the script with the return code from the command
prof task_stop
exit $RETVAL
