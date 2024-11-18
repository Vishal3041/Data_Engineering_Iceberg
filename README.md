# Data Engineering Iceberg Assignment

## 🚀 Overview

This project implements a **scalable data pipeline** to process website log data for actionable analytics. It utilizes **Apache Spark**, **Amazon S3**, and **Apache Iceberg** to transform raw logs into structured insights. The pipeline provides daily and weekly metrics for:
- **Top 5 IP addresses by request count**.
- **Top 5 devices (mobile, desktop, tablet)**.

All components are deployed on a Kubernetes cluster managed via **AWS EKS**, with infrastructure provisioned using **Terraform**.

---

## 📚 Architecture

### Key Components:
1. **Data Ingestion**:
   - Raw logs stored in **Amazon S3** as text files.
2. **Data Transformation**:
   - Apache Spark processes logs, partitions data by date, and stores it in Iceberg format on S3.
3. **Query Engine**:
   - Spark SQL computes analytics using Iceberg tables.
4. **Infrastructure**:
   - **EKS cluster** hosts the Spark jobs.
   - **Amazon RDS** serves as the Hive Metastore backend.

### 🗺️ Architecture Diagram
![Architecture Diagram](Data_Pipeline_Flowchart_Spaced_Portrait.png)  


---

## 🛠️ Prerequisites

Make sure you have the following tools installed and configured:
- **Terraform**: Infrastructure provisioning  
  ```bash
  brew install terraform       # macOS  
  sudo apt install terraform   # Linux  
  ```
- **AWS CLI**: AWS resource management  
  ```bash
  aws configure  
  ```
- **kubectl**: Kubernetes cluster interaction  
  ```bash
  brew install kubectl       # macOS  
  curl -LO <kubernetes_release_url> # Linux  
  ```
- **Python Virtual Environment**: For Python dependencies  
  ```bash
  python3 -m venv env  
  source env/bin/activate    # macOS/Linux  
  pip install py4j pyspark  
  ```

---

## 🚧 Setup Instructions

### 1️⃣ Infrastructure Deployment
1. Clone the repository:  
   ```bash
   git clone https://github.com/Vishal3041/Private-proj.git
   cd Private-proj
   ```
2. Navigate to the Terraform directory and initialize Terraform:  
   ```bash
   terraform init  
   terraform plan  
   terraform apply --auto-approve  
   ```
3. Verify resources:
   ```bash
   kubectl get nodes  
   aws s3 ls  
   ```

### 2️⃣ Spark Setup on EKS
1. Deploy the Spark operator:  
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami  
   helm install spark bitnami/spark --namespace default \  
       --set master.service.type=LoadBalancer \  
       --set worker.replicas=3  
   ```
2. Confirm Spark deployment:  
   ```bash
   kubectl get pods --all-namespaces  
   ```

### 3️⃣ Data Processing
1. Build and push the Spark Docker image:
   ```bash
   docker build -t spark-job .  
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 767397764346.dkr.ecr.us-east-1.amazonaws.com/spark-repo  
   docker push 767397764346.dkr.ecr.us-east-1.amazonaws.com/spark-repo:latest  
   ```
2. Submit the Spark job:
   ```bash
   kubectl apply -f spark-logs-transform.yaml  
   kubectl logs -f <spark-job-pod>  
   ```

---

## 🔍 Running Analytics Queries

1. Access Spark SQL:  
   ```bash
   kubectl exec -it <spark-driver-pod> -- spark-sql  
   ```
2. Execute the following queries:  

   - **Top 5 IPs by Request Count (Daily)**:
     ```sql
      SELECT ip, COUNT(*) AS request_count
     FROM my_catalog.db_logs
     GROUP BY ip
     ORDER BY request_count DESC
     LIMIT 5;
     ```

   - **Top 5 Devices by Request Count (Daily)**:
     ```sql
      SELECT device_type, COUNT(*) AS request_count
     FROM my_catalog.db_logs
     GROUP BY device_type
     ORDER BY request_count DESC
     LIMIT 5
     ```

   - **Top 5 Devices (Weekly)**:
     ```sql
     SELECT device_type, COUNT(*) AS device_count, WEEK(datetime) AS week
     FROM my_catalog.db_logs
     GROUP BY device_type, week
     ORDER BY week DESC, device_count DESC
     LIMIT 5;
     ```

   - **Top 5 IP Addresses by Request Count (Weekly)**:
     ```sql
     SELECT ip, COUNT(*) AS request_count, WEEKOFYEAR(datetime) AS week
     FROM my_catalog.db_logs
     GROUP BY ip, week
     ORDER BY week DESC, request_count DESC
     LIMIT 5
     ```

---

## 🔍 Observability and Scaling

### Observability
- Monitor Spark jobs using the **Spark UI**.
- Collect performance metrics using Kubernetes logs and metrics-server.

### Scaling
- Increase the EKS cluster's node count for larger workloads:
  ```bash
  terraform apply -var="node_count=5"
  ```
- Optimize Spark configurations for better parallelism and memory allocation.

---

## 🔧 Assumptions and Challenges

### Assumptions:
- Hive Metastore is used as the Iceberg catalog backend.
- Logs are structured as shown in the example dataset.

### Challenges:
- Configuring RDS inbound rules to allow external connections.
- Debugging Spark job failures in Kubernetes pods.

---

## 📊 Performance Insights
The pipeline ensures efficient querying and supports scaling with:  
- Partitioning by date for faster query performance.  
- Iceberg's metadata capabilities for optimized data retrieval.  

---

## 💡 Conclusion

This project showcases a production-grade data engineering pipeline, leveraging modern tools like Iceberg and Spark. It provides robust analytics capabilities while ensuring scalability and performance.

