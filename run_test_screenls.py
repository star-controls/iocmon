#!/usr/bin/python

#run screen -ls on a remote machine

from subprocess import Popen, PIPE, STDOUT
from time import sleep
from datetime import datetime

#cmd = "ssh -T sysuser@softioc4"
cmd = "ssh -T sysuser@bermuda"
#cmd = "ssh -T sysuser@alh2"
#cmd = "tcsh"

ssh = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)

sleep(10)

#ssh.stdin.write("screen -ls\n")
#ssh.stdin.flush()

#for i in xrange(9):
#while True:
#    line = ssh.stdout.readline().rstrip()
#    print line
#    if len(line) <=0: break

while True:
    try:
        ssh.stdin.write("screen -ls\n")
        ssh.stdin.flush()

        while True:
            line = ssh.stdout.readline().rstrip()
            print line
            if len(line) <=0: break

        print datetime.now().date(), datetime.now().time()
        sleep(10)

    except KeyboardInterrupt:
        print
        break

#ssh.stdin.write("date\n")
#print ssh.stdout.readline()

ssh.stdin.close()

ssh.terminate()


