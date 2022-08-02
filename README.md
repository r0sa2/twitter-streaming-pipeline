# Twitter Streaming Pipeline
## About
This repository is intended to document the implementation of an end-to-end Twitter streaming pipeline for sentiment analysis. The implementation is bare-bones in the sense that the primary focus is on how to minimally connect the different pipeline components together. Issues such as authentication, scaling with Docker Swarm/Kubernetes, cloud deployment etc. are not the focus here.

## Sentiment Analysis
Sentiment analysis is performed using an LSTM model trained on the <a href="https://www.kaggle.com/datasets/kazanova/sentiment140">sentiment140 dataset</a>. The classification report of the trained model on the test dataset (10% of the total dataset) is depicted below.

<p align="center">
    <img src="/assets/classification_report.png" alt="Flowchart" height="60%" width="60%"/>
</p>

## Pipeline Architecture
The pipeline architecture is depicted in the flowchart below. Each of the components is housed in a separate Docker container.

<p align="center">
    <img src="/assets/flowchart.png" alt="Flowchart" height="90%" width="90%"/>
</p>

In words,
1. The Tweepy producer writes tweets filtered based on a given keyword to the Kafka ```tweets``` topic.
2. The sentiment analyser consumes tweets from the ```tweets``` topic, computes their sentiment, and writes the tweets with their sentiments to the ```tweets_with_sentiment``` topic.
3. There are two separate sinks - an Elasticsearch/Kibana sink, and an InfluxDB/Grafana sink. Each sink has a connector that consumes from the ```tweets_with_sentiment``` topic and writes to the sink. ```compose-ek.yaml``` contains the implementation of the Elasticsearch/Kibana sink, and  ```compose-ig.yaml``` contains the implementation of the InfluxDB/Grafana sink.

## Dashboards
A sample Kibana dashboard is depicted below. It contains visualizations for the total no. of tweets processed, the no. of tweets processed as a time series over the last 10 minutes, the average sentiment as a time series over the last 10 minutes, and 5 recent tweets. 

<p align="center">
    <img src="/assets/kibana_dashboard.png" alt="Kibana Dashboard" height="90%" width="90%"/>
</p>

A sample Grafana dashboard with the same visualizations is depicted below.

<p align="center">
    <img src="/assets/grafana_dashboard.png" alt="Grafana Dashboard" height="90%" width="90%"/>
</p>

## Usage
1. Setup a Twitter developer account and install Docker desktop on the host machine.
2. Fill in the environment variables with the missing values in the compose file.
3. Using compose v2 syntax, run the pipeline with the Elasticsearch/Kibana sink with ```docker compose -f compose-ek.yaml up```, or the pipeline with the InfluxDB/Grafana sink with ```docker compose -f compose-ig.yaml up```.
4. ```notes.txt``` contains some additional instructions for InfluxDB/Grafana setup. Note that the instructions aren't comprehensive, and primarily intended to remind me of what I did.

## References
* https://www.kaggle.com/datasets/kazanova/sentiment140
* https://www.youtube.com/watch?v=Lu1nskBkPJU&ab_channel=AISpectrum (Twitter developer account setup)
* https://docs.docker.com/engine/install/
