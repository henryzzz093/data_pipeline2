terraform {
  backend "s3" {
    profile = "terraform"
    bucket  = "terraform-henry"
    key     = "data-piplines/tf.state"
    region  = "us-west-2"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
}