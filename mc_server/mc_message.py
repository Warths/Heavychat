import re
from conf import PREFIX, COMMAND

class McMessage:
    def __init__(self, byte):
        self.logline = byte.decode()
        self.type = 'USER_MSG' if "<" in self.logline[33] else 'SRV_MSG'
        if self.type == 'USER_MSG':
            self.player = self.get_player(self.logline)
            self.content = self.get_content(self.logline)
        if self.type == 'USER_MSG' and self.content[0] == PREFIX:
            if self.content.split(" ")[0] == PREFIX + COMMAND:
                self.type = 'COMMAND'
                self.content = self.content[len(PREFIX + COMMAND + ' '):]
                self.arg = self.content.split(' ')
            else:
                self.type = 'TO_TWITCH'
                self.content = self.content[len(PREFIX):]


    @staticmethod
    def get_player(logline):
        player = logline.split("<")[1].split(">")[0]
        player = re.sub('[§]+[0-9a-fk-or]?', '', player)
        return player

    @staticmethod
    def get_content(logline):
        content = logline.split("> ")[1].split("\n")[0]
        return content