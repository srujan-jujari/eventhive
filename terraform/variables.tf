variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.medium" # k8s usually needs more than t2.micro
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = "eventhive-key"
}
