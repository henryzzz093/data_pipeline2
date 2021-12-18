resource "aws_db_instance" "data_warehouse" {
  allocated_storage   = 10
  engine              = "postgres"
  engine_version      = "11.5"
  identifier          = "henry"
  instance_class      = "db.t2.micro"
  username            = ""
  password            = ""
  skip_final_snapshot = true
  publicly_accessible = true
  apply_immediately   = true
}