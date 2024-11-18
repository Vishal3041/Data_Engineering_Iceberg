from pyspark.sql import SparkSession
from pyspark.sql.functions import when, to_timestamp
import re
import os

# Set up environment variables for AWS credentials (recommended approach)
os.environ['AWS_ACCESS_KEY_ID'] = 'aws_access_key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'aws_secret_key'

# Initialize Spark session with S3 and Iceberg configurations
print("Creating Spark session")

spark = SparkSession.builder \
    .appName("S3 Log Transformation") \
    .config("spark.hadoop.fs.s3a.access.key", os.getenv('AWS_ACCESS_KEY_ID')) \
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv('AWS_SECRET_ACCESS_KEY')) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.jars", "bash_scripts/aws-java-sdk-bundle-1.12.517.jar,bash_scripts/iceberg-spark-runtime-3.5_2.12-1.7.0.jar,bash_scripts/hadoop-aws-3.3.4.jar") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.my_catalog.type", "hadoop") \
    .config("spark.sql.catalog.my_catalog.warehouse", "s3a://log-dataset-bucket/") \
    .getOrCreate()


# Set log level to ERROR to minimize log output
spark.sparkContext.setLogLevel("ERROR")

print("Spark session created successfully")

# Example to read a file from S3
bucket_name = "log-dataset-bucket"
file_key = "/logs/logs.txt"

# Load the log file from S3
s3_path = f"s3a://{bucket_name}/{file_key}"
try:
    logs_rdd = spark.read.text(s3_path)  # Read the file as an RDD of strings
    print(logs_rdd.show(5))  # Show some of the logs for debugging

    # Define the log pattern
    log_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?) (.*?) HTTP/.*" (\d+) (\d+) "-" "(.*?)"')

    # Process logs and create a list of dictionaries
    data = []
    for log in logs_rdd.collect():
        log_value = log['value']  # Extract the log string from the Row object
        match = log_pattern.match(log_value)
        if match:
            data.append({
                "ip": match.group(1),
                "timestamp": match.group(2),
                "method": match.group(3),
                "endpoint": match.group(4),
                "status": int(match.group(5)),
                "bytes": int(match.group(6)),
                "user_agent": match.group(7),
            })

    print("Transformed data: ", data)

    # Convert data to a Spark DataFrame
    df = spark.createDataFrame(data)
    print("DataFrame created: ", df)

    # Add device type based on user agent
    df = df.withColumn("device_type", 
                    when(df.user_agent.contains("Mobile"), "Mobile")
                    .when(df.user_agent.contains("Tablet"), "Tablet")
                    .otherwise("Desktop"))

    # Convert timestamp to datetime
    df = df.withColumn("datetime", to_timestamp(df["timestamp"], "dd/MMM/yyyy:HH:mm:ss Z"))
    print("DataFrame with datetime and device type: ", df)

    # Write the DataFrame to S3 as a single Parquet file
    parquet_path = "s3a://log-dataset-bucket/db_logs"
    df.coalesce(1).write.parquet(parquet_path, mode="overwrite")
    print(f"File written to S3 as Parquet: {parquet_path}")

    # Create Iceberg Table (if it doesn't exist)
    table_name = "my_catalog.db_logs"
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ip STRING,
            timestamp STRING,
            method STRING,
            endpoint STRING,
            status INT,
            bytes INT,
            user_agent STRING,
            device_type STRING,
            datetime TIMESTAMP
        )
        USING iceberg
        PARTITIONED BY (days(datetime))  -- Partition by day, adjust based on your needs
        LOCATION '{parquet_path}'
    """)
    print(f"Iceberg table {table_name} created")

    # Insert data into Iceberg table
    df.write.format("iceberg").mode("append").saveAsTable(table_name)
    print(f"Data inserted into Iceberg table {table_name} successfully")

    # 1. Top 5 IP Addresses by Request Count
    top_ips_query = """
        SELECT ip, COUNT(*) AS request_count
        FROM my_catalog.db_logs
        GROUP BY ip
        ORDER BY request_count DESC
        LIMIT 5
    """
    top_ips = spark.sql(top_ips_query)
    top_ips.show()

    # 2. Top 5 Devices by Request Count
    top_devices_query = """
        SELECT device_type, COUNT(*) AS request_count
        FROM my_catalog.db_logs
        GROUP BY device_type
        ORDER BY request_count DESC
        LIMIT 5
    """
    top_devices = spark.sql(top_devices_query)
    top_devices.show()

    # 3. Top 5 IP Addresses by Request Count (Daily)
    top_ips_daily_query = """
        SELECT ip, COUNT(*) AS request_count, DATE(datetime) AS day
        FROM my_catalog.db_logs
        GROUP BY ip, day
        ORDER BY day DESC, request_count DESC
        LIMIT 5
    """
    top_ips_daily = spark.sql(top_ips_daily_query)
    top_ips_daily.show()

    # 4. Top 5 IP Addresses by Request Count (Weekly)
    top_ips_weekly_query = """
        SELECT ip, COUNT(*) AS request_count, WEEKOFYEAR(datetime) AS week
        FROM my_catalog.db_logs
        GROUP BY ip, week
        ORDER BY week DESC, request_count DESC
        LIMIT 5
    """
    top_ips_weekly = spark.sql(top_ips_weekly_query)
    top_ips_weekly.show()

    # 5. Store Results in Separate Tables or Views
    top_ips.createOrReplaceTempView("top_ips_view")
    spark.sql("CREATE TABLE IF NOT EXISTS my_catalog.top_ips AS SELECT * FROM top_ips_view")

    top_ips_daily.createOrReplaceTempView("top_ips_daily_view")
    spark.sql("CREATE TABLE IF NOT EXISTS my_catalog.top_ips_daily AS SELECT * FROM top_ips_daily_view")

    top_ips_weekly.createOrReplaceTempView("top_ips_weekly_view")
    spark.sql("CREATE TABLE IF NOT EXISTS my_catalog.top_ips_weekly AS SELECT * FROM top_ips_weekly_view")

except Exception as e:
    print(f"Error reading file: {e}")