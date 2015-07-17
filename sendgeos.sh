#!/bin/csh -f
#PBS -q xlong
source /etc/profile.d/modules.csh

module add matlab
cd @RUNDIR
while ( ! -e STOP )
if ( -e SEND ) then
    rm SEND
    rm GCsent
    touch GCsending
    matlab -nodesktop -nojvm -nodisplay -nosplash -r geostogcm -logfile geostogcm.log
    rm GCsending
    touch GCsent
else
    sleep 2
endif
end
exit(0)
