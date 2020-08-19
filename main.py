#!/usr/local/epics/modules/pythonIoc/pythonIoc

from softioc import softioc, builder
from iocmon import iocmon

#monitor instance
mon = iocmon()

#load the ioc
builder.LoadDatabase()
softioc.iocInit()

#start the monitoring loop
mon.start_update_loop()

#open the ioc shell
softioc.interactive_ioc(globals())

