output "instance_public_ip" {
  description = "Public IP of EC2 instance"
  value       = aws_instance.ps5_bot.public_ip
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh -i <your-private-key.pem> ubuntu@${aws_instance.ps5_bot.public_ip}"
}

