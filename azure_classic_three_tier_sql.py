from diagram_as_code.aws.three_tier_classic_aws import aws_classic_three_tier_sql_diagram
from pricing.aws.get_ec2_monthly_price import get_ec2_monthly_price
from pricing.aws.get_ebs_monthly_price import get_ebs_monthly_price
from pricing.aws.get_alb_monthly_price import get_alb_monthly_price
from pricing.aws.get_rds_mysql_monthly_price import get_rds_mysql_monthly_price
from pricing.aws.get_client_vpn_connection_monthly_price import get_client_vpn_connection_monthly_price
from pricing.aws.get_client_vpn_endpoint_monthly_price import get_client_vpn_endpoint_monthly_price
from os_path import get_current_dir

def aws_classic_three_tier_sql(workload, auto_scale, region):
    prices = {}
    print("here")
    current_dir = get_current_dir()
    
    diagram_path = aws_classic_three_tier_sql_diagram(auto_scale, current_dir)
    if workload == "Low":
        instance_type = "t2.small"
    elif workload == "Medium":
        instance_type = "t2.medium"
    else:
        instance_type = "t2.large"
    prices["EC2"] = get_ec2_monthly_price(region, instance_type)
    prices["EBS"] = get_ebs_monthly_price(region, "gp2", 30)
    # There are two ELB usage type that we can request: LoadBalancerUsage and LCUUsage (LoadBalancerUnits)
    prices["ALB"] = get_alb_monthly_price(region, "LoadBalancing:Application", "LCUUsage")
    + get_alb_monthly_price(region, "LoadBalancing:Application", "LoadBalancerUsage")
    prices["Client_VPN"] = get_client_vpn_connection_monthly_price(region, 
                                                                        connections=1, 
                                                                        hoursPerDay=8, 
                                                                        workingDays=22) 
    + get_client_vpn_endpoint_monthly_price(region, 
                                            subnetAssociations=2)
    prices["RDS_MySQL"] = get_rds_mysql_monthly_price(region, 
                                                           instanceType='db.t3.micro', 
                                                           databaseEngine='MySQL',
                                                           deploymentOption='Single-AZ')
    return prices, diagram_path


prices, diagram_path = aws_classic_three_tier_sql("Medium", "No", "US East (N. Virginia)")
print(prices)
print(diagram_path)