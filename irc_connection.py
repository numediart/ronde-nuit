'''Connect to an IRC server to gather messages from one of its channel.
'''
import argparse

from src.irc_bot import IrcBot


def main():
    '''Main function used to parse command line arguments.

    Default configuration is :
        server : 'irc.chaat.fr'
        port : 6667
        channel : '#accueil'
        name : ronde
        file : output.json
    '''
    parser = argparse.ArgumentParser(
        description='Gather data (messages) from an IRC channel on a server.')
    parser.add_argument('-s', '--server', type=str, default='irc.chaat.fr',
                        help='IRC server to connect to.')
    parser.add_argument('-p', '--port', type=int, default=6667,
                        help='port to log on.')
    parser.add_argument('-c', '--channels', type=str, default=['#accueil'],
                        nargs='+', help='channel on the server to log in.')
    parser.add_argument('-n', '--name', type=str, default='ronde',
                        help='name of the bot on the server.')
    parser.add_argument('-f', '--file', type=str, default='output.json',
                        help='path to JSON file to store messages in.')
    args = parser.parse_args()

    bot = IrcBot(args.server, args.channels, args.name,
                 args.port, args.file)
    bot.start()


if __name__ == '__main__':
    main()
