variable "db_name" {
  description = "The name of the database"
  type        = string
}

variable "username" {
  description = "Master username for the RDS instance"
  type        = string
}

variable "password" {
  description = "Master password for the RDS instance"
  type        = string
}

variable "allocated_storage" {
  description = "The size of the database (in GB)"
  type        = number
  default     = 20
}

variable "engine" {
  description = "The database engine (e.g., mysql, postgres)"
  type        = string
  default     = "mysql"
}

variable "instance_class" {
  description = "The instance type for the RDS"
  type        = string
  default     = "db.t2.micro"
}

variable "environment" {
  description = "The environment for the RDS instance (e.g., dev, prod)"
  type        = string
  default     = "dev"
}