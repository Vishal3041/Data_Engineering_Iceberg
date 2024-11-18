provider "aws" {
  region     = "us-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
}

# Create S3 bucket (S3 is global, but you can reference VPC for the required networking if needed)
module "s3" {
  source      = "./modules/s3"
  bucket_name = "log-dataset-bucket"
  environment = "dev"
}

# Create RDS instance in the default VPC using the DB subnet group
resource "aws_db_instance" "db_instance" {
  allocated_storage = 20
  engine            = "mysql"
  instance_class    = "db.t4g.micro"
  username          = "admin"
  password          = "admin123" # Avoid hardcoding in production; use Terraform secrets or AWS Secrets Manager.
  db_name           = "LogsDB"
}


# Create EKS Cluster in the default VPC and subnets
module "eks" {
  source               = "./modules/eks"
  cluster_name         = "my-eks-cluster"
  cluster_role_arn     = "arn:aws:iam::767397764346:role/Eks-Cluster-Role"     # Replace with actual ARN
  worker_node_role_arn = "arn:aws:iam::767397764346:role/Eks-Worker-Node-Role" # Replace with actual ARN
  desired_size         = 2
  min_size             = 1
  max_size             = 3
  subnet_ids           = ["subnet-021267b66463bc389", "subnet-09e900991d128968d"]
}