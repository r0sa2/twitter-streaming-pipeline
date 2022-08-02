import json
from kafka import KafkaProducer
import os
import tweepy

twitter_api_key = os.environ["TWITTER_API_KEY"]
twitter_api_key_secret = os.environ["TWITTER_API_KEY_SECRET"]
twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
twitter_access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
twitter_keyword = os.environ["TWITTER_KEYWORD"]
kafka_tweets_topic = os.environ["KAFKA_TWEETS_TOPIC"]

producer = KafkaProducer(
    bootstrap_servers=["kafka:9093"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8", errors="strict")
)

class StreamListener(tweepy.Stream):
    def on_status(self, status):
        message = {
            "time": status.created_at.isoformat(),
            "text": status.text
        }
        producer.send(kafka_tweets_topic, message)

streamListener = StreamListener(
    consumer_key=twitter_api_key,
    consumer_secret=twitter_api_key_secret,
    access_token=twitter_access_token,
    access_token_secret=twitter_access_token_secret
)

streamListener.filter(
    track=[twitter_keyword],
    languages=["en"]
)