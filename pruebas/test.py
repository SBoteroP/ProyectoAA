import time
import sys
import os
from os import listdir,system

if len(sys.argv)>1 :
    name=sys.argv[1]
else:
    name="default"
monfichier= open(name)
text=monfichier.read()
monfichier.close()
text=text.split('\n')
del text[-1]
array=list()
for n in text :
    array.append(list(n))
    
print(array[0].index('A'))
i=0
j=0
while i< len(array) :
    while j<len(array[i]):
        if array[i][j]=='A':
            print([i,j])
        j+=1
    i+=1
output=[]
for d in array:
    for n in d:
        if n not in output:
            output.append(n)
    
print(len(output)-1)

