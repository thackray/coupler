# dummy model 2
print "Dummy 2 is now running"
input_stuff = open('input2.txt','r').read()
print input_stuff
print "Dummy 2 is done, stopping"
with open('twoisdone.txt','w') as f:
    f.write('Bye bye')
