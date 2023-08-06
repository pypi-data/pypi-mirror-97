MDPW
====
This package generates a PrettyMIDI object from Array of Array. 
Here is a sample code.
:: 

 import mdpw
 a = ['s',['n',64,1,64,1],['n',68,1,64,1],['n',71,1,64,1],
    ['c',['n',64,1,64,1],['n',68,1,64,1],['n',71,1,64,1]]]
 mdpw.compile(a, 120).write("hello.mid")


'n' means a note and followed values are pitch, duration, velocity and instrument. The instrument 129 means Drum.
's' means to play sequentially and 'c' means to play simultaneously.
