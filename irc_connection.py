'''Connect to an IRC server to gather messages from one of its channel.
'''
import argparse

from src.connection import IrcBot


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Gather data (messages) from an IRC channel on a server.')
    parser.add_argument('-s', '--server', type=str,
                        default='irc.chaat.fr',
                        help='IRC server to connect to.')
    parser.add_argument('-p', '--port', type=int,
                        default=6667,
                        help='port to log on.')
    parser.add_argument('-c', '--channels', type=str,
                        default=['#accueil'],
                        nargs='+', help='channel on the server to log in.')
    parser.add_argument('-n', '--name', type=str,
                        default='ronde',
                        help='name of the bot on the server.')
    parser.add_argument('-f', '--file', type=str,
                        default='output.json',
                        help='path to JSON file to store messages in.')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    # Load parameters
    opt = parse_args()

    bot = IrcBot(opt.server, opt.channels, opt.name, opt.port, opt.file)
    bot.start()
