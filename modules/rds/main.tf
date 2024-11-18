resource "aws_db_instance" "db_instance" {
  allocated_storage    = var.allocated_storage
  engine               = var.engine
  instance_class       = var.instance_class
  username             = var.username
  password             = var.password

  tags = {
    Name        = "RDS-${var.environment}" # Use environment for tagging
    Environment = var.environment
  }
}