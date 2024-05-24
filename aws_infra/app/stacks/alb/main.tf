# This is where you put your resource declaration
resource "aws_security_group" "alb_sg" {
  name        = "alb_sg"
  description = "Allow inbound HTTP traffic"
  vpc_id      =  <%= output('vpc.vpc_id') %>

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "main" {
  name               = "fastapi-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            =  <%= output('vpc.public_subnets') %>
}

resource "aws_lb_target_group" "fastapi" {
  name     = "fastapi-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = <%= output('vpc.vpc_id') %>
  target_type = "ip"
  depends_on = [aws_lb.main]
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.fastapi.arn
  }
  depends_on = [aws_lb_target_group.fastapi]
}
