import os

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from transformers import (CamembertTokenizerFast,
                          TFCamembertForSequenceClassification, TFTrainer,
                          TFTrainingArguments)

from .dataset import get_split


def compute_metrics(eval_pred):
    """Metric used for prediction.
    """
    predictions, _ = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return predictions


def retrain(folder,
            token_model='camembert-base',
            sentiment_model='tblard/tf-allocine'):
    '''Retrain a sentiment analysis model.

    Args
    ----
    folder : str
        folder to containing data to retrain from.
        Folder should contain 2 csv files named train.csv (for training) and test.csv (for testing).
    token_model : str, optional
        Model used for tokenisation. It should be a pretrained from CamembertTokenizerFast class.
        Default is 'camembert-base'.
    sentiment_model : str, optional
        Model used for retraining. It should be a pretrained from TFCamembertForSequenceClassification. 
        Default is 'tblard/tf-allocine'.

    Returns
    -------
    TFTrainer
        trained model. Model is also saved in results folder.
    '''

    train_texts, train_labels = get_split(os.path.join(folder, 'train.csv'))

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_texts, train_labels, test_size=.2)

    tokenizer = CamembertTokenizerFast.from_pretrained(token_model)

    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True)

    train_dataset = tf.data.Dataset.from_tensor_slices((
        dict(train_encodings),
        train_labels
    ))
    val_dataset = tf.data.Dataset.from_tensor_slices((
        dict(val_encodings),
        val_labels
    ))

    training_args = TFTrainingArguments(
        output_dir='./results',          # output directory
        num_train_epochs=50,             # total number of training epochs
        per_device_train_batch_size=16,  # batch size per device during training
        per_device_eval_batch_size=64,   # batch size for evaluation
        warmup_steps=50,                 # number of warmup steps for learning rate scheduler
        weight_decay=0.01,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=10,
        save_strategy='steps',
        save_steps=10,
        save_total_limit=5,
        debug=True
    )

    with training_args.strategy.scope():
        model = TFCamembertForSequenceClassification.from_pretrained(
            sentiment_model)

    trainer = TFTrainer(model=model,
                        args=training_args,
                        train_dataset=train_dataset,
                        eval_dataset=val_dataset,
                        compute_metrics=compute_metrics
                        )

    trainer.train()
    trainer.save_model('results')
    return trainer
