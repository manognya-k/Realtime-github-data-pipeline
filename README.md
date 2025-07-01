## **🚀 End-to-End GitHub Data Pipeline using Docker, Kafka, Spark, MySQL & React**
This project is a full-stack data pipeline that collects GitHub data in real-time, processes it with Apache Spark, stores the processed data in MySQL, and visualizes everything in a React dashboard. The entire setup runs locally using Docker and LocalStack, and infrastructure is provisioned using Terraform.

🧰 Tech Stack
Docker & Docker Compose – To containerize and run the services

LocalStack – To simulate AWS services like S3 locally

Terraform – For setting up infrastructure as code

Apache Kafka – For real-time streaming of GitHub events

Apache Spark (PySpark) – For data processing and transformation

MySQL – For storing structured/processed data

Flask – Backend API to serve data

React – Frontend dashboard to visualize GitHub data

🔄 📊 Pipeline Workflow
📥 1. GitHub Data Ingestion (Producer)
A Python script (github_producer.py) connects to the GitHub API.

It fetches repository or event data and sends it to a Kafka topic in real-time.

🧩 Technology Used: GitHub API + Kafka Producer

🔁 2. Kafka Consumer to S3 (Raw Layer)
Another Python script (kafka_to_s3.py) acts as a Kafka consumer.

It listens to the Kafka topic and writes incoming JSON data into a LocalStack S3 bucket, simulating AWS S3.

🧩 Technology Used: Kafka Consumer + LocalStack (S3)

🔄 3. Spark Transformation (Raw to Curated)
The PySpark job (spark_s3_to_mysql.py) reads the raw JSON files from S3.

It performs transformations like flattening, filtering, and formatting.

Finally, the cleaned data is loaded into a MySQL database for querying and analysis.

🧩 Technology Used: PySpark + MySQL

🔌 4. Flask REST API
The backend (flask_app.py) connects to the MySQL database.

It provides API endpoints that serve transformed GitHub data to the frontend.

🧩 Technology Used: Flask + SQLAlchemy (or connector)

🖥️ 5. React Frontend Dashboard
A React app (react-dashboard/) fetches data via Flask’s API.

It displays real-time GitHub insights such as:

Top repositories

Most active users

Commit activity

Star trends, etc.

🧩 Technology Used: React + Axios + Chart.js (or any graphing library)

✅ Expected Outcome
By the end of this pipeline:

🔃 Live GitHub data is fetched continuously.

📦 Data flows through Kafka → S3 → Spark → MySQL in real-time.

📊 A dashboard displays insightful GitHub metrics through REST API calls.

🐳 Everything runs seamlessly using Docker containers.

🧪 You get a local simulation of a cloud-based streaming pipeline without AWS costs using LocalStack.

