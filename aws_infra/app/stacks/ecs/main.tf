resource "aws_ecs_cluster" "main" {
  name = "fastapi-cluster"
}

resource "aws_ecs_task_definition" "fastapi" {
  family                   = "fastapi-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  memory                   = "512"
  cpu                      = "256"
  execution_role_arn       = <%= output('iam.ecs_task_execution_role_arn') %>

  container_definitions = jsonencode([
    {
      name      = "fastapi"
      image     = "${<%= output('ecr.repository_url') %>}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "fastapi" {
  name            = "fastapi-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.fastapi.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = <%= output('vpc.private_subnets') %>
    security_groups  = [<%= output('alb.alb_security_group_id') %>]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = <%= output('alb.alb_target_group_arn') %>
    container_name   = "fastapi"
    container_port   = 80
  }
}
