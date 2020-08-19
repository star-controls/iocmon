
#Slow controls machine running some IOCs

from subprocess import Popen, PIPE
import atexit
from threading import Timer, Thread
from time import sleep

from softioc import alarm

from ioc import ioc

#_____________________________________________________________________________
class machine(Thread):
    #_____________________________________________________________________________
    def __init__(self, config):
        Thread.__init__(self)

        #iocs running on the machine
        self.iocs = {}

        #command for ssh link to the machine
        host = config["host"].strip()
        user = config["user"].strip()
        self.uATh = user+"@"+host
        cmd = "ssh -T "+user+"@"+host

        #open the ssh
        print "Connecting to '"+host+"' as '"+user+"'"
        self.ssh = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)

        #close the ssh when exiting
        atexit.register(self.close_ssh)

        #update periodicity
        self.update_period = 60 # sec

        #timer to detect no response from the machine
        self.timeout = 120 # sec
        self.timer = Timer(self.timeout, self.set_invalid)
        self.timer.start()

    #_____________________________________________________________________________
    def update(self):

        #update status of running iocs in the machine

        #list the iocs on the machine
        try:
            self.ssh.stdin.write("screen -ls\n")
            self.ssh.stdin.flush()
        except:
            print "Exception in", self.uATh
            self.set_invalid()
            return

        #get output from the list command
        out = []
        while True:
            lin = self.ssh.stdout.readline().strip()
            #print line
            if len(lin) <=0: break
            out.append(lin)

        #extract running iocs from the output
        running_iocs = []
        #skip to the iocs
        while len(out) > 0:
            lin = out.pop(0)
            if lin.find("There are screens on:") >= 0: break
            if lin.find("There is a screen on:") >= 0: break
        #running ioc names
        while len(out) > 0:
            lin = out.pop(0)
            lin = lin.split()
            if len(lin) <= 0: continue
            lin = lin[0].split(".")
            if len(lin) != 2: continue

            running_iocs.append( lin[1] )

        #test for iocs in the machine
        for i in self.iocs.iterkeys():
            cnt = running_iocs.count(i)
            pv_stat = self.iocs[i].pv_stat
            #print cnt, i
            if cnt == 1:
                #ok
                pv_stat.set(0)
                continue
            if cnt <= 0:
                #not running
                pv_stat.set(1, alarm.MAJOR_ALARM, alarm.STATE_ALARM)
                continue
            if cnt > 1:
                #multiple instances
                pv_stat.set(2, alarm.MAJOR_ALARM, alarm.STATE_ALARM)
                continue
            #undefined by the above
            pv_stat.set(4, alarm.MAJOR_ALARM, alarm.STATE_ALARM)

        #reset the timer
        self.reset_timer()

    #_____________________________________________________________________________
    def run(self):

        #periodically run the update via the Thread
        while True:
            self.update()
            sleep(self.update_period)

    #_____________________________________________________________________________
    def add_ioc(self, config):

        #add ioc to the machine

        nam = config["ioc"].strip()
        self.iocs[nam] = ioc(config)

    #_____________________________________________________________________________
    def set_invalid(self):

        #raise invalid alarm for iocs in the machine
        for i in self.iocs.itervalues():
            i.pv_stat.set(3, alarm.INVALID_ALARM, alarm.TIMEOUT_ALARM)

    #_____________________________________________________________________________
    def reset_timer(self):

        #reset the timer at the end of update

        self.timer.cancel()
        self.timer = Timer(self.timeout, self.set_invalid)
        self.timer.start()

    #_____________________________________________________________________________
    def close_ssh(self):

        #close the ssh connection
        print "Closing ssh for", self.uATh

        self.ssh.stdin.close()
        self.ssh.terminate()



