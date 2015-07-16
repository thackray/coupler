#!/bin/csh -f
## PBS directives 
## nb, PBS directives begin '#PBS'

#PBS -N pops_test
#PBS -l nodes=1:ppn=8
#PBS -j oe
#PBS -q medium
#PBS -M thackray@mit.edu



source /etc/profile.d/modules.csh
module add intel




   limit  stacksize     2097152 kbytes
   setenv KMP_STACKSIZE 209715200
   setenv OMP_NUM_THREADS 8

cd @RUNDIR # cd to your run dir
while ( ! -e STOP )
if ( -e GO ) then
    rm GO
    rm -f logm # clear pre-existing log files 
    rm GCdone
    touch GCrunning
    time ./@EXECUTABLE > logm # time job; pipe output to log file 
    rm GCrunning
    touch GCdone
else
    sleep 2
endif
end
exit(0) # exit normally
