#!/bin/csh -f
#PBS -l nodes=1
#PBS -q xlong
source /etc/profile.d/modules.csh

module add matlab
cd @INSTALLPATH/GEOS-Chem/run
while ( ! -e STOP )
if ( -e SEND ) then
    rm SEND
    rm SENT
    touch SENDING
    matlab -nodesktop -nojvm -nodisplay -nosplash -r geostogcm -logfile geostogcm.log
    rm SENDING
    touch SENT
else
    sleep 2
endif
end
exit(0)
