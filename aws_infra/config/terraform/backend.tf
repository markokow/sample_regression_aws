# This file was initially generated by terraspace_plugin_aws 0.6.1
# Backend Config Variables Docs
# https://terraspace.cloud/docs/config/backend/variables/
# terraform {
#   backend "s3" {
#     bucket         = "<%= expansion('terraform-state-:ACCOUNT-:REGION-:ENV') %>"
#     key            = "<%= expansion(':PROJECT/:REGION/:APP/:ROLE/:ENV/:EXTRA/:BUILD_DIR/terraform.tfstate') %>"
#     region         = "<%= expansion(':REGION') %>"
#     dynamodb_table = "terraform_locks"
#   }
# }