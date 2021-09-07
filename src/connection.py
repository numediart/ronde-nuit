"""A bot to read a channel on a server and log every information.

Based on :
    https://github.com/jaraco/irc/blob/main/scripts/testbot.py
"""
import json
import os
from typing import List

import irc.bot
import irc.strings
import requests


class IrcBot(irc.bot.SingleServerIRCBot):
    '''Bot to get messages from IRC channels.
    '''

    def __init__(self,
                 server: str,
                 channels: List[str],
                 nickname: str,
                 port: int = 6667,
                 jsonfile: str = 'output.json'):
        '''Initialize the bot using irc package.
        '''
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.names = channels
        self.server = server
        self.port = port
        self.jsonfile = jsonfile

        self.index = {key: 0 for key in self.names}

        irc.client.ServerConnection.buffer_class.encoding = "latin-1"

    def on_welcome(self, c, e):
        '''What to do when logging in the server.
        '''
        for channel in self.names:
            c.join(channel)
            print('Logged into {}@{}:{}'.format(channel, self.server, self.port))

    def update_json(self,
                    channel: str,
                    msg: str) -> None:
        '''Add a message to the json file.

        Args
        ----
        msg : str
            message to add
        '''
        data = {
            'message': msg,
            'channel': channel}

        if os.path.exists(self.jsonfile):
            with open(self.jsonfile, 'r') as jsonf:
                jsondata = json.load(jsonf)
                jsondata.append(data)
        else:
            jsondata = [data]

        with open(self.jsonfile, 'w') as jsonf:
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
        # JSON file update
        channel = e.target.lower()
        self.update_json(channel, e.arguments[0])

        # Update terminal text
        self.index[channel] += 1
        print('Messages read in {}: {}'.format(channel, self.index[channel]))


def download_txt_online(url: str,
                        outputname: str = 'output.txt'):
    '''Download a text file online.

    Args
    ----
    url : str
        url to text file
    outputname : str
        path to the text file to write content into
    '''
    r = requests.get(url, allow_redirects=True)
    open(outputname, 'wb').write(r.content)
