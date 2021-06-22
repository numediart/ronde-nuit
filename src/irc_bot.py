"""A bot to read a channel on a server and log every information.

Based on :
    https://github.com/jaraco/irc/blob/main/scripts/testbot.py
"""
import csv
import json
import os
from datetime import datetime
from typing import Optional

import irc.bot
import irc.strings


class IrcBot(irc.bot.SingleServerIRCBot):
    def __init__(self,
                 server: str,
                 channel: str,
                 nickname: str,
                 port: int = 6667,
                 csvfile: Optional[str] = None,
                 jsonfile: Optional[str] = None):
        '''Initialize the bot using irc package.
        '''
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.channel = channel

        self.jsonfile = 'chat.json' if jsonfile is None else jsonfile
        self.csvfile = 'chat.csv' if csvfile is None else csvfile
        self.create_csv()

        self.index = 0

    def create_csv(self) -> None:
        '''Creates the CSV file. Adds a header if file is new.
        '''
        header = None
        if not os.path.exists(self.csvfile):
            header = ['message']

        with open(self.csvfile, 'a', newline='') as csvf:
            csvwriter = csv.writer(csvf, delimiter=',')
            if header:
                csvwriter.writerow(header)

    def on_welcome(self, c, e):
        '''What to do when logging in the server.
        '''
        c.join(self.channel)

    def update_csv(self, msg: str) -> None:
        '''Add a message to the csv file.

        Args
        ----
        msg : str
            message to add
        '''
        with open(self.csvfile, 'a', encoding="utf-8", newline='') as csvf:
            csvwriter = csv.writer(csvf, delimiter=',')
            csvwriter.writerow([msg])

    def update_json(self, msg: str) -> None:
        '''Add a message to the json file.

        Args
        ----
        msg : str
            message to add
        '''
        data = {'message': msg}

        if os.path.exists(self.jsonfile):
            with open(self.jsonfile, 'r') as jsonf:
                jsondata = json.load(jsonf)
                jsondata.append(data)
        else:
            jsondata = [data]

        with open(self.jsonfile, 'w', newline='') as jsonf:
            json.dump(jsondata, jsonf)

    def on_pubmsg(self, c, e):
        '''What to do when a message is published on the server.

        Message format is:
            type: pubmsg
            source: name of sender
            target: channel
            arguments: ['<msg>']
            tags: []
        '''
        # CSV file
        self.update_csv(e.arguments[0])

        # JSON file
        self.update_json(e.arguments[0])

        # Update terminal text
        self.index += 1
        print('Messages read : {}'.format(self.index), end='\r')
