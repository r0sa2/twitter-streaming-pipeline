from datetime import datetime
from elasticsearch import Elasticsearch
import json
from kafka import KafkaConsumer
import os

kafka_tweets_with_sentiment_topic = os.environ["KAFKA_TWEETS_WITH_SENTIMENT_TOPIC"]
elasticsearch_index = os.environ["ELASTICSEARCH_INDEX"]

consumer = KafkaConsumer(
    kafka_tweets_with_sentiment_topic,
    bootstrap_servers=["kafka:9093"],
    value_deserializer= lambda x: json.loads(x.decode(encoding="utf-8", errors="strict")),
    auto_offset_reset="earliest"
)

client = Elasticsearch("http://elasticsearch:9200")

index = 1
for message in consumer:
    message_dict = message.value
    message_dict["time"] = datetime.fromisoformat(message_dict["time"])
    client.index(index=elasticsearch_index, id=index, document=message_dict)
    index += 1