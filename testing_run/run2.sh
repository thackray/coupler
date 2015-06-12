## PBS directives 
## nb, PBS directives begin '#PBS'

#PBS -N run0
#PBS -l nodes=1:ppn=1
#PBS -j oe
#PBS -q debug
#PBS -M thackray@mit.edu


cd @RUNDIR
rm -f logm2 # clear pre-existing log files 

# copy geos into run dir
#cp /home/selin/geoschem/GEOS-Chem.v8-03-02/Code.v8-03-02/bin/geos geos
#cp /home/clf/Geos/geos-chem/GeosCore/geos geos

#run #1
time python dum2.py > logm2 # time job; pipe output to log file 




exit(0) # exit normally
