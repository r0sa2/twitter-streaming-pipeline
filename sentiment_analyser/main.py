import json
from kafka import KafkaConsumer, KafkaProducer
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
import numpy
import os
import pickle
import re

SEQUENCE_LENGTH = 300

def preprocess(text):
    text = text.encode(encoding="ascii", errors="ignore").decode(encoding="ascii", errors="ignore") # Convert to ASCII
    text = text.lower() # To lowercase
    text = re.sub(pattern="&amp[,;]", repl="&", string=text) # Clean ampersands
    text = re.sub(pattern="#\S+", repl="[#]", string=text) # Clean hashtags
    text = re.sub(pattern="@\S+", repl="[@]", string=text) # Clean mentions
    text = re.sub(pattern="http[\S]+", repl="[/]", string=text) # Clean URLs
    text = re.sub(pattern="\s+", repl=" ", string=text) # Replace all whitespace with single space
    text = re.sub(pattern=r"[^A-Za-z0-9 ]+", repl="", string=text) # Retain alphanumeric characters/spaces
    text = re.sub(pattern=r"(.)\1\1+", repl=r"\1\1", string=text) # Replace three or more consecutive characters with two characters 
    return text

kafka_tweets_topic = os.environ["KAFKA_TWEETS_TOPIC"]
kafka_tweets_with_sentiment_topic = os.environ["KAFKA_TWEETS_WITH_SENTIMENT_TOPIC"]

consumer = KafkaConsumer(
    kafka_tweets_topic,
    bootstrap_servers=["kafka:9093"],
    value_deserializer= lambda x: json.loads(x.decode(encoding="utf-8", errors="strict")),
    auto_offset_reset="earliest"
)

producer = KafkaProducer(
    bootstrap_servers=["kafka:9093"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8", errors="strict")
)

with open(file="tokenizer.pickle", mode="rb") as f:
    tokenizer = pickle.load(f)

model = load_model("model.hdf5")

def get_sentiment_score(text):
    text = preprocess(text)
    sequence = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    return model.predict([sequence], verbose=0)[0][0]

for message in consumer:
    message_dict = message.value
    sentiment_score = get_sentiment_score(message_dict["text"])
    if sentiment_score >= 0.7:
        message_dict["sentiment_label"] = 1
    elif sentiment_score >= 0.3:
        message_dict["sentiment_label"] = 0
    else:
        message_dict["sentiment_label"] = -1
    message_dict["sentiment_score"] = str(sentiment_score)
    producer.send(kafka_tweets_with_sentiment_topic, message_dict)