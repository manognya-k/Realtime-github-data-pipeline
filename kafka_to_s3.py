import json
import boto3
from kafka import KafkaConsumer
from datetime import datetime
import uuid

# --- CONFIGURATION ---
KAFKA_TOPIC = "github-issues"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

S3_BUCKET = "github-pipeline-bucket"
S3_PREFIX = "issues/"  # S3 folder
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_ACCESS_KEY = "mock"
AWS_SECRET_KEY = "mock"

# --- S3 CLIENT ---
s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="us-east-1"
)

# --- KAFKA CONSUMER ---
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False
)

print(f"Listening to topic '{KAFKA_TOPIC}'...")

for message in consumer:
    issue = message.value

    # Construct file name and content
    file_id = f"{uuid.uuid4().hex}.json"
    s3_key = f"{S3_PREFIX}{file_id}"
    json_data = json.dumps(issue, indent=2)

    # Upload to S3 (LocalStack)
    response = s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=json_data,
        ContentType="application/json"
    )
    
    print(f"✅ Uploaded: {s3_key}")
