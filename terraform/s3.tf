# Creating multiple s3 buckets

resource "aws_s3_bucket" "datalake" {
  
  bucket = "data-pipeline-datalake-henry"
  acl    = "private"
  force_destroy = true

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket" "public_s3" {
  
  bucket = "data-pipeline-public-s3"
  acl    = "public-read"
  force_destroy = true

  lifecycle {
    prevent_destroy = false
  }
}

