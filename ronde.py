'''Simple GUI for La Ronde de Nuit project.
'''
import argparse
import json
import tkinter as tk
from tkinter import Misc, filedialog, ttk
from typing import Any, Dict, List

import ftfy
import yaml

from src.analysis import SentimentAnalyzer
from src.manager import MsgManager


class Ronde:
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
            config['models']['version']), config['colors'])

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
            msg, fg, bg, time = self.manager.next_data()

            # Update color
            self.label.configure(text=msg)
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

        self.root.after(100, self.update)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Runs La Ronde de Nuit demo.')
    parser.add_argument('-c', '--config', type=str, default='config/default.yaml',
                        help='Configuration file for the demonstration.')
    opt = parser.parse_args()

    return opt


if __name__ == "__main__":
    opt = parse_args()
    with open(opt.config, 'r') as f:
        config = yaml.load(f, yaml.FullLoader)

    root = tk.Tk()
    timer = Ronde(root, config)
    root.mainloop()
