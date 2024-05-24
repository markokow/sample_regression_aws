output "alb_dns_name" {
  description = "The DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "alb_security_group_id" {
  description = "The ID of the ALB security group"
  value       = aws_security_group.alb_sg.id
}

output "alb_target_group_arn" {
  description = "The ARN of the ALB target group"
  value       = aws_lb_target_group.fastapi.arn
}
