import abc
import json
from typing import Any, Dict, List

import ftfy
import requests
from colour import Color

from .analysis import SentimentAnalyzer
from .format import RondeHTML, remove_irc_formatting


class ColorManager():
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
        if label == 'negative' and self.index[ctype] < len(self.colors[ctype]) - 1:
            self.index[ctype] += 1
        if label == 'positive' and self.index[ctype] > 0:
            self.index[ctype] -= 1
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
        objColorStart = Color(cstart)
        objColorEnd = Color(cend)

        for elem in list(objColorStart.range_to(objColorEnd, steps)):
            yield elem


class AbstractMsgManager():
    def __init__(self,
                 config: Dict):
        self.analyzer = SentimentAnalyzer(
            config['models']['version'], config['models']['threshold'])
        self.stack: List[Any] = []

        self.colors = ColorManager(config['colors'])
        self.steps = config['manager']['steps']
        self.transition = config['manager']['transition']

        self.data: List[Any] = []
        self.previous = None

    def set_data(self, data):
        self.data = data

    def has_data(self):
        return len(self.data)

    def next_data(self):
        if not self.stack:
            if self.data:
                self.update_stack()

        if self.stack:
            self.previous = self.stack.pop(0)
            return self.previous
        return []

    def update_stack(self):
        '''
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

    def get_next_msg(self):
        '''
        '''
        msg = remove_irc_formatting(self.data.pop(0))
        return ftfy.ftfy(msg)

    @abc.abstractmethod
    def parse_data(self):
        pass


class MsgManager(AbstractMsgManager):
    '''
    '''

    def __init__(self,
                 config: Dict):
        super().__init__(config)

    def parse_data(self, url):
        with open(url) as f:
            msgs = [x['message'] for x in json.load(f)]
            self.set_data(msgs)


class OnlineMsgManager(AbstractMsgManager):
    '''Colors on Tkinter should be #xxyyzz where xxyyzz is an hexadecimal number.
    '''

    def __init__(self,
                 config: Dict):
        super().__init__(config)
        self.parser = RondeHTML()

    def parse_data(self, url):
        r = requests.get(url, allow_redirects=True)
        self.parser.feed(r.text)
        self.set_data(self.parser.stack)
