'''Simple GUI for La Ronde de Nuit project.
'''
import argparse
import json
import time
import tkinter as tk
from tkinter import Misc, filedialog, ttk
from typing import Any, Dict, List

import yaml

from src.analysis import SentimentAnalyzer
from src.manager import MsgManager, OnlineMsgManager
from transformers import logging


class RondeColorFromFile:
    def __init__(self,
                 parent: Misc,
                 config: Dict[str, Any]):
        # Time to wait between actions
        self.times = config['time']

        # Data extracted from a JSON file
        self.data: List[Any] = []
        self.display: List[Any] = []

        # parent containing GUI
        self.root = parent

        # colors to show
        self.manager = MsgManager(SentimentAnalyzer(
            config['models']['version']), config['colors'], transition=config['time']['transition'])

        self.create_window()

    def create_window(self):
        # Frame containing the text and a selection button (for the messages and their labels)
        self.frame = tk.Frame(master=self.root, background="black")

        # To show the messages
        self.label = tk.Label(master=self.frame,
                              text="Welcome to La Ronde de Nuit.\nPlease select a JSON file below:",
                              font=("Arial", 30), background="black", foreground='white',
                              wraplength=600,
                              justify='center')

        # To select a file
        self.button = ttk.Button(
            master=self.frame, text="Select File", command=self.openfile)

        self.label.pack(fill=tk.BOTH, expand=True)
        self.button.pack(side=tk.BOTTOM, expand=True)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_data():
            msg, fg, bg, time, _ = self.manager.next_data()

            # Update color
            self.label.configure(text='')
            self.update_color(fg, bg)
            self.root.after(time, self.update)

    def update_color(self, fg, bg):
        """
        """
        self.frame.configure(background=bg)
        self.label.configure(background=bg)
        self.label.configure(foreground=fg)

    def openfile(self):
        '''Opens a file and store data. Calls update afterward.

        File should be a JSON file.
        '''
        filename = filedialog.askopenfilename()
        with open(filename) as f:
            self.manager.set_data(json.load(f))

        self.button.pack_forget()
        self.root.after(100, self.update)


class RondeColor:
    def __init__(self,
                 parent: Misc,
                 config: Dict[str, Any],
                 url: str = 'https://nightwatch.couzinetjacques.com/ReqMsg_01.php'):
        # Time to wait between actions
        self.times = config['time']

        # Data extracted from a JSON file
        self.data: List[Any] = []
        self.display: List[Any] = []

        # parent containing GUI
        self.root = parent

        # colors to show
        self.manager = OnlineMsgManager(SentimentAnalyzer(
            config['models']['version']), config['colors'], transition=config['time']['transition'])

        self.url = url
        self.create_window()

    def create_window(self):
        # Frame containing the text and a selection button (for the messages and their labels)
        self.frame = tk.Frame(master=self.root, background="black")

        # To show the messages
        self.label = tk.Label(master=self.frame,
                              text="Welcome to La Ronde de Nuit.\n",
                              font=("Arial", 30), background="black", foreground='white',
                              wraplength=600,
                              justify='center')

        # To select server url
        # 'https://nightwatch.couzinetjacques.com/ReqMsg_01.php'
        self.button = ttk.Button(
            master=self.frame, text="Run", command=self.openfile)

        self.label.pack(fill=tk.BOTH, expand=True)
        self.button.pack(side=tk.BOTTOM, expand=True)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_data():
            msg, fg, bg, time, _ = self.manager.next_data()

            # Update color
            self.label.configure(text='')
            self.update_color(fg, bg)
            self.root.after(time, self.update)
        else:
            self.manager.parse_data(self.url)

    def update_color(self, fg, bg):
        """
        """
        self.frame.configure(background=bg)
        self.label.configure(background=bg)
        self.label.configure(foreground=fg)

    def openfile(self):
        '''Opens a file and store data. Calls update afterward.

        File should be a JSON file.
        '''
        self.manager.parse_data(self.url)

        self.button.pack_forget()
        self.root.after(100, self.update)


class RondeText():

    def __init__(self,
                 config: Dict[str, Any],
                 url: str):
        # Time to wait between actions
        self.times = config['time']

        # Data extracted from a JSON file
        self.data: List[Any] = []

        # colors to show
        self.manager = OnlineMsgManager(SentimentAnalyzer(
            config['models']['version']), config['colors'], steps=0, transition=config['time']['transition'])

        self.url = url

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_data():
            msg, _, _, t, _ = self.manager.next_data()
            print(msg)
            time.sleep(t/1000)
        else:
            self.manager.parse_data(self.url)

    def loop(self):
        while(1):
            self.update()


class Verbose():
    def __init__(self,
                 config: Dict[str, Any],
                 url: str):
        # Time to wait between actions
        self.times = config['time']

        # Data extracted from a JSON file
        self.data: List[Any] = []

        # colors to show
        self.manager = MsgManager(SentimentAnalyzer(
            config['models']['version']), config['colors'], steps=0, transition=config['time']['transition'])

        self.url = url

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_data():
            msg, _, _, t, label = self.manager.next_data()
            print(f"#### Sequence : {msg} ---- Label : {label} ####")
            time.sleep(t/1000)

        else:
            self.manager.parse_data(self.url)

    def loop(self):
        while(1):
            self.update()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs La Ronde de Nuit demo.')
    parser.add_argument('-c', '--config', type=str, default='config/default.yaml',
                        help='Configuration file for the demonstration.')
    parser.add_argument('-v', '--version', type=int, default=0,
                        help='Version of visualisation.')
    parser.add_argument('-f', '--file', type=str, default='',
                        help='file to read data from.')
    opt = parser.parse_args()

    return opt


if __name__ == "__main__":
    opt = parse_args()
    with open(opt.config, 'r') as f:
        config = yaml.load(f, yaml.FullLoader)

    if opt.version == 0:
        root = tk.Tk()
        if opt.file == '':
            RondeColor(root, config)
        else:
            RondeColor(root, config, opt.file)
        root.mainloop()

    if opt.version == 1:
        logging.set_verbosity_error()

        timer = RondeText(config, opt.file)
        timer.loop()

    if opt.version == 2:
        logging.set_verbosity_debug()

        verb = Verbose(config, opt.file)
        verb.loop()
