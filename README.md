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

## Colaboratory
https://colab.research.google.com/drive/1PliF1rM7jO9RXFqBj4IOGi-PnVEqnzyV?usp=sharing

## TODO

* [ ] Visualisation
  * [ ] Add time between display in configuration
  * [ ] Change window display (make it as an option ?)
* [x] Colors
  * [x] Make ranging between two hexadecimal values
  * [x] Make it as a class ?
* [ ] Communication
  * [ ] Receive data from SQL server
* [ ] Model
  * [ ] Create code structure for retraining
  * [ ] Retrain with new annotation
  * [ ] Add to Colaboratory
* [x] Misc
  * [x] Cleanup colab
  * [x] Add explanations to colab
  * [ ] Download new data from Sylvain
  * [x] Apply sentiment analysis to Sylvain's data
## Some references

[Spacy](https://spacy.io/)
[ImageColorPicker](https://imagecolorpicker.com/)

### For development

[HuggingFace Dataset](https://huggingface.co/docs/datasets/add_dataset.html)
[TorchVision Dataset](https://pytorch.org/vision/stable/datasets.html)
[Torch Dataset](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html)
[HuggingFace Fine-tuning](https://huggingface.co/transformers/training.html)

Example of dataset (Allocine): 
[Allocine Dataset Structure](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/create_dataset.ipynb)
[Allocine Dataset Code](https://github.com/huggingface/datasets/blob/master/datasets/allocine/allocine.py)