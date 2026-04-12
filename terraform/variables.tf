variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro" # Using t3.micro to comply with AWS Free Tier constraints
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = "eventhive-new-key"
}
