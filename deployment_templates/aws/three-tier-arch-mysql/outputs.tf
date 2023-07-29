output "web_load_balancer_dns_name" {
  value = aws_lb.cc-web-alb.dns_name

}

output "app_load_balancer_dns_name" {
  value = aws_lb.cc-app-alb.dns_name
}

output "rds_mysql_endpoint" {
  value = aws_db_instance.cc-rds-mysql.endpoint
}

output "rds_mysql_master_username" {
  value = aws_db_instance.cc-rds-mysql.username
}