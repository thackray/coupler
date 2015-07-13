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
while ([ ! -f STOP ])
if ([ -f GO ])
then
    rm GO
    rm -f logm # clear pre-existing log files 
    rm GCdone
    touch GCrunning
# copy geos into run dir
#cp /home/selin/geoschem/GEOS-Chem.v8-03-02/Code.v8-03-02/bin/geos geos
#cp /home/clf/Geos/geos-chem/GeosCore/geos geos

#run #1
    time ./@EXECUTABLE > logm # time job; pipe output to log file 
    rm GCrunning
    touch GCdone
else
    sleep 2
fi
end



exit(0) # exit normally
