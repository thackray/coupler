
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
          'mat_output_files':['gasdep_llc90.bin','partdep_llc90.bin',
                              'popgconc_llc90.bin'],
          'rundirname':'MITgcm/verification/global_pcb_llc90/run',
          'executable':'mitgcmuv',
          }

from models import GEOSChem, MITgcm
from coupler import Coupler
from datetime import datetime

M1 = GEOSChem(GCinfo)
M2 = MITgcm(MGinfo))
start_time, end_time = datetime(2005,6,7,0),datetime(2005,6,14,0)
step = 30*24
coupled = Coupler(start_time, end_time, step, model_objs=[M1,M2], 
                  check_frequency=5*60)
coupled.startup()
coupled.run()
