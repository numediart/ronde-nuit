'''Simple GUI for La Ronde de Nuit project.
'''
import argparse

from src.gui import create_ronde_gui


def parse_args():
    '''Define an argument parser and returns the corresponding dictionary.

    Returns
    -------
    dict
        dictionary of input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Runs La Ronde de Nuit demo.')
    parser.add_argument('-c', '--config', type=str,
                        default='config/default.yaml',
                        help='Configuration file for the demonstration.')
    parser.add_argument('-f', '--file', type=str,
                        default='https://nightwatch.couzinetjacques.com/ReqMsg_01.php',
                        help='file or website to read data from. If empty, this will open a file browser to select a file.')
    opt = parser.parse_args()

    return opt


if __name__ == "__main__":
    # Load parameters and config file
    opt = parse_args()

    # Create the GUI
    ronde = create_ronde_gui(opt.config, opt.file)

    # Init messages 

    # Run the mainloop
    ronde.mainloop()
