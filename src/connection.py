"""Functions related to data online download.
"""
import json
import os
from typing import List, Dict

import irc.bot
import irc.strings
import requests


class IrcBot(irc.bot.SingleServerIRCBot):
    '''Bot to get messages from IRC channels.

    Based on :
        https://github.com/jaraco/irc/blob/main/scripts/testbot.py

    Attributes
    ----------
    server : str
        name of the server
    channels : list of str
        list of channel names to connect to
    nickname : str
        bot name on the server
    port : int
        port to connect to
    jsonfile : str
        path to the json file containing channel messages
    key : dict
        number of messages read per channel
    '''

    def __init__(self,
                 server: str,
                 channels: List[str],
                 nickname: str,
                 port: int = 6667,
                 jsonfile: str = 'output.json') -> None:
        '''Initialize the bot using irc package.

        Args
        ----
        server : str
            name of the server
        channels : list of str
            list of channel names to connect to
        nickname : str
            bot name on the server
        port : int, optional
            port to connect to.
            Default is 6667.
        jsonfile : str, optional
            path to the json file containing channel messages.
            Default is 'output.json'.
        '''
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.names = channels
        self.server = server
        self.port = port
        self.jsonfile = jsonfile

        self.index = {key: 0 for key in self.names}

        irc.client.ServerConnection.buffer_class.encoding = "latin-1"

    def on_welcome(self,
                   c,
                   e):
        '''Join all channels when logging into the server.
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
        channel : str
            channel in which the message has been read
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

    def on_pubmsg(self,
                  c,
                  e):
        '''Store a message when published on the server.

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


class OnlineTxtParser():
    '''Class to extract and parse a txt file online.

    Attributes
    ----------
    url : str
        url to the txt file
    file : str
        temporary file to write txt file into
    json : str
        final JSON output file
    '''

    def __init__(self,
                 url: str,
                 jsonfile: str = 'output.json') -> None:
        '''Initialize the parser with url and json file.

        Args
        ----
        url : str
            url to the txt file

        json : str, optional
            final JSON output file.
            Default is 'output.json'
        '''
        self.url = url
        self.file = 'tmp.txt'
        self.json = jsonfile

    def download_txt_online(self) -> None:
        '''Download a text file online.
        '''
        r = requests.get(self.url, allow_redirects=True)
        open(self.file, 'wb').write(r.content)

    def read_txt_file(self,
                      length: int = -1) -> List[Dict[str, str]]:
        '''Parse txt file.

        Args
        ----
        length : optional, int
            number of messages to extract. If -1, extract all messages.
            Default is -1.

        Returns
        -------
        list of dictionary
            list of messages structured as dictionary.
        '''
        result = []
        msgs = []
        with open(self.file, 'r', encoding='utf8') as f:
            line = f.readline()

            while line and length:
                if line and line not in msgs:
                    result.append({'message': line})
                    msgs.append(line)
                    length -= 1

                line = f.readline()

        return result

    def convert_txt_file(self,
                         length: int = -1) -> None:
        '''Convert txt file to JSON file.

        Each line of the txt line is a new sentence.

        Args
        ----
        length : optional, int
            number of messages to extract. If -1, extract all messages.
            Default is -1.
        '''
        data = self.read_txt_file(length)

        with open(self.json, 'w') as f:
            json.dump(data, f, indent=4)

    def get_online_file(self) -> None:
        '''Download file at url and converts it to JSON file.
        '''
        self.download_txt_online()
        self.convert_txt_file()
