import json

class search_result:
    serieId = ""
    serieName = ""
    serieImg = ""

    seasonNumber = ""
    seasonName = ""

    episodeNumber = ""
    episodeName = ""
    episodeHref = ""
    episodeImg = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class soapberry_exception(Exception):
    message = ""
    logs = []

    def __init__(self, exception, logs): 
        Exception.__init__(self, exception)
        self.message = repr(exception)
        self.logs = logs

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class soapberry_log:
    time = ""
    message = ""

    def toString(self):
        return self.time + ": " + self.message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)