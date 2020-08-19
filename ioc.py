
#IOC running on a monitored machine

from softioc import builder

#_____________________________________________________________________________
class ioc:
    #_____________________________________________________________________________
    def __init__(self, config):

        #name for the pvs
        host = config["host"].strip()
        ioc = config["ioc"].strip()
        pvnam = host+":"+ioc

        #status pv
        self.pv_stat = builder.mbbIn(pvnam+":status",
                                     ("OK", 0),
                                     ("NOT_RUNNING", 1),
                                     ("MULTIPLE_INSTANCES", 2),
                                     ("DISCONNECTED", 3),
                                     ("UNDEFINED", 4)
        )

        #description pv
        desc = config["description"].strip(" \"'")
        self.pv_desc = builder.stringIn(pvnam+":description", initial_value=desc)

