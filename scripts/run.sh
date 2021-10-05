export PATH="~/miniconda3/bin:$PATH"
source activate c2l3play

cd ronde-nuit/
python ronde.py -f 'https://nightwatch.couzinetjacques.com/ReqMsg_01.php'
