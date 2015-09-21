#!/bin/csh
#PBS -l nodes=1
#PBS -q xlong
source /etc/profile.d/modules.csh

module add matlab
cd @INSTALLPATH/MITgcm/verification/global_pcb_llc90/run
while ( ! -e STOP )
if ( -e SEND ) then
    rm SEND
    rm SENT
    touch SENDING
    matlab -nodesktop -nojvm -nodisplay -nosplash -r gcmtogeos -logfile gcmtogeos.log
    rm SENDING
    touch SENT
else
    sleep 2
endif
end

sleep 60
rm STOP
exit(0)
