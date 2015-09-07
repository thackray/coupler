
GCinfo = {'Name':'GEOS-Chem',
          'rootdir':'/home/thackray/coupler_test',
          'in_from':['MITgcm'],
          'out_for':['MITgcm'],
          'input_files':['input.geos','regrid_dep_ll2llc.m','GC_gridinfo.m',
			   'areas_4x5_m2.dat'],
          'share_script':'geostogcm.m',
          'mat_output_files':['gasdep_llc90.bin','partdep_llc90.bin',
                              'popgconc_llc90.bin'],
          'rundirname':'GEOS-Chem/run',
          }

MGinfo = {'Name':'MITgcm',
          'rootdir':'/home/thackray/coupler_test',
          'in_from':['GEOS-Chem'],
          'out_for':['GEOS-Chem'],
	  'input_files':['data','data.pcb','data.diagnostics',
                         'regrid_evas_llc2ll.m'],
          'share_script':'gcmtogeos.m',
          'mat_output_files':['evasion_latlon.nc'],
          'rundirname':'MITgcm/verification/global_pcb_llc90/run',
          }

from models import GEOSChem, MITgcm
from coupler import Coupler
from datetime import datetime

M1 = GEOSChem(GCinfo)
M2 = MITgcm(MGinfo)
start_time, end_time = datetime(2000,1,1,0),datetime(2001,1,1,0)
step = 21*24
coupled = Coupler(start_time, end_time, step, model_objs=[M1,M2], 
                  check_frequency=10)
coupled.startup()
coupled.run()
