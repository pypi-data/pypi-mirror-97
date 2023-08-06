# -*- coding: utf-8 -*-
"""
VERSION 4.0
@author: Jakob Seidl
jakob.seidl@nanoelectronics.physics.unsw.edu.au
"""
import time

import pyneMeas.Instruments.Instrument as Instrument

@Instrument.enableOptions
class TimeMeas(Instrument.Instrument):
    """Creates a TimeMeas virtual instrument that can set time (setter) or measure the elapsed time during a measurement.

    :param
    :return: TimeMeas instance

    >>> TimeMeas(0.5)
    <Instruments.TimeMeas.TimeMeas object at 0x10fcc5790>
    """


    defaultOutput = "sourceLevel"
    defaultInput = "timeStamp"
    def __init__(self):
        super(TimeMeas,self).__init__()
        # self.timeInterval = timeInterval
        self.initTime = time.time()
        self.type = 'TimeMeas'
        self.name = 'myTimeMeas'
        self.dummyPoint = 0
    
    @Instrument.addOptionSetter("sourceLevel")
    def _dummySourceFunction(self,dummyVariable):
        # time.sleep(self.timeInterval)
        self.dummyPoint = dummyVariable

    @Instrument.addOptionGetter("sourceLevel")
    def _dummyReadSourceFunction(self):
        # time.sleep(self.timeInterval)
        return self.dummyPoint

    @Instrument.addOptionGetter("type")
    def _getInstrumentType(self):
        return self.type
    @Instrument.addOptionGetter("timeStamp")
    def _getTime(self):
        return time.time()-self.initTime
    
    @Instrument.addOptionSetter("name")
    def _setName(self,instrumentName):
         self.name = instrumentName

    @Instrument.addOptionGetter("name")
    def _getName(self):
        return self.name

    @Instrument.addOptionSetter("timeStampReset")
    def _setTimeReset(self):
        """ By default, TimeMeas measures the time passed since it's creation in the beginning of a script. For more accurate time values,
            execute myTimeMeas.set("timeStampReset") before executing the sweepAndSave(...) function"""
        self.initTime = time.time()
    
    def goTo(target = 0.1,delay = 0.2,stepsize = 0.2): #Dummy function. Is required for every class to be passed to the sweep functin.
        return

