"""
This module reads, supplies and updates the current 'measurement ID', a running number on each setup.
A two letter identifier of each setup, e.g., AT for Attocube, Pr for probe station, He for Heliox  etc. is also saved in this file.
Both are read in the sweep function sweepAndSave() each time a measurement is done.
"""
# This has to be set every time pyNe is installed on a new system. It denotes the path where the unique number is saved.
import platform
import os
import json
# preFix = {'Darwin':'', # THis just gives the right prefix for MAc ('Darwin' and Windows)
#           'Windows':'../'}

relPath = os.path.realpath(__file__)[:-15] #Giving the full path without the GlobalMeasID.py script ending
filePath =  relPath + 'GlobalMeasIDBinary'




def init(preFix = 'A',ID= 0):
    with open(filePath, 'w') as file:
     file.write(json.dumps({'currentPreFix':preFix,preFix:ID
                           }))

def  addPrefix(newPreFix):
    with open(filePath, 'r') as file:
        # print(file.read())
        inputDic=  json.loads(file.read())
        inputDic = {newPreFix:0,**inputDic}
    with open(filePath, 'w') as file:
        file.write(json.dumps(inputDic))
        print(f'Succesfully added the new measurement preFix/Setup: {newPreFix}')


def readCurrentID():
    with open(filePath, 'r') as file:
        Dict = json.loads(file.read())
        return Dict[Dict['currentPreFix']]

def listIDs():
    with open(filePath, 'r') as file:
        Dict = json.loads(file.read())
        current = f"Currently used Prefix/Setup: {Dict['currentPreFix']}  --> ID = {Dict[Dict['currentPreFix']]} \n -------------------------- \nOther available Setups/Prefixes are: "
        print(current)
        retString = ''
        retString = retString.join(current+'\n')
        for key,item in Dict.items():
            if (key !='currentPreFix' and key != Dict['currentPreFix']):
                print(f"Prefix/Setup: {key}  --> ID = {item}")
                retString = retString.join(f"Prefix/Setup: {key}  --> ID = {item}\n")

        # return retString
def increaseID():
    with open(filePath, 'r') as file:
        # print(file.read())
        inputDic=  json.loads(file.read())
        inputDic[inputDic['currentPreFix']] = str(int(inputDic[inputDic['currentPreFix']]) + 1)
    with open(filePath, 'w') as file:
        file.write(json.dumps(inputDic))

def setCurrentSetup(preFix):
    with open(filePath, 'r') as file:
        Dict = json.loads(file.read())
        previousPrefix = Dict['currentPreFix']
    if preFix in Dict.keys():

        if previousPrefix == preFix:
            print(f'Using current Id/Prefix: {previousPrefix}')
            pass
        else:
            Dict['currentPreFix'] = preFix
            with open(filePath, 'w') as file:
                file.write(json.dumps(Dict))
                print(f'Succesfully changed preFix/Setup from: {previousPrefix} ---> {preFix}')
    else:
        print(listIDs())
        raise Exception(f'Prefix not defined!!\n Currently defined prefixes can be listed by usign the listIDs() function.\n Define the desired prefix first using the addPrefix(newPrefix) method')

def readCurrentSetup():
    with open(filePath, 'r') as file:
        Dict=  json.loads(file.read())
        return Dict['currentPreFix']


#def readCurrentID():
#        IDTXT =open(IDpath,"r")
#        ID = int(IDTXT.read())
#        IDTXT.close()
#        return(ID) 
#    
#def increaseID():
#        ID = readCurrentID()
#        IDTXT =open(IDpath,"w")
#        IDTXT.write(str(ID+1))
#        IDTXT.close()
#def readCurrentSetup():
#    return currentSetup
#        
#def init():
#    """Creates a new ID file at the path specified in variable 'Idpath'. Should only be called if the ID file was deleted etc. """
#    IDTXT =open(IDpath,"w")
#    IDTXT.write(str(0))
#    IDTXT.close()
    