'''Class to handle GUI and general display for Ronde project.
'''
import os
import time
import tkinter as tk
from tkinter import Misc, filedialog, ttk
from typing import Any, Dict, List, Optional

import yaml
from transformers import logging

from .manager import AbstractMsgManager, JsonMsgManager, OnlineMsgManager


class RondeGUI():
    def __init__(self,
                 config: Dict[str, Any],
                 parent: Optional[Misc] = None,
                 url: str = ''):
        # Time to wait between actions
        self.config = config

        # Data extracted from a JSON file
        self.data: List[Any] = []
        self.display: List[Any] = []

        # parent containing GUI
        self.root = parent

        # colors to show
        self.url = url
        if self.url == '' or os.path.isfile(self.url):
            self.manager: AbstractMsgManager = JsonMsgManager(config)
        else:
            self.manager = OnlineMsgManager(config)

        if self.root:
            self.create_window()

    def create_window(self):
        # Frame containing the text and a selection button (for the messages and their labels)
        self.frame = tk.Frame(master=self.root, background="black")

        # To show the messages
        labelTxt = "Welcome to 'La Ronde de Nuit'."
        buttonTxt = "Run"
        if self.url == '':
            labelTxt += "\nPlease select a JSON file below:"
            buttonTxt = "Select File"

        self.label = tk.Label(master=self.frame,
                              text=labelTxt,
                              font=("Arial", 30), background="black", foreground='white',
                              wraplength=600,
                              justify='center')

        # To select a file
        self.button = ttk.Button(
            master=self.frame, text=buttonTxt, command=self.openfile)

        self.label.pack(fill=tk.BOTH, expand=True)
        self.button.pack(side=tk.BOTTOM, expand=True)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def openfile(self):
        '''Opens a file and store data. Calls update afterward.

        File should be a JSON file.
        '''
        if self.url == '':
            self.url = filedialog.askopenfilename()

        self.manager.parse_data(self.url)

        self.button.pack_forget()
        self.root.after(100, self.update)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_messages():
            msg, fg, bg, label, score = self.manager.next_data()

            # Update color
            self.update_text(msg, label, score)

            if self.config['display']['colors']:
                self.update_color(fg, bg)
        else:
            self.manager.parse_data(self.url)
        self.wait()

    def update_text(self, msg, label, score):
        """Update the text.

        Args
        ----
        msg : str
            message to write
        label : str
            label of the corresponding message
        score : float
            related score
        """
        if self.root:
            if self.config['display']['text']:
                self.label.configure(text=msg)
            else:
                self.label.configure(text='')

        if self.config['print']['text']:
            if self.config['print']['mode'] == 'demo':
                print(msg)
            elif self.config['print']['mode'] == 'debug':
                print(
                    f"#### Sequence: {msg} ---- Label: {label} ---- Score: {score}####")

    def update_color(self, fg, bg):
        """
        """
        self.frame.configure(background=bg)
        self.label.configure(background=bg)
        self.label.configure(foreground=fg)

    def wait(self):
        """Make the process wait.
        """
        if self.root:
            self.root.after(self.config['manager']['transition'], self.update)
        else:
            time.sleep(self.config['manager']['transition']/1000)

    def mainloop(self):
        if self.root:
            self.root.mainloop()
        else:
            while(1):
                self.update()


def set_verbosity(config: Dict):
    '''Set machine learning models verbosity.

    Args
    ----
    config : dict
        dictionary of configuration. Should be organized as
          - 'text' which defines if text is visible in command line
          - 'mode' which defines the level of verbosity. Can either be
            'demo' (low level of verbosity) or 'debug' (highest level)
    '''
    if config['text']:
        if config['mode'] == 'demo':
            logging.set_verbosity_error()
        elif config['mode'] == 'debug':
            logging.set_verbosity_debug()
        else:
            logging.set_verbosity_info()
    else:
        logging.set_verbosity_error()


def create_ronde_gui(configpath: str,
                     url: str) -> RondeGUI:
    '''Creates the GUI for 'La Ronde de nuit' project.

    Args
    ----
    configpath : str
        path to the configuration file
    filepath : str
        path to the file to run on or url to the website

    Returns
    -------
    RondeGUI
        the GUI to display messages and their analysis
    '''
    with open(configpath, 'r') as f:
        config = yaml.load(f, yaml.FullLoader)

    # Adapt verbosity
    set_verbosity(config['print'])

    # Define GUI or not
    root = None
    if config['display']['colors'] or config['display']['text']:
        root = tk.Tk()

    # Create the process
    ronde = RondeGUI(config, root, url)

    return ronde