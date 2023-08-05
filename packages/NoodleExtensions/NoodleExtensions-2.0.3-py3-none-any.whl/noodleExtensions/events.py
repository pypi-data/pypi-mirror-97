class AnimateTrack:
    def __init__(self, beat, track, duration, **properties):
        '''An animate track object which contains info on an animateTrack event.\n
        `beat` - The beat at which the event should start.\n
        `track` - the track that should be animated\n
        `duration` - the duration of the event\n
        `data` - The animation data.\n

        __str__() returns affected track name'''

        newEvent = {
            "_time":beat,
            "_type":"AnimateTrack",
            "_data":{
                "_track":track,
                "_duration":duration
            }
        }
        for prop in properties.keys():
            newEvent["_data"][prop] = properties[prop]
        
        self.event = newEvent

        self._time = beat
        self._track = track
        self._duration = duration
        self._properties = properties

    def __str__(self):
        return self._track
    
    @classmethod
    def fromDict(cls, data:dict):
        '''Construcs a new AnimateTrack object from a dictionary.'''
        return super().__init__(data["_time"], data["_data"]["_track"], data["_data"]["_duration"], **data["_data"])

class AssignPathAnimation:
    def __init__(self, beat, track, duration, **properties):
        '''an Assign Path Animation object which contains info on an assignPathAnimation event.\n
        `beat` - The beat at which the event should start.
        `track` - The track that should be animated.\n
        `duration` - The duration of the event.\n
        `data` - The animation data.\n

        __str__() returns affected track name'''

        newEvent = {
            "_time":beat,
            "_type":"AssignPathAnimation",
            "_data":{
                "_track":track,
                "_duration":duration
            }
        }
        for prop in properties.keys():
            newEvent["_data"][prop] = properties[prop]
        
        self.event = newEvent
        
        self._time = beat
        self._track = track
        self._duration = duration
        self._properties = properties

    def __str__(self):
        return self._track

    @classmethod
    def fromDict(cls, data:dict):
        '''Construcs a new AssignPathAnimation object from a dictionary.'''
        return super().__init__(data["_time"], data["_data"]["_track"], data["_data"]["_duration"], **data["_data"])

class AssignTrackParent:
    def __init__(self, beat, tracks, parentTrack):
        '''an Assign Track Parent object which contains info on an assignTrackParent event.\n
        `beat` -  The beat at which the event should start.\n
        `tracks` - A list of tracks to parent.
        `parentTrack` - The parent track.
        
        __str__() returns the parentTrack.
        __list__() returns the children tracks.'''

        newEvent = {
            "_time":beat,
            "_type":"AssignTrackParent",
            "_data":{
                "_childrenTracks":tracks,
                "_parentTrack":parentTrack
            }
        }
        self.event = newEvent

        self._time = beat
        self._childrenTracks = tracks
        self._parentTrack = parentTrack

    def __str__(self):
        return self._parentTrack

    def __list__(self):
        return self._childrenTracks

    @classmethod
    def fromDict(cls, data:dict):
        '''Construcs a new AssignTrackParent object from a dictionary.'''
        return super().__init__(data["_time"], data["_data"]["_childrenTracks"], data["_data"]["_parentTrack"])

class AssignPlayerToTrack:
    def __init__(self, beat, track):
        '''an Assign Player To Track object which contains info on an assignPlayerToTrack event.\n
        `beat` - The beat at which the event should happen.\n
        `track` - The track that will be assigned to the player.
        
        __str__() returns the track that the player is parented to.'''

        newEvent = {
            "_time": beat,
            "_type": "AssignPlayerToTrack",
            "_data": {
                "_track": track
            }
        }

        self.event = newEvent

        self._time = beat
        self._track = track
    def __str__(self):
        return self._track
    
    @classmethod
    def fromDict(cls, data:dict):
        '''Construcs a new AssignPlayerToTrack object from a dictionary.'''
        return super().__init__(data["_time"], data["_data"]["_track"])