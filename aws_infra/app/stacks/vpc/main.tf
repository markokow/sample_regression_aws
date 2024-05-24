# This is where you put your resource declaration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "vpc_sample"
  cidr = "10.0.0.0/16"

  azs             = ["ap-southeast-1a", "ap-southeast-1b"]
  private_subnets = ["10.0.0.0/24", "10.0.1.0/24"]
  public_subnets  = ["10.0.2.0/24", "10.0.3.0/24"]

  private_subnet_names = ["Private Subnet A", "Private Subnet B"]
  public_subnet_names  = ["Public Subnet A", "Public Subnet B"]

  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = true
}
