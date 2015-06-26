#!/bin/csh

set workingdir=/path/to/here
set rundir=$workingdir/GEOS-Chem/run
mkdir $rundir
cd $rundir

cp /home/clf/Geos/GEOS-Chem.v9-01-03_wPAHs/Colins_PCBs/* .