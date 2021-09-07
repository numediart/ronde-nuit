from typing import Any, Dict, List

import ftfy
from colour import Color

from .format import remove_irc_formatting


class MsgManager():
    '''Colors on Tkinter should be #xxyyzz where xxyyzz is an hexadecimal number.
    '''

    def __init__(self,
                 analyzer,
                 colors: Dict):
        self.colors = colors.copy()
        self.analyzer = analyzer
        self.stack: List[Any] = []

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

    def update_stack(self, step=100):
        elem = self.data.pop(0)
        msg = remove_irc_formatting(elem['message'])
        msg = ftfy.ftfy(msg)

        _, label = self.analyzer.analyze(msg)
        fg = self.colors[label]["fg"]
        bg = self.colors[label]["bg"]

        if self.previous:
            pmsg, pfg, pbg, _ = self.previous
            for ifg, ibg in zip(self.colorRange(pfg, fg, step),
                                self.colorRange(pbg, bg, step)):
                self.stack.append((pmsg, ifg, ibg, 10))

        self.stack.append((msg, fg, bg, 10))

    def set_colors(self, colors):
        """
        """
        self.colors = colors.copy()

    def colorRange(self, colorStart, colorEnd, step=100):
        """
        """
        objColorStart = Color(colorStart)
        objColorEnd = Color(colorEnd)

        for elem in list(objColorStart.range_to(objColorEnd, step)):
            yield elem
