
#IOC monitor

from time import sleep
import pandas as pd
from softioc import builder

from machine import machine

#_____________________________________________________________________________
class iocmon():
    #_____________________________________________________________________________
    def __init__(self):

        #prefix for the PVs
        builder.SetDeviceName("iocmon")

        #open the configuration
        csv = pd.read_csv("config.csv")

        #all slow controls machines
        self.machines = {}

        #load machines and iocs from the configuration
        for i in csv.iterrows():
            host = i[1]["host"].strip()

            if host not in self.machines:
                sleep(0.3)
                self.machines[host] = machine(i[1])

            self.machines[host].add_ioc(i[1])

    #_____________________________________________________________________________
    def start_update_loop(self):

        #start monitoring thread for each machine

        for i in self.machines.itervalues():
            sleep(0.3)
            i.daemon = True
            i.start()

