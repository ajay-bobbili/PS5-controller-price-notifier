variable "aws_region" {
  description = "AWS Region"
  default     = "ap-south-1"   # Mumbai region
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"    # Free tier eligible
}

variable "key_name" {
  description = "Name of the SSH key pair"
}

variable "public_key_path" {
  description = "Path to your public key"
  default     = "~/.ssh/id_rsa.pub"
}
