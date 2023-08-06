"""
@author: Adam Micolich
Updated by Jakob Seidl
This module does the input handling for the USB-6216, which is effectively a pair of analog outputs
and a set of 8 analog inputs. The output handling is done by a separate .py. 
"""

import pyneMeas.Instruments.Instrument as Instrument
import nidaqmx as nmx


@Instrument.enableOptions
class USB6216In(Instrument.Instrument):
    # Default options to set/get when the instrument is passed into the sweeper
    defaultInput = "inputLevel"
    defaultOutput = "None"

    def __init__(self, address,usbPort = 'Dev1'):
        super(USB6216In, self).__init__()
        self.dev = address
        self.usbPort = usbPort
        self.type ="USB6216"  #We can check each instrument for its type and react accordingly
        self.name = "myUSB6216"

        # Define the self.port which is the handle to the device
        if self.dev in [*range(8)]:
            self.port = f"{self.usbPort}/ai{self.dev}"
            
        else: raise ValueError(f'Please insert a valid Input port for the NIDaQ ranging from 0 to 7. You entered {self.dev}')
        
    @Instrument.addOptionSetter("name")
    def _setName(self,instrumentName):
         self.name = instrumentName
         
    @Instrument.addOptionGetter("name")
    def _getName(self):
        return self.name
        
    @Instrument.addOptionGetter("inputLevel")
    def _getInputLevel(self):
        with nmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(self.port)
            tempData = task.read()
        measInput = float(tempData)/self.scaleFactor        
        return measInput
    
    @Instrument.addOptionGetter("scaleFactor")
    def _getScaleFactor(self):
        return self.scaleFactor
    
    @Instrument.addOptionSetter("scaleFactor")
    def _setScaleFactor(self,scaleFactor):
        self.scaleFactor = scaleFactor
            
    def goTo(self,target,stepsize=0.001,delay=0.02):
        pass
            
    def close(self):
        pass