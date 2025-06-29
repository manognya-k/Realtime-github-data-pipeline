provider "aws" {
  access_key = "mock"
  secret_key = "mock"
  region     = "us-east-1"
  
  endpoints {
    s3 = "http://localhost:4566"
  }
  
  skip_credentials_validation = true
  s3_use_path_style           = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
  
}


resource "aws_s3_bucket" "github_data" {
  bucket = "github-pipeline-bucket"
}