from kafka import KafkaProducer
import requests, json


producer = KafkaProducer(bootstrap_servers='localhost:9092', 
                        value_serializer=lambda v: json.dumps(v).encode('utf-8')
                        )
                        
def on_send_success(record_metadata):
    print(f"Sent to {record_metadata.topic} [partition {record_metadata.partition}]")

def on_send_error(excp):
    print(f"Failed to send: {excp}")
    
for item in requests.get("https://api.github.com/repos/apache/spark/issues").json():
    producer.send("github-issues", item).add_callback(on_send_success).add_errback(on_send_error)

producer.flush()