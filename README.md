# La Ronde de Nuit

This repository is dedicated to C2L3Play project called "La Ronde de Nuit".

This project contains several codes used for :
   * irc data extraction for sentiment-analysis annotation (to csv)
   * general text analysis and conversion (to json / csv)
   * sentiment analysis using default configuration of transformers libray or camembert
   * dataset structuring for general machine learning purpose
   * retraining of a sentiment analysis model
   * color / text visualisation of sentiment analysis

## How To


We will explain here the different scripts that can be used and how to use them. The available scripts are:
  * *irc_connection.py*
  * *online_read.py*
  * *convert2csv.py*
  * *train.py*
  * *analyze_file.py*
  * *ronde.py*

First we start with the setting up of the virtual env.

**Virtual env setup**

For some reasons pip install requirements.txt seems to loop on irc package, so we
divided installation of the packages in different parts gathered in script/install_packages.sh. 

> ```
> conda create -n ronde python=3.8
> cd /path/to/ronde-nuit/repo
> sudo chmod +x scripts/install_packages.sh
> cd scripts/
> ./install_package.sh
> ```

**Data collection from website or IRC**

First programs are used to extract messages / sentences from IRC or an online txt file.
We use 2 programs here:
  * **irc_connection.py** is used to connect to an IRC chat and save any message read from it.

> We can use the default configuration for extraction:
> ``` 
> python irc_connection.py
> ```
> 
> Or we can define our own server, port, channels, name and JSON file:
> ``` 
> python irc_connection.py -s 'irc.chaat.fr' -p 6667 -c '#accueil' '#maroc' -n 'ronde' -f 'output.json'
> ```
> 
> Multiple channels can be given at once. Output JSON file will have a 'channel' value with the channel tag.

  * **online_read.py** is used to get information from an online txt file.

> We need to define the url of the online txt file.
> ```
> python online_read.py 'http://someurl.com/myfile.txt'
> ```
> 
> We can also define the JSON file in which the sentences will be stored.
> ```
> python online_read.py 'http://someurl.com/myfile.txt' -f 'output.json'
> ``` 

**File conversion to CSV**

Extraction methods create JSON files. They need to be converted to CSV file for annotation.

We use *convert2csv.py* file for this purpose.

> Message extraction creates a JSON file. We use this function to convert JSON output to CSV file.
> 
> We can use the script with default parameters:
> ``` 
> python convert2csv.py 'data/whatsapp_500.json'
> ```
> 
> It is assumed that sentiment analysis is computed on the JSON file. Hence we can define which result we want to show in the CSV file:
> ``` 
> python convert2csv.py 'data/whatsapp_500.json' -c 'data/whatsapp_500.csv' -m 'default' 'camembert'
> ```

**Retraining the model**

Once the annotation is done, we can proceed to the training of our model.

**/!\ IMPORTANT: CSV columns used for retraining should be called 'message' (for the input text) and 'label' (for the corresponding sentiment).** 

We use *train.py* file for the retraining.

> We need to define the folder where our data is stored. The folder may contain multiple csv file. Be careful as they all will be used for training.
> ```
> python train.py 'data/sorted/'
> ```
> 
> Retraining requires a tokenisation model and a sentiment analysis model. Those can be modified as a parameter.
> ```
> python train.py 'data/sorted/' -t camembert-base -s 'tblard/tf-allocine'

**Run transformers' sentiment analysis**

We can now use our model for sentiment analysis. This is based on *analyze_file.py*.

> We can use the default sentiment analysis in transformers:
> ``` 
> python analyze_file.py 'data/whatsapp_500.json' -v 1
> ```
> 
> Or use the default behavior, which is based on CamemBERT model (for French language):
> ``` 
> python analyze_file.py 'data/whatsapp_500.json'
> ```

**Run GUI**

The GUI behavior depends on the YAML configuration file. The script used is *ronde.py*.

> ```
> python ronde.py
> ```
> 
> You can modify the configuration file used for the GUI. You can also define a file or website to base the GUI on.
> ```
> python ronde.py -c 'config/default.yaml' -f 'https://nightwatch.couzinetjacques.com/ReqMsg_01.php'
## Colaboratory

Colaboratory is an online tool to run python code. This do not require any local installation and can even train model on GPUs. The tool will open on the browser through this [link](https://colab.research.google.com/github/numediart/ronde-nuit/blob/master/ronde_nuit.ipynb).

## Some references

[Spacy](https://spacy.io/) is another framework like transformers for NLP. 

[ImageColorPicker](https://imagecolorpicker.com/) to help select colors.
