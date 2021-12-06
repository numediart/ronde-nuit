'''Class to handle GUI and general display for Ronde project.
'''
import os
import time
import tkinter as tk
from tkinter import Misc, filedialog, ttk
from typing import Any, Dict, List, Optional

from pythonosc import udp_client
import mido

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

        self.osc_clients, self.midi_outports = [], []
        for ip, port in zip( config[ 'osc' ][ 'ip' ], config[ 'osc' ][ 'port' ] ) : 
            self.osc_clients.append( udp_client.SimpleUDPClient( ip, port ) ) 
            
        for port in range( config[ 'midi' ][ 'nb_port' ] ) :
            try :
                out = mido.open_output( )
                self.midi_outports.append( out )
            except OSError :
                print( 'No output port availble - Receiving apps should be launched first so that output_port() can connect to the created MIDI ports.') 

        

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

        if( self.config[ 'manager' ][ 'last_messages' ] > -1 ) :
            self.manager.set_start( self.config[ 'manager' ][ 'last_messages' ] )

        self.button.pack_forget()
        self.root.after(100, self.update)

    def update(self):
        '''Update the text with the next message and the background with color corresponding to message sentiment.
        '''
        if self.manager.has_messages():
            msg, fg, bg, label, score = self.manager.next_data()

            self.sendOut( label, score )
            # Update color
            self.update_text(msg, label, score)

            if self.config['display']['colors']:
                self.update_color(fg, bg)
        else:
            if( self.config[ 'manager' ][ 'toLoop' ] ) :
                self.manager.parse_data(self.url)
                if( self.config[ 'manager' ][ 'last_messages' ] > -1 ) :
                    self.manager.set_start( self.config[ 'manager' ][ 'last_messages' ] )

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
        
        self.manager.parse_data(self.url)
        if( self.config[ 'manager' ][ 'last_messages' ] > -1 ) :
            self.manager.set_start( self.config[ 'manager' ][ 'last_messages' ] )

        if self.root:
            self.root.mainloop()
        else:
            while(1):
                self.update()

    def sendOut( self, label, score ) :
        '''
        Send out throught OSC and MIDI label and score outputted from model.
        OSC sent data are /label and /score.
        Midi data are sent as control change Midi messages whose numnber is define in the config file. 
        There three cc number : one for the label (0 : negative, 63 : neutral, 127 : positive), one for the whole part of the score as a percentage 
        and one for the frac part of the percentage
        '''
        score_whole , score_frac = self.splitScoreAsInts( score ) 

        ## OSC sends
        for client in self.osc_clients : 
            client.send_message( "/label", label )
            client.send_message( "/score", score )

        if( label == 'positive') : 
            value = 127
        elif( label == 'negative' ) :
            value = 0
        elif( label == 'neutral' ) :
            value = 63

        for midi_port in self.midi_outports :
            label_msg = mido.Message( 'control_change', control = self.config[ 'midi' ][ 'label_cc_nb' ], value = value )
            score_whole_msg = mido.Message( 'control_change', control = self.config[ 'midi' ][ 'score_int_cc_nb' ], value = score_whole )   
            score_frac_msg = mido.Message( 'control_change', control = self.config[ 'midi' ][ 'score_float_cc_nb' ], value = score_frac )   
            midi_port.send( label_msg )
            midi_port.send( score_whole_msg )
            midi_port.send( score_frac_msg )
        #score_int_cc_nb score_float_cc_nb

    def splitScoreAsInts( self, score ) :
        '''
        Rough function which splits the score taken as a percentage (between 0 and 100) into two ints representing the whole 
        and the frac part of the percentage.
        These two ints are used to be sent out as two separate midi control change messages.
        This function could be refined whith the use of math.modf.
        '''
        score = score * 100
        whole = int( score )
        frac = int( ( score - whole ) * 100 )

        return whole, frac

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
