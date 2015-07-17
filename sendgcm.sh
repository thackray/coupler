#!/bin/csh
#PBS -q short
source /etc/profile.d/modules.csh

module add matlab
cd @RUNDIR
while ( ! -e STOP )
if ( -e SEND ) then
    rm SEND
    rm MGsent
    touch MGsending
    matlab -nodesktop -nojvm -nodisplay -nosplash -r gcmtogeos -logfile gcmtogeos.log
    rm MGsending
    touch MGsent
else
    sleep 2
endif
end
exit(0)
