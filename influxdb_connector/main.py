from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
import json
from kafka import KafkaConsumer
import os

kafka_tweets_with_sentiment_topic = os.environ["KAFKA_TWEETS_WITH_SENTIMENT_TOPIC"]
influxdb_org = os.environ["INFLUXDB_ORG"]
influxdb_token = os.environ["INFLUXDB_TOKEN"]
influxdb_bucket = os.environ["INFLUXDB_BUCKET"]
influxdb_measurement = os.environ["INFLUXDB_MEASUREMENT"]

consumer = KafkaConsumer(
    kafka_tweets_with_sentiment_topic,
    bootstrap_servers=["kafka:9093"],
    value_deserializer= lambda x: json.loads(x.decode(encoding="utf-8", errors="strict")),
    auto_offset_reset="earliest"
)

client = InfluxDBClient(
    url="http://influxdb:8086", 
    token=influxdb_token, 
    org=influxdb_org
)
write_api = client.write_api(write_options=ASYNCHRONOUS)

for message in consumer:
    message_dict = {}
    message_dict["measurement"] = influxdb_measurement
    message_dict["time"] = message.value["time"]
    message_dict["fields"] = {
        "text": message.value["text"],
        "sentiment_label": message.value["sentiment_label"],
        "sentiment_score": message.value["sentiment_score"]
    }
    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=message_dict)