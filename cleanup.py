import os
import json


def remove_irc_formatting(msg):
    '''Removes the tags for IRC formatting characters.

    Based on https://gist.github.com/ion1/2791653
    '''
    msg = msg.replace('\\x02', '')    # bold
    msg = msg.replace('\\x12', '')    # reverse
    msg = msg.replace('\\x1f', '')    # underline

    msg = msg.replace('\\x11', '')    # fixed
    msg = msg.replace('\\x16', '')    # reverse
    msg = msg.replace('\\x1d', '')    # italic

    msg = msg.replace('\\x030', '')   # white
    msg = msg.replace('\\x031', '')   # black
    msg = msg.replace('\\x032', '')   # blue
    msg = msg.replace('\\x033', '')   # green
    msg = msg.replace('\\x034', '')   # red
    msg = msg.replace('\\x035', '')   # brown
    msg = msg.replace('\\x036', '')   # purple
    msg = msg.replace('\\x037', '')   # orange
    msg = msg.replace('\\x038', '')   # yellow
    msg = msg.replace('\\x039', '')   # light green
    msg = msg.replace('\\x0310', '')  # teal
    msg = msg.replace('\\x0311', '')  # light cyan
    msg = msg.replace('\\x0312', '')  # light blue
    msg = msg.replace('\\x0313', '')  # pink
    msg = msg.replace('\\x0314', '')  # grey
    msg = msg.replace('\\x0315', '')  # light brey
    msg = msg.replace('\\x03', '')    # color
    return msg


def main():
    path = os.path.join('data', 'chaat_accueil.json')
    with open(path) as f:
        data = json.load(f)

    for elem in data:
        msg = remove_irc_formatting(elem['message'])
        if len(msg) > 3:
            print(msg)


if __name__ == '__main__':
    main()
