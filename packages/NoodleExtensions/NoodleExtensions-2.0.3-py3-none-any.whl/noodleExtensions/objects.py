class Note:
    def __init__(self, beat, index, layer, type, cutDirection, **customData):
        '''a note object which contains info on a note.\n
        `beat` - The beat of the note.\n
        `index` - The lineIndex of the note\n
        `layer` - The lineLayer of the note\n
        `type` - The note type\n
        `cutDirection` - The cut direction of the note\n
        `customData` - The note's custom data\n
        '''
        newNote = {
            "_time":beat,
            "_lineIndex":index,
            "_lineLayer":layer,
            "_type":type,
            "_cutDirection":cutDirection
        }

        if customData != {}:
            newNote["_customData"] = customData
        
        self.note = newNote

        self._time = beat
        self._lineIndex = index
        self._lineLayer = layer
        self._type = type
        self._cutDirection = cutDirection
        self._customData = customData
        
    @classmethod # allows to call method without needing to call __init__
    def fromDict(cls, data:dict):
        '''Will return a Note object from a note dict data.'''
        if data.get("_customData") is None: # fixing index error
            noteObjFromDict = cls(data["_time"], data["_lineIndex"], data["_lineLayer"], data["_type"], data["_cutDirection"])
        else:
            noteObjFromDict = cls(data["_time"], data["_lineIndex"], data["_lineLayer"], data["_type"], data["_cutDirection"], **data["_customData"])

        return noteObjFromDict

class Obstacle:
    def __init__(self, beat, index, type, duration, width, **customData):
        '''a note object which contains info on a note.\n
        `beat` - The start beat of the wall.\n
        `index` - The starting left position of the wall.\n
        `type` - The wall type type\n
        `duration` - How many beats the wall lasts.\n
        `width` - How wide the wall should be\n
        `customData` - The note's custom data\n
        '''
        newWall = {
            "_time":beat,
            "_lineIndex":index,
            "_type":type,
            "_duration":duration,
            "_width":width,
            "_customData":{}
        }

        if customData != {}:
            newWall["_customData"] = customData
        
        self.obstacle = newWall

        self._time = beat
        self._lineIndex = index
        self._type = type
        self._duration = duration
        self._width = width
        self._customData = customData
        
    @classmethod
    def fromDict(cls, data:dict):
        '''Will return a Obstacle object from dict data.'''
        if data.get("_customData") is None:
            noteObjFromDict = cls(data["_time"], data["_lineIndex"], data["_type"], data["_duration"], data["_width"])
        else:
            noteObjFromDict = cls(data["_time"], data["_lineIndex"], data["_type"], data["_duration"], data["_width"], **data["_customData"])

        return noteObjFromDict