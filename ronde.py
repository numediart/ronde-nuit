'''Simple GUI for La Ronde de Nuit project.
'''
import argparse
import os
import time
import tkinter as tk
from tkinter import Misc, filedialog, ttk
from typing import Any, Dict, List, Optional

import yaml
from transformers import logging

from src.manager import AbstractMsgManager, MsgManager, OnlineMsgManager


class AbstractRonde():
    def __init__(self,
                 config: Dict[str, Any],
                 parent: Optional[Misc] = None,
                 url: str = ''):
        # Time to wait between actions
        self.transition = config['display']['transition']
        # Weither text is shown
        self.showText = config['display']['showText']

        # Data extracted from a JSON file
        self.data: List[Any] = []
        self.display: List[Any] = []

        # parent containing GUI
        if parent:
            self.root = parent

        # colors to show
        self.url = url
        if url == '' or os.path.isfile(url):
            self.manager: AbstractMsgManager = MsgManager(config)
        else:
            self.manager = OnlineMsgManager(config)

    def create_window(self):
        pass


class RondeColorFromFile(AbstractRonde):
    def __init__(self,
                 config: Dict[str, Any],
                 parent: Misc,
                 url: str = ''):
        super().__init__(config, parent, url)

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
        self.url = filedialog.askopenfilename()
        self.manager.parse_data(self.url)

        self.button.pack_forget()
        self.root.after(100, self.update)


class RondeColor(AbstractRonde):
    def __init__(self,
                 config: Dict[str, Any],
                 parent: Misc,
                 url: str = ''):
        super().__init__(config, parent, url)

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
            _, fg, bg, _, _ = self.manager.next_data()

            # Update color
            self.label.configure(text='')
            self.update_color(fg, bg)
            self.root.after(self.manager.transition, self.update)
        else:
            self.manager.parse_data(self.url)
            self.root.after(self.manager.transition, self.update)

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


class RondeText(AbstractRonde):
    def __init__(self,
                 config: Dict[str, Any],
                 url: str = ''):
        super().__init__(config, None, url)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_data():
            msg, _, _, _, _ = self.manager.next_data()
            print(msg)
            time.sleep(self.manager.transition/1000)
        else:
            self.manager.parse_data(self.url)

    def mainloop(self):
        while(1):
            self.update()


class Verbose(AbstractRonde):
    def __init__(self,
                 config: Dict[str, Any],
                 url: str = ''):
        super().__init__(config, None, url)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_data():
            msg, _, _, label, score = self.manager.next_data()
            print(
                f"#### Sequence: {msg} ---- Label: {label} ---- Score: {score}####")
            time.sleep(self.manager.transition/1000)

        else:
            self.manager.parse_data(self.url)

    def mainloop(self):
        while(1):
            self.update()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs La Ronde de Nuit demo.')
    parser.add_argument('-c', '--config', type=str,
                        default='config/default.yaml',
                        help='Configuration file for the demonstration.')
    parser.add_argument('-v', '--version', type=int,
                        default=0,
                        help='Version of visualisation.')
    parser.add_argument('-f', '--file', type=str,
                        default='https://nightwatch.couzinetjacques.com/ReqMsg_01.php',
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
            RondeColorFromFile(config, root)
        else:
            RondeColor(config, root, opt.file)

    elif opt.version == 1:
        logging.set_verbosity_error()

        root = RondeText(config, opt.file)

    elif opt.version == 2:
        logging.set_verbosity_debug()

        root = Verbose(config, opt.file)

    root.mainloop()
