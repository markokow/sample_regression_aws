# This is where you put your resource declaration
module "iam_user1" {
  source                        = "terraform-aws-modules/iam/aws//modules/iam-user"
  name                          = "test1"
  force_destroy                 = true
  create_iam_user_login_profile = false
  create_iam_access_key         = true
}

module "iaws_iam_policy_documentam_group_with_policies" {
  source = "terraform-aws-modules/iam/aws//modules/iam-group-with-policies"

  name = "ECRGroup"

  group_users = [
    module.iam_user1.iam_user_name
  ]
  attach_iam_self_management_policy = false
  custom_group_policies = [
    {
      name   = "AllowECRPushPull"
      policy = data.aws_iam_policy_document.ecr.json
    }
  ]
}

data "aws_iam_policy_document" "ecr" {
  statement {
    sid    = "AllowPushPull"
    effect = "Allow"
    actions = [
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:GetDownloadUrlForLayer",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
      "ecr:GetAuthorizationToken",
    ]
    resources = ["*"]
  }
}

module "ecs_task_execution_role" {
  source = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"

  create_role = true
  role_name   = "ecsTaskExecutionRole"

  trusted_role_services = [
    "ecs-tasks.amazonaws.com"
  ]

  custom_role_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  ]
}
