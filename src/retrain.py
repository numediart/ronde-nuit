import os

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from transformers import (CamembertTokenizerFast,
                          TFCamembertForSequenceClassification, TFTrainer,
                          TFTrainingArguments)

from .dataset import create_splits


def compute_metrics(eval_pred):
    metrics_dict = {}
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)


def retrain(folder='data/sorted',
            token_model='camembert-base',
            sentiment_model='tblard/tf-allocine'):

    train_texts, train_labels = create_splits(
        os.path.join(folder, 'train.csv'))
    test_texts, test_labels = create_splits(
        os.path.join(folder, 'test.csv'))

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_texts, train_labels, test_size=.2)

    tokenizer = CamembertTokenizerFast.from_pretrained(token_model)

    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True)

    train_dataset = tf.data.Dataset.from_tensor_slices((
        dict(train_encodings),
        train_labels
    ))
    val_dataset = tf.data.Dataset.from_tensor_slices((
        dict(val_encodings),
        val_labels
    ))
    test_dataset = tf.data.Dataset.from_tensor_slices((
        dict(test_encodings),
        test_labels
    ))

    training_args = TFTrainingArguments(
        output_dir='./results',          # output directory
        num_train_epochs=100,            # total number of training epochs
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
