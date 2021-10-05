from typing import Any, Dict, List
import requests

import ftfy
from colour import Color

from .format import remove_irc_formatting, RondeHTML


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

    def get_current(self, ctype):
        return self.colors[ctype][self.index[ctype]]

    def get_next(self, label, ctype):
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

    def colorRange(self, colorStart, colorEnd, step=100):
        """
        """
        objColorStart = Color(colorStart)
        objColorEnd = Color(colorEnd)

        for elem in list(objColorStart.range_to(objColorEnd, step)):
            yield elem


class MsgManager():
    '''Colors on Tkinter should be #xxyyzz where xxyyzz is an hexadecimal number.
    '''

    def __init__(self,
                 analyzer,
                 colors: Dict,
                 steps=100,
                 transition=10):
        self.analyzer = analyzer
        self.stack: List[Any] = []

        self.colors = ColorManager(colors)
        self.previous = None
        self.steps = steps
        self.transition = transition

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
        elem = self.data.pop(0)
        msg = remove_irc_formatting(elem['message'])
        msg = ftfy.ftfy(msg)

        _, label = self.analyzer.analyze(msg)

        fg = self.colors.get_next(label, 'fg')
        bg = self.colors.get_next(label, "bg")

        if self.previous and self.steps > 0:
            pmsg, pfg, pbg, _, plab = self.previous
            for ifg, ibg in zip(self.colors.colorRange(pfg, fg, self.steps),
                                self.colors.colorRange(pbg, bg, self.steps)):
                self.stack.append((pmsg, ifg, ibg, self.transition, plab))

        self.stack.append((msg, fg, bg, self.transition, label))


class OnlineMsgManager():
    '''Colors on Tkinter should be #xxyyzz where xxyyzz is an hexadecimal number.
    '''

    def __init__(self,
                 analyzer,
                 colors: Dict,
                 steps=100,
                 transition=10):
        self.analyzer = analyzer
        self.stack: List[Any] = []

        self.colors = ColorManager(colors)
        self.previous = None
        self.steps = steps
        self.transition = transition
        self.parser = RondeHTML()

    def parse_data(self, url):
        r = requests.get(url, allow_redirects=True)
        self.parser.feed(r.text)
        self.set_data(self.parser.to_read)

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
        elem = self.data.pop(0)
        msg = remove_irc_formatting(elem)
        msg = ftfy.ftfy(msg)

        _, label = self.analyzer.analyze(msg)

        fg = self.colors.get_next(label, 'fg')
        bg = self.colors.get_next(label, "bg")

        if self.previous and self.steps > 0:
            pmsg, pfg, pbg, _, plab = self.previous
            for ifg, ibg in zip(self.colors.colorRange(pfg, fg, self.steps),
                                self.colors.colorRange(pbg, bg, self.steps)):
                self.stack.append((pmsg, ifg, ibg, self.transition, plab))

        self.stack.append((msg, fg, bg, self.transition, label))
