#!/usr/bin/python

#alarm handler configuration for iocmon

import pandas as pd

#_____________________________________________________________________________
class ioc():
    def __init__(self):
        self.name = ""

#_____________________________________________________________________________
class machine():
    def __init__(self):
        self.iocs = []

#_____________________________________________________________________________
def create_alh():

    #output alarm handler configuration
    alh = open("iocmon.alhConfig", "w")
    alh.write("GROUP STAR IOC_Monitor\n")
    alh.write("$COMMAND firefox https://online.star.bnl.gov/SlowControls2018/webioc.html > /dev/null 2>&1\n")
    alh.write("$GUIDANCE\n")
    alh.write("Call slow controls expert for alarm here\n")
    alh.write("$END\n")
    alh.write("\n")

    #prefix for PV names
    prefix = "iocmon"

    #load the configuration
    machines = {}
    machine_names = []
    csv = pd.read_csv("config.csv")
    for i in csv.iterrows():
        host = i[1]["host"].strip()
        inam = i[1]["ioc"].strip()

        if host not in machines:
            machines[host] = machine()
            machine_names.append(host)

        machines[host].iocs.append(inam)

    #machine and ioc names in alphabetical order
    machine_names.sort()
    for i in machines.itervalues():
        i.iocs.sort()

    #build the configuration
    for i in machine_names:
        alh.write("GROUP IOC_Monitor "+i+"\n")
        for j in machines[i].iocs:
            pvnam = prefix+":"+i+":"+j+":status"
            alh.write("CHANNEL "+i+" "+pvnam+" ---T-\n")
            alh.write("$ALIAS "+j+"\n")
        alh.write("\n")

#_____________________________________________________________________________
if __name__ == "__main__":

    create_alh()

    print "All done"



