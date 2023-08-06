import sys
import os
import re

sys.path.append('..')

from waapi import WaapiClient
from pprint import pprint
from csg_helpers import soundbank_helper
import operator

client = None



def connect(port=8095):
    """ Connect to Wwise authoring api , on default port 8095 or an alternative port.
    This sets up the client used for all future calls in the same session, so should be called before any other functions

    :param port: The waapi port to use (default 8095)
    :return: wwise connection info structure OR False

    """
    global client
    try:
        client = WaapiClient(url="ws://127.0.0.1:{0}/waapi".format(port))
    except Exception as ex:
        print("Connection error: {}".format(ex))
        print("Error connecting to Wwise. Please check your Waapi settings in User Preferences (wamp port expecting 8095) .....exiting")
        #input('Press <ENTER> to continue')
        return False
        #sys.exit()
    else:
        result = client.call("ak.wwise.core.getInfo")
        return result

def exit():
    """Exiting the connection. Also clears automation mode

    """
    automationMode(False)
    try:
        client.disconnect()
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getClient():
    """Getter for the waapi client connection

    """
    return client

def call(procedure,arguments):
    """Support manually calling a waapi procedure with custom arguments

    :param procedure: The name of the waapi procedure to call
    :param arguments: The argument map to pass to procedure

    :return: Result structure or False

    """
    try:
        res = client.call(procedure,arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

############# Function definitions #########################################

### Project undo and save ######

def beginUndoGroup():
    """Begin an undo group

    """
    try:
        res = client.call("ak.wwise.core.undo.beginGroup")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def cancelUndoGroup():
    """Cancel an undo group

        """
    try:
        res = client.call("ak.wwise.core.undo.cancelGroup")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def endUndoGroup(undogroup):
    """Name and end an undo group

    :param undogroup: Name to give the undo group that is ending

    """
    undoArgs = {"displayName": undogroup}
    try:
        res = client.call("ak.wwise.core.undo.endGroup", undoArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def saveWwiseProject():
    """Save the wwise project

    """
    try:
        res = client.call("ak.wwise.core.project.save")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setupSubscription(subscription, target, returnArgs = ["id", "name", "path"]):
    """Subscribe to an event. Define a target to call when triggered, get the retunArgs back

    :param subscription: Waapi subscription topic
    :param target: The function to run on the callback trigger
    :param returnArgs: Properties to return with the callback

    """
    try:
        res = client.subscribe(subscription, target, {"return": returnArgs})
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def getProjectInfo(additionalProperties=[]):
    """Get the wwise project info by default returns filePath, @DefaultLanguage

    :param additionalProperties: List of additional properties to return from the project (optional)
    :return: Results structure or False

    """
    arguments = {
        "from": {"ofType": ["Project"]},
        "options": {
            "return": ["type","id", "name", "filePath","@DefaultLanguage"]+additionalProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get",arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None and len(res["return"]) > 0:
            return res["return"][0]
        else:
            return False

def getLanguages():
    """Get the list of languages from the wwise project

    :return: List of languages

    """
    langlist=[]
    arguments = {
        "from": {"ofType": ["Language"]},
        "options": {
            "return": ["name"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            for lang in res["return"]:
                if lang['name'] != 'SFX' and lang['name'] != 'External' and lang['name'] != 'Mixed':
                    langlist.append(lang['name'])
            return langlist
        else:
            return []

def getPathToWwiseProjectFolder():
    """Gets a path to the root folder of wwise project, cleans any nonsense from Mac paths.

    :return: os.path formated path to the wwise folder on disk

    """
    projectInfo = getProjectInfo()
    WwiseProjectPath = projectInfo["filePath"]
    WwiseProjectPath = WwiseProjectPath.replace("Y:", "~").replace('\\', '/')
    pathToWwiseFolder = os.path.expanduser(os.path.dirname(WwiseProjectPath))
    return pathToWwiseFolder


###  Object creation and property setting ######
def createWwiseObject(parentID, otype="BlendContainer", oname="", conflict="merge"):
    """Create a wwise object of type otype, called oname, underneath

    :param parentID: The GUID of the parent object
    :param otype: The type of wwise object to create
    :param oname: The name to give the new object
    :param conflict: Behaviour for conflicting objects (default=merge)

    :return: The newly created wwise object structure or False

    """
    createObjArgs = {
        "parent": parentID,
        "type": otype,
        "name": oname,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.create", createObjArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def createWwiseObjectFromArgs(args = {}):
    """Create a wwise object from a custom argument structure.
    Useful if you need to create many complex objects.

    :param args: A map of custom arguments for ak.wwise.core.object.create
    :return: The newly created wwise object(s) or False

    """
    try:
        res = client.call("ak.wwise.core.object.create", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setProperty(objectID, property, value,platform=None):
    """Set a property of a wwise object

    :param objectID: GUID of the object
    :param property: Name of the property to set
    :param value: The value to set for given property
    :param platform: Optional. The platform to apply the property for
    :return: Result structure or False

    """
    setPropertyArgs = {
        "object": objectID,
        "property": property,
        "value": value
    }
    if platform:
        setPropertyArgs["platform"]=platform
    try:
        res = client.call("ak.wwise.core.object.setProperty",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setPropertyPerPlatform(object, property, value, platform):
    """Set a property of a wwise object

    :param object: GUID of the object
    :param property: Name of the property to set
    :param value: The value to set for given property
    :param platform: The platform to apply this property to
    :return: Result structure or False

    """
    setPropertyArgs = {
        "object": object,
        "property": property,
        "value": value,
        "platform": platform
    }
    try:
        res = client.call("ak.wwise.core.object.setProperty",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setReference(objectID, reference, value,platform=None):
    """Set a reference of a wwise object

    :param objectID: GUID of the object
    :param reference: Name of the reference to set
    :param value: The value to set for given property
    :param platform: Optional. The platform to apply the reference for
    :return: Result structure or False

    """
    setArgs = {
        "object": objectID,
        "reference": reference,
        "value": value
    }
    if platform:
        setArgs["platform"]=platform
    try:
        res = client.call("ak.wwise.core.object.setReference",setArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setNotes(objectID, value):
    """Set the notes of object to value

    :param objectID: GUID of the object
    :param value: String to set as notes
    :return: Result structure or False

    """
    setPropertyArgs = {
        "object": objectID,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setNotes",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def importAudioFiles(args):
    """Import audio files with custom args

    :param args: A map of custom arguments for ak.wwise.core.audio.import
    :return: Result structure or False

    """
    try:
        res = client.call("ak.wwise.core.audio.import", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setupImportArgs(parentID, fileList,originalsPath,language="SFX"):
    """Helper function to construct args for import operation

    :param parentID: GUID of the parent object
    :param fileList: List of audio files to import
    :param originalsPath: Relative location to put new files inside Originals
    :param language: Import audio as SFX (default) or a given language
    :return: An arguments structure ready to be passed into importAudioFiles()

    """
    ParentID = str(parentID)
    importFilelist = []
    if language != "SFX":
        type = "<Sound Voice>"
    else:
        type = "<Sound SFX>"

    for audiofile in fileList:
        foo = audiofile.rsplit('.') #remove extension from filename
        audiofilename = foo[0]
        importFilelist.append(
            {
                "audioFile": audiofile,
                "objectPath": type + os.path.basename(audiofilename)
            }
        )

    importArgs = {
        "importOperation": "useExisting",
        "autoAddToSourceControl": True,
        "default": {
            "importLanguage": language,
            "importLocation": ParentID,
            "originalsSubFolder": originalsPath
            },
        "imports": importFilelist
        }
    return importArgs


def deleteWwiseObject(objectID):
    """Delete a wwise object

    :param objectID: GUID of object to be deleted
    :return: Result structure or False

    """
    args = {"object":objectID}
    try:
        res = client.call("ak.wwise.core.object.delete",args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

###  Searching the project  ######

def getSelectedObjects(properties=[]):
    """Get the currently selected object(s), returning any extra properties.
    By default objects will return ["id","type", "name", "path"] + properties[]

    :param properties: list of additional properties to be returned for the wwise objects.
    :return: Result structure or False

    """
    baseProperties = ["id","type", "name", "path"]
    selectedObjectArgs = {
        "options": {
            "return": baseProperties+properties
        }
    }
    try:
        res = client.call("ak.wwise.ui.getSelectedObjects",selectedObjectArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["objects"]
        else:
            return []

def getDescendantObjectsOfType(objectID,ofType,returnProperties=[],tfrom="id",select="descendants"):
    """Perform a search fromObject to find descendants ofType, return additional properties for each object.
    Optionally change the from and select parts of the query, by default use ID as the object
    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    :param objectID: Starting point of search. Default is a GUID
    :param ofType: Type of wwise objects to search for
    :param returnProperties: Additional properties to return for each object
    :param tfrom: Key that determines how fromObject is used in the search (default=id)
    :param select: Key that determines which objects are searched in relation to the fromObject (default=descendants)
    :return: Result structure or False

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [objectID]},
        "transform": [
            {"select": [select]},
            {"where":["type:isIn",[ofType]]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getDescendantObjects(objectID,returnProperties=[],tfrom="id",select="descendants"):
    """Perform a search fromObject to find all descendants, return additional properties for each object.
    Optionally change the from and select parts of the query, by default use ID as the object

    :param objectID: Starting point of search.
    :param returnProperties: Additional properties to return for each object
    :param tfrom: Key that determines how fromObject is used in the search (default=id)
    :param select: Key that determines which objects are searched in relation to the fromObject (default=descendants)
    :return: Result structure or False

    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [objectID]},
        "transform": [
            {"select": [select]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []


def getObjectsByName(name,type,returnProperties=[],tfrom="ofType"):
    """Perform a search by name, return additional properties for each object.
    Named search must also include a type filter.
    For more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    :param name: String to match with object names
    :param type: Type of wwise objects to search for
    :param returnProperties: Additional properties to return for each object
    :param tfrom: Key that determines how fromObject is used in the search (default=ofType)
    :return: Result structure or False

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [type]},
        "transform": [
            #{"where": ["name:matches",[name]]}
            {"where": ['name:matches', '^'+name+'$']}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def searchForObject(searchterm,returnProperties=[],tfrom="search"):
    """Perform a search by name, return additional properties for each object.
    For more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    :param searchterm: String to search for
    :param returnProperties: Additional properties to return for each object
    :param tfrom: Type of search to do, defaults to "search" can be overridden to use path
    :return: Result structure or False

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [searchterm]},
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getObjectProperties(objectID,returnProperties=[],tfrom="id"):
    """Get some additional properties from a wwise Object, by default use ID as the object

    :param objectID: Wwise object to get properties from. Default is a GUID
    :param returnProperties: Additional properties to return for each object
    :param tfrom: Key that determines how fromObject is used in the search (default=id)
    :return: Result structure or False
    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [objectID]},
        "transform": [],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None and len(res["return"])>0:
            if len(res["return"]) > 1:
                return res["return"]
            else:
                if len(res["return"]) > 0:
                    return res["return"][0]
                else:
                    return False
        else:
            return []

def getAllObjectsOfType(ofType,returnProperties=[]):
    """Get all objects of a certain type, and return any extra properties

    :param ofType: Type of wwise objects to search for
    :param returnProperties: Additional return properties to get for each object
    :return: Result structure or False

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {"ofType": [ofType]},
        "transform": [
            #{"select": "parent"}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getReferencesToObject(objectID,returnProperties=[],tfrom="id"):
    """ get the references to a given object, by default use ID as the object

    :param fromObject: Wwise object to get references to. Default is a GUID
    :param returnProperties: Additional properties to return for each object
    :param tfrom: Key that determines how fromObject is used in the search (default=id)
    :return: Results structure or False

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [objectID]},
        "transform": [
            {"select": ["referencesTo"]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getListOfTypes():
    """return the list of valid object types, can help debugging"""
    try:
        res = client.call("ak.wwise.core.object.getTypes")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def filterWwiseObjects(objects,property,operation, value, NOT=0):
    """helper function to filter a list of objects by a specific property, value and comparison operation
    # e.g. return only objects with "@Volume" , "<" , "-48"

    :param objects: List of wwise objects to filter
    :param property: Which property to filter by
    :param operation: String comparison operator for filter. One of; "==","<","<=",">",">=","!=","contains"
    :return: List of objects matching filters
    """
    results = []
    op = getOperator(operation)
    for obj in objects:
        if not property in obj:## this object doesnt have the property, so skip it
            continue
        if NOT ==0:
            if op(obj[property],value):
                results.append(obj)
        else:
            if not op(obj[property],value):
                results.append(obj)
    return results

def getOperator(string):
    """Helper function to convert string comparison to python operator"""
    if string == "==":
        return operator.eq
    elif string == "<":
        return operator.lt
    elif string == "<=":
        return operator.le
    elif string == ">":
        return operator.gt
    elif string == ">=":
        return operator.ge
    elif string == "!=":
        return operator.ne
    elif string == "contains":
        return operator.contains
    else:
        print("WARNING!!! Did not recognise operator argument..defaulting to EQUALS")
        return operator.eq


#####  Soundbanks #####
def generateSoundbanks(banklist = []):
    """Generate soundbanks

    :param banklist: List of bank names to generate
    """
    args = {
        "command": "GenerateSelectedSoundbanksAllPlatforms",
        "objects": [
            banklist
        ]
    }
    try:
        res = client.call("ak.wwise.ui.commands.execute", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def getSoundbanks(objectID,tfrom="id"):
    """ Return all Soundbanks referencing any object of the Work Unit directly

    :param objectID: The object GUID to use in the search
    :param tfrom: Key that determines how obj is used in the search (default=id)
    :return: List of banks directly referencing obj
    """
    BankList =[]
    for transform in soundbank_helper.bankTransforms:
        arguments = {
            "from": {tfrom: [objectID]},
            "transform": transform,
            "options": {
                "return": ['id', 'name', 'type']
            }
        }
        try:
            res = client.call("ak.wwise.core.object.get", arguments)
        except Exception as ex:
            print("call error: {}".format(ex))
            return False
        else:
            if res != None:
                # print (res.kwresults["return"])
                for bank in res["return"]:
                    if bank["name"] not in BankList:
                        BankList.append((bank["name"]))
    return BankList


def executeCommand(command,objects = []):
    """wrapper to execute UI commands
    See https://www.audiokinetic.com/library/2017.1.9_6501/?source=SDK&id=globalcommandsids.html

    :param command: Command to execute
    :param objects: List of objects to pass to the command
    :return: Result structure or False
    """
    args = {}
    if type(objects) is list:
        args = {
            "command": command,
            "objects": objects
        }
    else:
        args = {
            "command": command,
            "objects": [
                objects
            ]
        }
    try:
        res = client.call("ak.wwise.ui.commands.execute", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def automationMode(enabled):
    """set automation mode on/off

    :param enabled: True or False

    :return: Result struct or False

    """
    args = {
        "enable": enabled
    }
    try:
        res = client.call("ak.wwise.debug.enableAutomationMode", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def checkoutWorkUnit(workunitID):
    """Source control operation to check out work unit

    :param workunitID: GUID of the work unit to checkout
    :return: Result structure or False
    """
    return executeCommand("WorkgroupCheckoutWWU",workunitID)

def cleanfilePathFromWwise(path):
    """Cleans the undesired characters from Mac paths that Wwise gives you. E.g. replaces Y: with ~

    :param path: path to clean (e.g. wproj or work unit path)
    :return: os.path formated path, cleaned of Mac/WINE characters
    """
    cleanMacpath = path.replace("Y:","~").replace('\\', '/')
    return os.path.abspath(os.path.expanduser(cleanMacpath))

def showObjectsInListView(objects = []):
    """Open the provided list of objects in the Wwise List View

    :param objects: A List of object IDs, paths or type qualified names
    :return: Result structure or False
    """
    try:
        res = executeCommand("ShowListView",objects)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setSwitchContainerAssignment(switch,child):
    """Assign a given child object to a given switch (switch container)

    :param switch: Name of the switch to assign child to
    :param child: ID of the wwise object to assign to switch
    :return: Result structure or False
    """
    args = {
        "stateOrSwitch": switch,
        "child":child
    }
    try:
        res = client.call("ak.wwise.core.switchContainer.addAssignment", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def removeSwitchContainerAssignment(switch,child):
    """Remove a given child object from a given switch (switch container)

    :param switch: Name of the switch to assign child to
    :param child: ID of the wwise object to assign to switch
    :return: Result structure or False
    """
    args = {
        "stateOrSwitch": switch,
        "child":child
    }
    try:
        res = client.call("ak.wwise.core.switchContainer.removeAssignment", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def moveWwiseObject(objectID,parent, conflict="replace"):
    """move object to new location under parent

    :param objectID: ID of wwise object to move
    :param parent: ID of the parent to move object under
    :param conflict: Behaviour for conflicting objects (default = replace)
    :return: Result structure or False

    """
    args = {

        "object": objectID,
        "parent": parent,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.move", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def renameWwiseObject(objectID,newName):
    """Rename a given object with newName

    :param objectID: ID of wwise object to rename
    :param newName: The new name of the wwise object
    :return: Result structure or False

    """
    args = {

        "object": objectID,
        "value": newName
    }
    try:
        res = client.call("ak.wwise.core.object.setName", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def copyWwiseObject(objectID, parent, conflict="replace"):
    """copy object to new location under parent
    
    :param objectID: ID of wwise object to copy
    :param parent: ID of the parent to paste object under
    :param conflict: Behaviour for conflicting objects (default = replace)
    :return: Result structure or False
    """
    args = {

        "object": objectID,
        "parent": parent,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.copy", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def isStringValidID(string):
    """Check if a given string is formatted as a valid ID, using regex fullmatch with pattern - ^\{[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\}$

    :param string: The string to match against the regex ID pattern
    :return: True if string matches the pattern of a wwise ID, otherwise  False

    """
    IDRegExPattern = r"^\{[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\}$"
    result = re.fullmatch(IDRegExPattern,string)
    if result:
        return True
    else:
        return False

def createStructureFromPath(path,parent):
    r"""Create a structure of objects from a string path

    :param path: String path of the structure to be created. Objects should be seperated by double backslash (\\) and type should prefix name in angle brackets <> e.g <WorkUnit>MyWorkUnit
    :param parent: ID or path of the parent object to create the structure under e.g. \\\\Actor-Mixer Hierarchy
    :return: The last descendent object in the path created

    e.g. res = csg_pywaapi.createStructureFromPath("<WorkUnit>Hello\\\\<Folder>World", "\\\\Actor-Mixer Hierarchy")
    """
    if not parent or not path:
        print("Error. Missing arguments")
        return False


    isParentID = isStringValidID(parent)
    if not isParentID:
        #the parent param was not an ID, lets try to find it in the wwise project
        results = searchForObject(parent,[],"path")
        numOfResults = len(results)
        if numOfResults == 1:
            nextParent = results[0]["id"]
        elif numOfResults == 0:
            print("Could not locate parent in wwise project. Arg given = "+parent)
            return False
        elif numOfResults > 1:
            print("Ambiguous parent argument. More than one possible parent found using arg: "+parent)
            print("Consider refining the argument or passing an explicit ID instead")
            return False
    else:
        result = searchForObject(parent,[],"id")
        if result:
            nextParent = parent
        else:
            print("Error. Cannot find an object with matching ID from parent argument")
            return False


    lastChild = None
    pathlist = path.split("\\")
    for node in pathlist:
        if node == "":
            continue #skip empty nodes

        #get the name and type from the node
        type = ""
        name = ""
        if "<" in node:
            type = node.split(">")[0]
            type = type.replace("<", "")
            name = node.split(">")[1]
        else:
            type = None
            name = node

        # check if there is already a child with the name under the parent
        res = getDescendantObjects(nextParent,[],"id","children")
        for item in res:
            if item["name"] == name:
                #node already exists in wwise
                nextParent = item["id"]
                lastChild = item
                break
        else:
            if type:    #node contains a type, and we didn't find an existing item so we try to create it
                res = createWwiseObject(nextParent,type,name)
                if res:
                    nextParent = res["id"]
                    lastChild = res
                else:   #object was not created
                    print("Error! Could not create object and found no existing object named "+name+" underneath " + parent)
                    return False
            else:
                print("Error! Could not create object and found no existing object named "+name+" underneath " + parent)
                return False

    if lastChild:
        return lastChild
    else:
        return False




############## End of Function definitions ##############################################

#If pywaapi is run as the main script, connect and print result
if __name__ == "__main__":
    result = connect()
    pprint(result)
    exit()

