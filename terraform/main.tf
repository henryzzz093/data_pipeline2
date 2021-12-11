resource "aws_s3_bucket" "datalake" {
  bucket = "data-pipeline-datalake-henry"
  acl    = "private"

  force_destroy = true

  lifecycle {
    prevent_destroy = false
  }
}