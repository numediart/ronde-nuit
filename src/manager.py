import abc
import json
from typing import Any, Dict, List, Optional

import ftfy
import requests
from colour import Color

from .analysis import SentimentAnalyzer
from .format import RondeHTML, remove_irc_formatting


class ColorManager():
    '''Manages background and foreground (text) colors.

    Attributes
    ----------
    colors : dict
        dictionary contains 2 keys:
          - fg, list of foreground colors or str of unique color
          - bg, list of background colors or str of unique color
    index : dict
        dictionary containing 2 keys:
          - fg, index of the current foreground color in colors
          - bg, index of the current background color in colors
    '''

    def __init__(self,
                 colors: Dict):
        """Set the color dictionnary to new values.

        Args
        ----
        colors : dict
            the dictionnary of colors which should be structured as:
              - fg, list of foreground colors or str of unique color
              - bg, list of background colors or str of unique color
        """
        if isinstance(colors['fg'], str):
            colors['fg'] = [colors['fg']]

        if isinstance(colors['bg'], str):
            colors['bg'] = [colors['bg']]

        self.colors = colors.copy()

        self.index = {}
        self.index['fg'] = len(self.colors['fg'])//2
        self.index['bg'] = len(self.colors['bg'])//2

    def get_current(self,
                    ctype: str):
        '''Get current color of an element.

        Args
        ----
        ctype : str
            element to get color from. Can either be 'fg' (foreground, i.e. text color) or 'bg' (background)

        Returns
        -------
        str
            current element color
        '''
        return self.colors[ctype][self.index[ctype]]

    def get_next(self,
                 label: str,
                 ctype: str):
        '''Get the next color depending on label.

        Args
        ----
        label : str
            sequence label. Can either be 'positive', 'neutral' or 'negative'
        ctype : str
            element to get color from. Can either be 'fg' (foreground, i.e. text color) or 'bg' (background)

        Returns
        -------
        str
            next color for element
        '''
        # Negative value moves to next index
        if label == 'negative' and self.index[ctype] < len(self.colors[ctype]) - 1:
            self.index[ctype] += 1

        # Positive value moves to previous index
        if label == 'positive' and self.index[ctype] > 0:
            self.index[ctype] -= 1

        # Neutral moves closer to "center" index (half the length of array)
        if label == 'neutral':
            if self.index[ctype] > len(self.colors[ctype])//2:
                self.index[ctype] -= 1
            elif self.index[ctype] < len(self.colors[ctype])//2:
                self.index[ctype] += 1

        return self.colors[ctype][self.index[ctype]]

    def colorRange(self,
                   cstart: str,
                   cend: str,
                   steps: int = 100):
        """Compute a range between to colors.

        Args
        ----
        cstart : str
            starting color
        cend : str
            ending color
        steps : int, optional
            number of colors on the range.
            Default is 100.

        Returns
        -------
        Iterator
            iterator on colors in the range
        """
        for elem in list(Color(cstart).range_to(Color(cend), steps)):
            yield elem


class AbstractMsgManager():
    '''Generic class to handle messages.

    Class inheriting this should define the parse_data method, which defines
    how to load a list of messages.

    The general behavior is as follow:
      - messages are loaded from a given source (typically txt file or url address)
      - each message is analyzed and added to a stack for treatment
      - once loaded messages stack is empty, look for new input (usually if input is url)
      - loop through previous steps

    Attributes
    ----------
    analyzer : SentimentAnalyzer
        model to analyze sentiment on a sequence
    stack : list of tuple
        list of tuple containing information on the next message to handle.
        Tuple structure is (<msg>, <fg>, <bg>, <label>, <score>) where
          - <msg> is the message
          - <fg> is its color
          - <bg> is the background color
          - <label> is the detected sentiment label
          - <score> is the analysis confidence
    colors : ColorManager
        manager to handle the colors and their transition
    steps : int
        number of steps for color grading between 2 messages
    messages : list
        list of messages to be handled.
    previous : tuple
        tuple of previous read message. This is mainly used to handle color range.
    '''

    def __init__(self,
                 config: Dict):
        '''Creates a MsgManager

        Args
        ----
        config : dict
            dictionary of configuration for the manager. Dictionary should have:
              - 'models' which should contain
                - 'version', an int for the model version
                - 'threshold', a float to define the score threshold under which label is set to 'neutral'
              - 'colors', the color manager configuration
              - 'manager' which should contain
                - 'steps', an int representing the number of steps for color ranging
        '''
        self.analyzer = SentimentAnalyzer(
            config['models']['version'], config['models']['threshold'])
        self.stack: List[Any] = []

        self.colors = ColorManager(config['colors'])
        self.steps = config['manager']['steps']

        self.messages: List[Any] = []
        self.previous = None

    def set_messages(self,
                     messages: List[str]) -> None:
        '''Set the list of messages.

        Args
        ----
        messages : list of str
            list of messages to set in the stack
        '''
        self.messages = messages.copy()

    def has_messages(self) -> bool:
        '''Returns if data has a message to be read.

        Returns
        -------
        bool
            True if data has any element, False otherwise
        '''
        return any(self.messages)

    def set_start(self, last) -> Optional[Any] :
        '''Define at which messages from the end the stack should really starts.
        This function will prevent from displaying all messages but the n last.
        Prevent from having to go throught all messages before starting to read all of them.
        '''
        self.messages = self.messages[ -last: ]

        return None

    def next_data(self) -> Optional[Any]:
        '''Get the next message in data stack.

        Returns
        -------
        tuple
            data related to the next message
        '''
        if not self.stack:
            if self.has_messages():
                self.update_stack()

        if self.stack:
            self.previous = self.stack.pop(0)
            return self.previous
        return None

    def update_stack(self) -> None:
        '''Update the stack of handled messages.

        Method will:
          - get the next message from messages stack
          - analyze the message
          - get the next colors depending on the label
            - create a range of colors between previous and current color if needed
          - add new info to the stack
        '''
        msg = self.get_next_msg()

        score, label = self.analyzer.analyze(msg)

        fg = self.colors.get_next(label, 'fg')
        bg = self.colors.get_next(label, "bg")

        if self.previous and self.steps > 0:
            pmsg, pfg, pbg, plab, psco = self.previous
            for ifg, ibg in zip(self.colors.colorRange(pfg, fg, self.steps),
                                self.colors.colorRange(pbg, bg, self.steps)):
                self.stack.append(
                    (pmsg, ifg, ibg, plab, psco))

        self.stack.append((msg, fg, bg, label, score))

    def get_next_msg(self) -> str:
        '''Collect and format the next message read.

        Returns
        -------
        str
            formatted next message to handle
        '''
        msg = remove_irc_formatting(self.messages.pop(0))
        return ftfy.ftfy(msg)

    @abc.abstractmethod
    def parse_data(self,
                   url: str) -> None:
        '''This method loads from data from an url.

        No returns, but messages attribute should be updated with new messages.

        Args
        ----
        url : str
            path to a file or webpage to handle messages.
        '''
        pass


class JsonMsgManager(AbstractMsgManager):
    '''Class to handle messages from a JSON file.

    Json file should be an array of dictionary.
    Each dictionary should have a key named 'message', which is the message to analyze.
    '''

    def __init__(self,
                 config: Dict):
        super().__init__(config)

    def parse_data(self,
                   url: str) -> None:
        with open(url) as f:
            msgs = [x['message'] for x in json.load(f)]
            self.set_messages(msgs)


class OnlineMsgManager(AbstractMsgManager):
    '''Class to handle messages from an HTML table.

    Handle table structure is defined in src.format.RondeHTML class.

    Attributes
    ----------
    parser : RondeHTML
        HTML parser used to handle data from the HTML table.
    '''

    def __init__(self,
                 config: Dict):
        super().__init__(config)
        self.parser = RondeHTML()

    def parse_data(self,
                   url: str) -> None:
        r = requests.get(url, allow_redirects=True)
        print( type( r.text ) )
        self.parser.feed(r.text)
        self.set_messages(self.parser.stack)
        