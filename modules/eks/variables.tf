variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "cluster_role_arn" {
  description = "The ARN of the IAM role for the EKS cluster control plane"
  type        = string
}

variable "worker_node_role_arn" {
  description = "The ARN of the IAM role for EKS worker nodes"
  type        = string
}

variable "subnet_ids" {
  description = "The subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "desired_size" {
  description = "Desired size of the EKS node group"
  type        = number
}

variable "min_size" {
  description = "Minimum size of the EKS node group"
  type        = number
}

variable "max_size" {
  description = "Maximum size of the EKS node group"
  type        = number
}