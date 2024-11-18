# Use the official Spark image as a base
FROM apache/spark:3.5.1

# Switch to root user to have permission to install packages
USER root

# Install dependencies and wget (to download MySQL JDBC driver and Hadoop AWS dependencies)
RUN apt-get update && apt-get install -y wget && apt-get clean

# Download MySQL JDBC driver and install it
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.30.tar.gz -P /tmp && \
    tar -xvzf /tmp/mysql-connector-java-8.0.30.tar.gz -C /tmp && \
    cp /tmp/mysql-connector-java-8.0.30/mysql-connector-java-8.0.30.jar /opt/spark/jars/

# Download Hadoop AWS and AWS SDK JARs for S3 support
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P /opt/spark/jars/ && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.517/aws-java-sdk-bundle-1.12.517.jar -P /opt/spark/jars/

# Set the Spark classpath to include the necessary JARs
ENV SPARK_CLASSPATH="/opt/spark/jars/*:/opt/spark/jars/mysql-connector-java-8.0.30.jar:/opt/spark/jars/hadoop-aws-3.3.4.jar:/opt/spark/jars/aws-java-sdk-bundle-1.12.517.jar"

# Optional: Add custom Spark configurations (if needed)
# COPY spark-defaults.conf /opt/spark/conf/

# Set the working directory
WORKDIR /opt/spark

# Expose necessary ports
EXPOSE 7077 8080 4040

# Default command to run Spark
CMD ["/opt/spark/bin/spark-submit", "--class", "org.apache.spark.examples.SparkPi", "--master", "spark://spark-master:7077", "--deploy-mode", "cluster", "--conf", "spark.kubernetes.container.image=767397764346.dkr.ecr.us-east-1.amazonaws.com/spark-repo/spark:latest", "/opt/spark/examples/jars/spark-examples_2.12-3.1.1.jar"]