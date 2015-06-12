M1info = {'Name':'Dummy1',
          'rootdir':'M1',
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
          'rootdir':'M2',
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
          'done_tag':'restart.pops.LASTYYYYMMDDHH',
          'running_tag':'logm',
          'error_tag':'',
          'in_from':['MITgcm','GEOS-Chem'],
          'out_for':['MITgcm','GEOS-Chem'],
          'runscript':'runonce.sh',
          'input_files':['input.geos'],
          'executable':'geos',
          }

MGinfo = {'Name':'MITgcm',
          'rootdir':'MITgcm',
          'done_tag':'doney',
          'running_tag':'runney',
          'error_tag':'',
          'in_from':['GEOS-Chem','MITgcm'],
          'out_for':['GEOS-Chem','MITgcm'],
          'runscript':'r2.sh',
          'input_files':[''],
          'executable':'',
          }

from models import DummyM
from coupler import Coupler

M1 = DummyM(M1info)
M2 = DummyM(M2info)
start_time, end_time = 0,3
step = 1
coupled = Coupler(start_time, end_time, step, model_objs=[M1,M2])
coupled.run()
