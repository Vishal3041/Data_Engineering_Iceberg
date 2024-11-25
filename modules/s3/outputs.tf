output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.log_files_bucket.bucket
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.log_files_bucket.arn
}