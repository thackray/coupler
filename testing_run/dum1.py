# dummy model 1
print "Dummy 1 is running"
input_stuff = open('input1.txt','r').read()
print input_stuff
print "Dummy 1 is stopping"
with open('oneisdone.txt','w') as f:
    f.write("later gater")
