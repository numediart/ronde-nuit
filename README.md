# La Ronde de Nuit

This repository is dedicated to C2L3Play project called "La Ronde de Nuit".

This project contains several codes used for :
   * irc data extraction for sentiment-analysis annotation (to csv)
   * whatsapp conversation analysis and conversion (to json / csv)
   * sentiment analysis using default configuration of transformers libray
   * sentiment analysis using camembert (transformers library)

## How To

**WhatsApp Chat conversion**

The file used is *extract_msg.py*.

This command will convert the txt WhatsApp chat history file to JSON, extracting the 5000 first messages:
``` 
python extract_msg.py 'data/whatsapp_famille.txt' 'data/whatsapp_5000.json' -l 5000
```

We can also extract all messages as follow:
``` 
python extract_msg.py 'data/whatsapp_famille.txt' 'data/whatsapp.json'
```

**IRC message gathering**

The file used is *irc_connection.py*.

We can use the default configuration for extraction:
``` 
python irc_connection.py
```

Or we can define our own server, port, channels, name and JSON file:
``` 
python irc_connection.py -s 'irc.chaat.fr' -p 6667 -c '#accueil' '#maroc' -n 'ronde' -f 'output.json'
```

Multiple channels can be given at once. Output JSON file will have a 'channel' value with the channel tag.

**Run transformers' sentiment analysis**

The file used is *analyze_file.py*.

We can use the default sentiment analysis in transformers:
``` 
python analyze_file.py 'data/whatsapp_500.json' -v 1
```

Or use the default behavior, which is based on CamemBERT model (for French language):
``` 
python analyze_file.py 'data/whatsapp_500.json'
```

**Convert JSON to CSV files**

The file used is *convert2csv.py*.

Message extraction creates a JSON file. We use this function to convert JSON output to CSV file.

We can use the script with default parameters:
``` 
python convert2csv.py 'data/whatsapp_500.json'
```

It is assumed that sentiment analysis is computed on the JSON file. Hence we can define which result we want to show in the CSV file:
``` 
python convert2csv.py 'data/whatsapp_500.json' -c 'data/whatsapp_500.csv' -m 'default' 'camembert'
```

**Run GUI**

Simply use *ronde.py*.

```
python ronde.py
```
## TODO

* [x] General conversation
  * [x] Remove short sentences (less than 3 words, might be a parameter)
  * [x] Handle encoding issues with latin words and emojis
  * [x] Remove IRC formatting
* [x] IRC conversation
  * [x] Store IRC messages into JSON file
  * [x] Clean message information (remove useless [] or '')
  * [x] Analyze conversation with sentiment-analysis (camembert)
  * [x] Anonymize messages
* [x] Sentiment analysis
  * [x] Create a GUI showing colors based on sentiment
  * [x] Convert sentiment to color
  * [x] Set NEUTRAL threshold as a parameter
  * [x] Update JSON / CSV when analyzing instead of creating a new one
* [x] CSV 
  * [x] Color format rows depending on the analyzed sentiment
  * [x] Create CSV to JSON and JSON to CSV routine

## Some references

[Spacy](https://spacy.io/)