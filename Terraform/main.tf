# Create key pair
resource "aws_key_pair" "ps5_bot_key" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

# Security Group: SSH only
resource "aws_security_group" "ps5_bot_sg" {
  name        = "ps5_bot_sg"
  description = "Allow SSH inbound"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # restrict later if you want
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "ps5_bot_ec2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = aws_key_pair.ps5_bot_key.key_name
  vpc_security_group_ids = [aws_security_group.ps5_bot_sg.id]

  tags = {
    Name = "PS5PriceBot"
  }

  # Optional: User data to install Python and Git automatically
  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt install -y python3-pip git
              EOF
}

# Latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}