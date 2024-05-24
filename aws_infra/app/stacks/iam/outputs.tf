# This is where you put your outputs declaration
output "iam_user_access_key_id" {
  value     = module.iam_user1.iam_access_key_id
  sensitive = true
}

output "iam_user_secret_access_key" {
  value     = module.iam_user1.iam_access_key_secret
  sensitive = true
}

output "ecs_task_execution_role_arn" {
  description = "The ARN of the ECS Task Execution Role"
  value       = module.ecs_task_execution_role.iam_role_arn
}
