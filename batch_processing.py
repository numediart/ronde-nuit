import os

from src.analysis import run_model
from src.whatsapp import convert_chat

input_file = os.path.join('data', 'whatsapp_famille.txt')
jsonfile_100 = os.path.join('data', 'whatsapp_100.json')
jsonfile_5000 = os.path.join('data', 'whatsapp_5000.json')

convert_chat(input_file, jsonfile_100, 100)
convert_chat(input_file, jsonfile_5000, 5000)

run_model(jsonfile_100, 0)
run_model(jsonfile_100, 1)
run_model(jsonfile_5000, 0)
run_model(jsonfile_5000, 1)


jsonfile_irc1 = os.path.join('data', 'chaat_accueil.json')
jsonfile_irc2 = os.path.join('data', 'irc_chat.json')

run_model(jsonfile_irc1, 0)
run_model(jsonfile_irc1, 1)
run_model(jsonfile_irc2, 0)
run_model(jsonfile_irc2, 1)
