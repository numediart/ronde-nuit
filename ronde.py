'''Simple GUI for La Ronde de Nuit project.
'''
import json
import time
import tkinter as tk
from tkinter import filedialog, ttk


class Ronde:
    def __init__(self, parent):
        self.time = 2000    # Time to wait between the reading of 2 messages.
        self.data = []      # Data extracted from a JSON file
        self.root = parent  #

        # Frame containing the text and a selection button (for the messages and their labels)
        self.frame = tk.Frame(master=self.root, background="black")

        # To show the messages
        self.label = tk.Label(master=self.frame,
                              text="Welcome to La Ronde de Nuit.\nPlease select a JSON file below:",
                              font=("Arial", 30), background="black", foreground='white')

        # To select a file
        self.button = ttk.Button(
            master=self.frame, text="Select File", command=self.openfile)

        self.label.pack(fill=tk.BOTH, expand=True)
        self.button.pack(side=tk.BOTTOM, expand=True)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.data:
            elem = self.data.pop(0)

            # Display the new message
            self.label.configure(text=elem['message'])

            # Update bbackground color
            #   POSITIVE = green
            #   NEUTRAL = yellow
            #   NEGATIVE = red
            if elem['camembert']['label'] == 'POSITIVE':
                self.frame.configure(background='green')
                self.label.configure(background='green')
            elif elem['camembert']['label'] == 'NEUTRAL':
                self.frame.configure(background='orange')
                self.label.configure(background='orange')
            elif elem['camembert']['label'] == 'NEGATIVE':
                self.frame.configure(background='red')
                self.label.configure(background='red')

            # Call update again after elapsed time
            self.root.after(self.time, self.update)

    def openfile(self):
        '''Opens a file and store data. Calls update afterward.

        File should be a JSON file.
        '''
        filename = filedialog.askopenfilename()
        with open(filename) as f:
            self.data = json.load(f)

        self.root.after(self.time, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    timer = Ronde(root)
    root.mainloop()
