# INPUT: C# Process '!!war' command with various args
# PROCESS: Using data.py
# OUTPUT: Unparsed string for parsing in C# CommandHandler
import sys
from data import DataHandler as Dh

dh = Dh() # processor (successful print outputs into C# process) 
a = sys.argv # input arguments

try:print(dh.commands[a[1]](a[2],a[3],a[4],a[5],a[6]))
except:
    try:print(dh.commands[a[1]](a[2],a[3]))
    except:
        try:print(dh.commands[a[1]](a[2]))
        except:
            try:print(dh.commands[a[1]]())
            except Exception as e:print(e)
