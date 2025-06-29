import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode
from pyspark.sql.types import *

# Define the relevant schema from JSON
# Define schema of the incoming JSON from Kafka
issue_schema = StructType([
    StructField("url", StringType()),
    StructField("repository_url", StringType()),
    StructField("labels_url", StringType()),
    StructField("comments_url", StringType()),
    StructField("events_url", StringType()),
    StructField("html_url", StringType()),
    StructField("id", LongType()),
    StructField("node_id", StringType()),
    StructField("number", LongType()),
    StructField("title", StringType()),
    StructField("user", StructType([
        StructField("login", StringType()),
        StructField("id", LongType()),
        StructField("node_id", StringType()),
        StructField("avatar_url", StringType()),
        StructField("gravatar_id", StringType()),
        StructField("url", StringType()),
        StructField("html_url", StringType()),
        StructField("followers_url", StringType()),
        StructField("following_url", StringType()),
        StructField("gists_url", StringType()),
        StructField("starred_url", StringType()),
        StructField("subscriptions_url", StringType()),
        StructField("organizations_url", StringType()),
        StructField("repos_url", StringType()),
        StructField("events_url", StringType()),
        StructField("received_events_url", StringType()),
        StructField("type", StringType()),
        StructField("user_view_type", StringType()),
        StructField("site_admin", BooleanType())
    ])),
    StructField("labels", ArrayType(StructType([
        StructField("id", LongType()),
        StructField("node_id", StringType()),
        StructField("url", StringType()),
        StructField("name", StringType()),
        StructField("color", StringType()),
        StructField("default", BooleanType()),
        StructField("description", StringType())
    ]))),
    StructField("state", StringType()),
    StructField("locked", BooleanType()),
    StructField("assignee", StructType([
        StructField("login", StringType()),
        StructField("id", LongType()),
        StructField("node_id", StringType()),
        StructField("avatar_url", StringType()),
        StructField("gravatar_id", StringType()),
        StructField("url", StringType()),
        StructField("html_url", StringType()),
        StructField("followers_url", StringType()),
        StructField("following_url", StringType()),
        StructField("gists_url", StringType()),
        StructField("starred_url", StringType()),
        StructField("subscriptions_url", StringType()),
        StructField("organizations_url", StringType()),
        StructField("repos_url", StringType()),
        StructField("events_url", StringType()),
        StructField("received_events_url", StringType()),
        StructField("type", StringType()),
        StructField("user_view_type", StringType()),
        StructField("site_admin", BooleanType())
    ])),
    StructField("assignees", ArrayType(MapType(StringType(), StringType()))),
    StructField("milestone", NullType()),
    StructField("comments", LongType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("closed_at", StringType()),
    StructField("author_association", StringType()),
    StructField("type", StringType()),
    StructField("active_lock_reason", StringType()),
    StructField("draft", BooleanType()),
    StructField("pull_request", StructType([
        StructField("url", StringType()),
        StructField("html_url", StringType()),
        StructField("diff_url", StringType()),
        StructField("patch_url", StringType()),
        StructField("merged_at", StringType())
    ])),
    StructField("body", StringType()),
    StructField("closed_by", NullType()),
    StructField("reactions", StructType([
        StructField("url", StringType()),
        StructField("total_count", LongType()),
        StructField("+1", LongType()),
        StructField("-1", LongType()),
        StructField("laugh", LongType()),
        StructField("hooray", LongType()),
        StructField("confused", LongType()),
        StructField("heart", LongType()),
        StructField("rocket", LongType()),
        StructField("eyes", LongType())
    ])),
    StructField("timeline_url", StringType()),
    StructField("performed_via_github_app", NullType()),
    StructField("state_reason", StringType())
])

# Spark session with S3 and MySQL connector settings
spark = SparkSession.builder \
    .appName("S3ToMySQL") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:4566") \
     .config("spark.hadoop.fs.s3a.access.key", "mock") \
    .config("spark.hadoop.fs.s3a.secret.key", "mock") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .getOrCreate()


# Read all JSON files under the 'issues' prefix
raw_df = spark.read.option("multiline", "true").schema(issue_schema).json("s3a://github-pipeline-bucket/issues/*.json")

exploded_df = raw_df.select("id", "title", explode("labels").alias("label")).select ("id", "title",col("label.name").alias("program_name"))



# Write to local filesystem partitioned by label name
# exploded_df.write \
#   .mode("overwrite") \
#   .partitionBy("program_name") \
#   .format("json") \
#   .save("file:///E:/real-time-pipeline/issues_partitioned_by_label")

exploded_df.show()

# Write to MySQL database
exploded_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3307/github") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "issues") \
        .option("user", "root") \
        .option("password", "password") \
        .mode("append") \
        .save()

print("Data written to MySQL database successfully.")

spark.stop()