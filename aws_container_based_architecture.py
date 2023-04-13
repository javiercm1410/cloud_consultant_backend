from diagram_as_code.aws.container_based_architecture_aws import aws_container_based_architecture_diagram
from pricing.aws.get_fargate_monthly_price import get_fargate_monthly_price
from pricing.aws.get_alb_monthly_price import get_alb_monthly_price
from pricing.aws.get_rds_mysql_monthly_price import get_rds_mysql_monthly_price
from pricing.aws.get_client_vpn_connection_monthly_price import get_client_vpn_connection_monthly_price
from pricing.aws.get_client_vpn_endpoint_monthly_price import get_client_vpn_endpoint_monthly_price
import json
import base64


def aws_container_three_tier_sql(workload, region, working_dir):
# def get_fargate_monthly_price(region, operating_system, architecture, pods_number, average_duration_in_mins, vcpu_number, memory_number_in_gb, storage_number_in_gb):

    prices = {}
    if workload == "Low":
         pods_number = 1
         average_duration_in_mins = 3000
         vcpu_number = 1
         memory_number_in_gb = 2
    elif workload == "Medium":
         pods_number = 2
         average_duration_in_hours = 3000
         vcpu_number = 2
         memory_number_in_gb = 4
    else:
         pods_number = 4
         average_duration_in_hours = 3000
         vcpu_number = 2
         memory_number_in_gb = 8
    diagram_path = aws_container_based_architecture_diagram(working_dir)
    prices["Fargate"] = get_fargate_monthly_price(region, "Linux", "x86", pods_number, average_duration_in_mins, vcpu_number, memory_number_in_gb, storage_number_in_gb=20)
    # There are two ELB usage type that we can request: LoadBalancerUsage and LCUUsage (LoadBalancerUnits)
    prices["ALB"] = get_alb_monthly_price(region, "LoadBalancing:Application", "LCUUsage", 0.8) + get_alb_monthly_price(region, "LoadBalancing:Application", "LoadBalancerUsage", None)
    prices["Client_VPN"] = get_client_vpn_connection_monthly_price(region, 
                                                                        connections=1, 
                                                                        hoursPerDay=8, 
                                                                        workingDays=22) + get_client_vpn_endpoint_monthly_price(region, 
                                                                                                                                subnetAssociations=2)
    prices["RDS_MySQL"] = get_rds_mysql_monthly_price(region, 
                                                           instanceType='db.t3.micro', 
                                                           databaseEngine='MySQL',
                                                           deploymentOption='Single-AZ', 
                                                           storage=5)

    # Read the image file as binary data
    with open(diagram_path, "rb") as image_file:
        image_data = image_file.read()

    # Encode the binary data as a base64 string
    base64_image = base64.b64encode(image_data).decode('utf-8')

    output = {
        "imageBase64": base64_image,
        "data": prices,
    }

    return json.dumps(output, ensure_ascii=False)
    # return prices, diagram_path
    # return prices, diagram_path



# output = aws_container_three_tier_sql("High", "US East (N. Virginia)")
# print(output)
# print(f"Diagram's path: {diagram_path}")
