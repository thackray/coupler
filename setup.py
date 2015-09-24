from templates import FileTemplate
import os
import sys

MODE = 'DEFAULT'
installdir = os.getcwd()
if len(sys.argv) > 2:
    if sys.argv[2] in ['--sandy', '-sandy','-s']:
        MODE = 'SANDY'

files_to_install = ['geossetup.sh.template','mitgcmsetup.sh.template',
                    'example.py.template', 'prepare_run_ecco_v4.template',
                    'prepare_run_input.template','runonce.sh','qsub_itXX.csh',
                    'sendgcm.sh','sendgeos.sh','startup.sh.template',
                    'subcoupler.sh','data.exch2.template']

template_locations = [os.path.join('setup_templates',ff) for ff 
                    in files_to_install]

if MODE == 'SANDY':
    template_locations[6] = os.path.join('setup_templates',
                                         'qsub_itXX.csh.template.sandy')
    template_locations[1] = os.path.join('setup_templates',
                                         'mitgcmsetup.sh.template.sandy')
    template_locations[11] = os.path.join('setup_templates',
                                         'data.exch2.template.sandy')

for fi,loc in zip(files_to_install,template_locations):
    T = FileTemplate(fi.split('.template')[0])
    T.load_template(loc)
    T.set_value('@INSTALLPATH',installdir)
    T.write()

print "setup mode: %s"%MODE
os.system('chmod +x mitgcmsetup.sh')
os.system('chmod +x geossetup.sh')
os.system('./mitgcmsetup.sh')
os.system('./geossetup.sh')
