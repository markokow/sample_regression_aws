# This is where you put your resource declaration
module "private_ecr" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name         = "exercise_ecr"
  repository_force_delete = true
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 10 images",
        selection = {
          tagStatus   = "untagged",
          countType   = "imageCountMoreThan",
          countNumber = 10
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
  repository_image_tag_mutability = "MUTABLE"
}

resource "null_resource" "docker_push" {
  provisioner "local-exec" {
    environment = {
      ECR_REPOSITORY_URL = "${module.private_ecr.repository_url}"
      AWS_ACCESS_KEY_ID     = <%= output('iam.iam_user_access_key_id') %>
      AWS_SECRET_ACCESS_KEY = <%= output('iam.iam_user_secret_access_key') %>
    }
    command = <<EOT
    aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin $ECR_REPOSITORY_URL
    docker build -t $ECR_REPOSITORY_URL:latest -f "../../../../../Dockerfile" "../../../../../"
    docker push $ECR_REPOSITORY_URL:latest
    EOT
  }
}
