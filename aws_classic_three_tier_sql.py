from diagram_as_code.aws.three_tier_classic_aws import aws_classic_three_tier_sql_diagram
from pricing.aws.get_ec2_monthly_price import get_ec2_monthly_price
from pricing.aws.get_ebs_monthly_price import get_ebs_monthly_price
from pricing.aws.get_alb_monthly_price import get_alb_monthly_price
from pricing.aws.get_rds_mysql_monthly_price import get_rds_mysql_monthly_price
# from pricing.aws.get_client_vpn_connection_monthly_price import get_client_vpn_connection_monthly_price
# from pricing.aws.get_client_vpn_endpoint_monthly_price import get_client_vpn_endpoint_monthly_price
import json
import base64


def aws_classic_three_tier_sql(workload, auto_scale, region, working_dir):
    prices = {}
    
    diagram_path = aws_classic_three_tier_sql_diagram(auto_scale, working_dir)
    if workload == "Low":
        instance_type = "t2.small" # 1 vCPU, 2GB RAM
    elif workload == "Medium":
        instance_type = "t2.medium" # 2 vCPU, 4GB RAM
    else:
        instance_type = "t2.large" #2 vCPU, 8GB RAM
    prices["EC2"] = get_ec2_monthly_price(region, instance_type)*2
    prices["EBS"] = get_ebs_monthly_price(region, "gp2", 20)*2
    # There are two ELB usage type that we can request: LoadBalancerUsage and LCUUsage (LoadBalancerUnits)
    prices["ALB"] = (get_alb_monthly_price(region, "LoadBalancing:Application", "LCUUsage", 0.8) + get_alb_monthly_price(region, "LoadBalancing:Application", "LoadBalancerUsage", None))*2
    # prices["Client_VPN"] = get_client_vpn_connection_monthly_price(region, 
    #                                                                     connections=1, 
    #                                                                     hoursPerDay=8, 
    #                                                                     workingDays=22) + get_client_vpn_endpoint_monthly_price(region, 
    #                                                                                                                             subnetAssociations=2)
    prices["RDS_MySQL"] = get_rds_mysql_monthly_price(region, 
                                                           instanceType="db.t3.small", 
                                                           databaseEngine='MySQL',
                                                           deploymentOption='Single-AZ', 
                                                           storage=100)*2

    # Read the image file as binary data
    with open(diagram_path, "rb") as image_file:
        image_data = image_file.read()

    # Encode the binary data as a base64 string
    base64_image = base64.b64encode(image_data).decode('utf-8')

    output = {
        "imageBase64": base64_image,
        "data": prices,
        # "terraformConfig": json.dumps(terraform_config, indent=2)
    }

    return output
    # return prices, diagram_path
    # return prices, diagram_path



# output = aws_classic_three_tier_sql("High", "No", "US East (N. Virginia)")
# print(output)
# print(f"Diagram's path: {diagram_path}")
