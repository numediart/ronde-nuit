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
  * *extract_msg.py*
  * *irc_connection.py*
  * *analyze_file.py*
  * *convert2csv.py*
  * *ronde.py*

**WhatsApp Chat conversion**

> The file used is *extract_msg.py*.
> 
> This command will convert the txt WhatsApp chat history file to JSON, extracting the 5000 first messages:
> ``` 
> python extract_msg.py 'data/whatsapp_famille.txt' 'data/whatsapp_5000.json' -l 5000
> ```
> 
> We can also extract all messages as follow:
> ``` 
> python extract_msg.py 'data/whatsapp_famille.txt' 'data/whatsapp.json'
> ```

**IRC message gathering**

> The file used is *irc_connection.py*.
> 
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

**Run transformers' sentiment analysis**

> The file used is *analyze_file.py*.
> 
> We can use the default sentiment analysis in transformers:
> ``` 
> python analyze_file.py 'data/whatsapp_500.json' -v 1
> ```
> 
> Or use the default behavior, which is based on CamemBERT model (for French language):
> ``` 
> python analyze_file.py 'data/whatsapp_500.json'
> ```

**Convert JSON to CSV files**

> The file used is *convert2csv.py*.
> 
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

**Run GUI**

> Simply use *ronde.py*.
> 
> ```
> python ronde.py
> ```

## Colaboratory

Colaboratory is an online tool to run python code. This do not require any local installation and can even train model on GPUs. The tool will open on the browser through this [link](https://colab.research.google.com/github/numediart/ronde-nuit/blob/master/ronde_nuit.ipynb).

## Some references

[Spacy](https://spacy.io/) is another framework like transformers for NLP. 

[ImageColorPicker](https://imagecolorpicker.com/) to help select colors.