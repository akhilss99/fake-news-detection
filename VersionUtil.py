from datetime import datetime

class Time:
    timePattern : str = "%d%m%Y%H%M"
    @classmethod
    def getKey(self):
        versionKey = datetime.now()
        return versionKey.strftime(self.timePattern)