from models import FileTemplate
import os
import sys

if len(sys.argv) < 3:
    installdir = os.getcwd()
else:
    installdir = os.path.join(os.getcwd(),sys.argv[1])


files_to_install = ['geossetup.sh.template','mitgcmsetup.sh.template',
                    'example.py.template', 'prepare_run_ecco_v4.template',
                    'prepare_run_input.template','startup.sh.template']

for fi in files_to_install:
    T = FileTemplate(fi.rstrip('template').rstrip('.'))
    T.load_template(fi)
    T.set_value('@INSTALLPATH',installdir)
    T.write()

os.system('chmod +x mitgcmsetup.sh')
os.system('chmod +x geossetup.sh')
os.system('./mitgcmsetup.sh')
os.system('./geossetup.sh')
