# PPPPPPPPPPPPPPPPP   NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
# P::::::::::::::::P  N:::::::N       N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# P::::::PPPPPP:::::P N::::::::N      N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# PP:::::P     P:::::PN:::::::::N     N::::::NEE::::::EEEEEEEEE::::EEE::::::EEEEEEEEE::::E
#   P::::P     P:::::PN::::::::::N    N::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
#   P::::P     P:::::PN:::::::::::N   N::::::N  E:::::E               E:::::E
#   P::::PPPPPP:::::P N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE
#   P:::::::::::::PP  N::::::N N::::N N::::::N  E:::::::::::::::E     E:::::::::::::::E
#   P::::PPPPPPPPP    N::::::N  N::::N:::::::N  E:::::::::::::::E     E:::::::::::::::E
#   P::::P            N::::::N   N:::::::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE
#   P::::P            N::::::N    N::::::::::N  E:::::E               E:::::E
#   P::::P            N::::::N     N:::::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
# PP::::::PP          N::::::N      N::::::::NEE::::::EEEEEEEE:::::EEE::::::EEEEEEEE:::::E
# P::::::::P          N::::::N       N:::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# P::::::::P          N::::::N        N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# PPPPPPPPPP          NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#
# Python Noodle Extensions Editor. (Great name, I know.) I can't do ASCII, so I used http://patorjk.com/software/taag/#p=testall&h=0&v=0&f=Alpha&t=PNEE "Doh" (Pronounced the same as Knee, /nē/)
# This code is awful. Please improve it.

import json, copy
from pathlib import Path
from enum import Enum
from .events import *
from .objects import *

version = "2.0.3"

PATHSWINDOWS = { # A list of internal Beat Saber download paths.
    "Steam":r"C:\Program Files (x86)\Steam\steamapps\common\Beat Saber",
    "Oculus":r"C:\OculusApps\Software\hyperbolic-magnematism-beat-saber"
}
PATHSLINUX = {
    "Steam":r"~/.steam/steam/SteamApps/common/Beat Saber",
    "Oculus":r"unknown" # I need someone to add an oculus download path (if exists) for Linux
}
EASINGSNET = "https://easings.net"
ANIMATORFORMATS = {
     "_position":       '[left/right, up/down, forw/backw, time (beat), "easing"]',
     "_rotation":       '[pitch, yaw, roll, time (beat), "easing"]',
"_localRotation":       '[pitch, yaw, roll, time (beat), "easing"]',
        "_scale":       '[left/right, up/down, forw/backw, time (beat), "easing"]',
     "_dissolve":       '[amount, time (beat), "easing"]',
"_dissolveArrow":       '[amount, time (beat), "easing"]',
         "_time":       '[lifespan, time (beat), "easing"]',
        "_color":       '[red, green, blue, time, easing]'
}
EASINGS = [
    "easeInsine",
    "easeOutSine",
    "easeInOutSine",
    "easeInCubic",
    "easeOutCubic",
    "easeInOutCubic",
    "easeInQuint",
    "easeOutQuint",
    "easeInOutQuint",
    "easeInCirc",
    "easeOutCirc",
    "easeInOutCirc",
    "easeInElastic",
    "easeOutElastic",
    "easeInOutElastic",
    "easeInQuad",
    "easeOutQuad",
    "easeInOutQuad",
    "easeInQuart",
    "easeOutQuart",
    "easeInOutQuart",
    "easeInExpo",
    "easeOutExpo",
    "easeInOutExpo",
    "easeInBack",
    "easeOutBack",
    "easeInOutBack",
    "easeInBounce",
    "easeOutBounce",
    "easeInOutBounce"
]


class NoodleExtensions:

    def updateDependencies(self, dependency:str) -> list:
        '''Update Dependencies adds a `_requirements` item. Do note it doesn't check if you have it installed nor does it check whether or not that dependency is real.\n
        However, it does check whether or not it's already in the list.\n
        Returns the list of dependencies.\n

        ### PARAMETERS\n
        `dependency` - the string item you want to add to the `_requirements`

        ### RETURNS
        The requirements list.
        '''
        infodatpath = self.levelPath
        infodatpath = infodatpath.split("\\")
        infodatpath.remove(infodatpath[len(infodatpath)-1])
        infodatpath.append("info.dat")
        infodatpath = "\\".join(infodatpath)

        infodat = json.load(open(infodatpath))
        with open(infodatpath, 'w') as editinfodat:
            for x in range(len(infodat["_difficultyBeatmapSets"])):
                # warning: the next few lines are ugly.
                for _difficultyBeatmaps in infodat["_difficultyBeatmapSets"][x]["_difficultyBeatmaps"]:
                    if _difficultyBeatmaps["_beatmapFilename"] == self.levelPath.split("\\")[len(self.levelPath.split("\\"))-1]: # if the difficulty is the same file as the one the user is using
                        if _difficultyBeatmaps["_customData"].get("_requirements") is None:
                            _difficultyBeatmaps["_customData"]["_requirements"] = []
                        if not dependency in _difficultyBeatmaps["_customData"]["_requirements"]:
                            _difficultyBeatmaps["_customData"]["_requirements"].append(dependency)
                        json.dump(infodat, editinfodat)
                        return _difficultyBeatmaps["_customData"]["_requirements"]
    
    def __init__(self, levelDatPath:str):
        '''The base editor for making noodle extensiosn levels.\n
        ### PARAMETERS\n
        `levelDatPath` - The level.dat path.
        
        ### FUNCTIONS\n
        `pushChanges` - Will push all your changes.\n
        `createNote` - Will create a new note.\n
        `createWall` - Will create a new wall.\n
        `getNote` - Will return a list of all notes who have matching data.'''


        self.levelPath = levelDatPath
        self.levelData = json.load(open(levelDatPath))
        self.updateDependencies('Noodle Extensions')
        if self.levelData["_customData"].get("_customEvents") is None:
            self.levelData["_customData"]["_customEvents"] = []
    
    def pushChanges(self):
        '''Will push the changes to the choosen level.dat.'''
        json.dump(self.levelData, open(self.levelPath, 'w'))

        # add "last edited by" as PNEE
        infodatpath = self.levelPath
        infodatpath = infodatpath.split("\\")
        infodatpath.remove(infodatpath[len(infodatpath)-1])
        infodatpath.append("info.dat")
        infodatpath = "\\".join(infodatpath)

        infodat = json.load(open(infodatpath))
        if infodat["_customData"].get("_editors") is None:
            infodat["_customData"]["_editors"] = {}
        infodat["_customData"]["_editors"]["PNEE"] = {
            "version":version
        }
        infodat["_customData"]["_editors"]["_lastEditedBy"] = "PNEE"
        json.dump(infodat, open(infodatpath, 'w'))

    def getNote(self, note:Note, excludeCustomData:bool=False):
        '''Will return a list of Note objects with matching data.
        
        ### PARAMETERS
        `note` a Note object.\n
        `excludeCustomData` Whether or not it should check if the custom data of the notes match.

        ### RETURNS
        A list of Note objects with matching data.'''

        noteData = Note.fromDict(note.note).note # create a new copy of the note object to avoid changing the data of the `note` fed into the function.

        if excludeCustomData and noteData.get("_customData") is not None:
            noteData.pop("_customData")
        notes = []
        for x in copy.deepcopy(self.levelData["_notes"]):
            if excludeCustomData and x.get("_customData") is not None:
                compareVal = copy.deepcopy(x)
                compareVal.pop("_customData")
            else:
                compareVal = copy.deepcopy(x)
            if compareVal == noteData:
                notes.append(
                    Note.fromDict(x)
                )
        
        return notes
    
    def getWall(self, wall:Obstacle, excludeCustomData:bool=False):
        '''Will return a list of Obstacles objects with matching data.
        
        ### PARAMETERS
        `wall` An obstacle object.\n
        `excludeCustomData` Whether or not it should check if the custom data of the notes match.
        
        ### RETURNS
        A list of Obstacle objects with matching data.'''

        wallData = Obstacle.fromDict(wall.obstacle).obstacle # create a new copy of the wall to avoid changing the data of the `wall` fed into the function.

        if excludeCustomData and wallData.get("_customData") is not None:
            wallData.pop("_customData")

        walls = []
        for x in copy.deepcopy(self.levelData["_obstacles"]):
            if excludeCustomData and x.get("_customData") is not None:
                compareVal = copy.deepcopy(x)
                compareVal.pop("_customData")
            else:
                compareVal = copy.deepcopy(x)
            if compareVal == wallData:
                walls.append(
                    Obstacle.fromDict(x)
                )
            
        return walls
    
    def editNote(self, oldNote:Note, newNote:Note, checkForCustomData:bool=False):
        '''Will edit the first note found.\n
        It is recommended to only change the note's customData property. Changing anything else will give weird results.
        
        ### PARAMETERS
        `oldNote` - The note that you want to edit\n
        `newNote` - The data that will replace it\n
        `checkForCustomData` - Whether or not the custom data of the `oldNote` needs to match the first note found.
        
        ### RETURNS
        The newNote dict data, or None if no note could be found.'''
        
        possibleNotes = self.getNote(oldNote, excludeCustomData=not checkForCustomData)
        if len(possibleNotes) == 0:
            return
        
        ind = self.levelData["_notes"].index(possibleNotes[0].note)
        self.levelData["_notes"][ind] = newNote.note
        return newNote.note

    def editWall(self, oldWall:Obstacle, newWall:Obstacle, checkForCustomData:bool=False):
        '''Will edit the first wall found.\n
        It is recommended to only change the wall's customData property. Changing anything else will give weird results.
        
        ### PARAMETERS
        `oldWall` - The wall that you want to edit
        `newWall` - The data that will replace it
        `checkForCustomData` - Whether or not the custom data of the `oldWall` needs to match the first wall found.

        ### RETURNS
        The newWall dict data, or None if no wall could be found'''

        possibleWalls = self.getWall(oldWall, excludeCustomData=not checkForCustomData)
        
        if len(possibleWalls) == 0:
            return
        
        ind = self.levelData["_obstacles"].index(possibleWalls[0].obstacle)
        self.levelData["_obstacles"][ind] = newWall.obstacle
        return newWall.obstacle
    def animateTrack(self, data:AnimateTrack):
        '''Creates a new AnimateTrack event. (Event will be overwritten if track is already being animated.)
        
        ### PARAMETERS
        `data` - An AnimateTrack object.
        
        ### RETURNS
        The event dict data.'''

        events = self.levelData["_customData"]["_customEvents"]
        for x in range(len(events)):
            if events[x]["_type"] == "AnimateTrack":
                if events[x]["_data"]["_track"] == data._track:
                    events[x] = data.event
                    return data.event
        
        events.append(data.event)
        return data.event

    
    def assignPathAnimation(self, data:AssignPathAnimation):
        '''Create a new AssignPathAnimation event. (Event will be overwritten if path is already being animated.)
        
        ### PARAMETERS
        `data` - an AssignPathAnimation object.
        
        ### RETURNS
        The event dict data.'''

        events = self.levelData["_customData"]["_customEvents"]
        for x in range(len(events)):
            if events[x]["_type"] == "AssignPathAnimation":
                if events[x]["_data"]["_track"] == data._track:
                    events[x] = data.event
                    return data.event
        
        events.append(data.event)
        return data.event
    
    def assignTrackParent(self, data:AssignTrackParent):
        '''Create a new AssignTrackParent event. (Children tracks will be overwritten if event already exists.)
        
        ### PARAMETERS
        `data` - an AssignTrackParent object.
        
        ### RETURNS
        The event's dict data.'''

        events = self.levelData["_customData"]["_customEvents"]
        for x in range(len(events)):
            if events[x]["_type"] == "AssignTrackParent":
                if events[x]["_time"] == data._time and events[x]["_data"]["_parentTrack"] == data._parentTrack:
                    events[x]["_data"]["_childrenTracks"] = data._childrenTracks
                    return data.event
        
        events.append(data.event)
        return data.event

    def assignPlayerToTrack(self, data:AssignPlayerToTrack):
        '''Create a new AssignPlayerToTrack event. (Track will be overwritten if event already exists.)
        
        ### PARAMETERS
        `data` - an AssignPlayerToTrack object.
        
        ### RETURNS
        The event's dict data.'''

        events = self.levelData["_customData"]["_customEvents"]
        for x in range(len(events)):
            if events[x]["_type"] == "AssignPlayerToTrack":
                if events[x]["_time"] == data._time:
                    events[x]["_data"]["_track"] = data._track
                    return data.event
        
        events.append(data.event)
        return data.event