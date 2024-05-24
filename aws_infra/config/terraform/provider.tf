# Docs: https://www.terraform.io/docs/providers/aws/index.html
#
# If AWS_PROFILE and AWS_REGION is set, then the provider is optional.  Here's an example anyway:
#
# Configure the AWS Provider

provider "aws" {
  profile = "vscode" # or specify what profile you specically use that has IAM admin access
}
