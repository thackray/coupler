M1info = {'Name':'Dummy1',
          'rootdir':'/home/thackray/mitgcm_geoschem_mix/testing_run/M1',
          'done_tag':'oneisdone.txt',
          'running_tag':'logm1',
          'error_tag':'',
          'in_from':['Dummy1','Dummy2'],
          'out_for':['Dummy2','Dummy1'],
          'runscript':'run1.sh',
          'input_files':['input1.txt'],
          'executable':'dum1.py',
          }

M2info = {'Name':'Dummy2',
          'rootdir':'/home/thackray/mitgcm_geoschem_mix/testing_run/M2',
          'done_tag':'twoisdone.txt',
          'running_tag':'logm2',
          'error_tag':'',
          'in_from':['Dummy1','Dummy2'],
          'out_for':['Dummy2','Dummy1'],
          'runscript':'run2.sh',
          'input_files':['input2.txt'],
          'executable':'dum2.py',
          }


GCinfo = {'Name':'GEOS-Chem',
          'rootdir':'GEOS-Chem',
          'done_tag':'GCdone',
          'running_tag':'GCrunning',
          'error_tag':'GCerror',
          'in_from':['MITgcm'],
          'out_for':['MITgcm'],
          'runscript':'runonce.sh',
          'input_files':['input.geos'],
          'share_script':'geostogcm.m',
          'mat_share_script':'sendgeos.sh',
          'mat_output_files':['evasion_latlon.nc'],
          'rundirname':['GEOS-Chem/run']
          'executable':'geos',
          }

MGinfo = {'Name':'MITgcm',
          'rootdir':'MITgcm',
          'done_tag':'MGdone',
          'running_tag':'MGrunning',
          'error_tag':'MGerror',
          'in_from':['GEOS-Chem'],
          'out_for':['GEOS-Chem'],
          'runscript':'qsub_itXX.sh',
          'input_files':['data',],
          'share_script':'gcmtogeos.m',
          'mat_share_script':'sendgcm.sh',
          'mat_output_files':['gasdep_llc90.bin','partdep_llc90.bin'],
          'rundirname':'MITgcm/verification/global_pcb_llc90/run',
          'executable':'mitgcmuv',
          }

from models import GEOSChem, MITgcm
from coupler import Coupler
from datetime import datetime

M1 = GEOSChem(GCinfo)
M2 = MITgcm(MGinfo))
start_time, end_time = datetime(2005,6,7,0),datetime(2005,6,14,0)
step = 7*24
coupled = Coupler(start_time, end_time, step, model_objs=[M1,M2], 
                  check_frequency=5*60)
coupled.startup()
coupled.run()
