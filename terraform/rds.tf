resource "aws_db_instance" "data_warehouse" {
  allocated_storage   = 10
  engine              = "postgres"
  engine_version      = "11.5"
  identifier          = "henry"
  instance_class      = "db.t2.micro"
  username            = "henry"
  password            = "henry123"
  skip_final_snapshot = true
  publicly_accessible = true
  apply_immediately   = true
  db_subnet_group_name = aws_db_subnet_group.subnet.name
  vpc_security_group_ids = [aws_security_group.rds.id]
}