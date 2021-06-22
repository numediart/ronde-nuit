# La Ronde de Nuit

This repository is dedicated to C2L3Play project called "La Ronde de Nuit".

This project contains several codes used for :
   * irc data extraction for sentiment-analysis annotation (to csv)
   * whatsapp conversation analysis and conversion (to json / csv)
   * sentiment analysis using default configuration of transformers libray
   * sentiment analysis using camembert (transformers library)


## TODO

* [ ] General conversation
  * [ ] Remove short sentences (less than 3 words, might be a parameter)
  * [ ] Handle encoding issues with latin words and emojis 
* [ ] IRC conversation
  * [ ] Store IRC messages into JSON file
  * [ ] Clean message information (remove useless [] or '')
  * [ ] Analyze conversation with sentiment-analysis (camembert)
* [ ] Sentiment analysis
  * [ ] Create a GUI showing colors based on sentiment
  * [ ] Convert sentiment to color
  * [ ] Set NEUTRAL threshold as a parameter
* [ ] CSV 
  * [ ] Color format rows depending on the analyzed sentiment
