from diagram_as_code.gcp.container_based_architecture import gcp_container_architecture
from pricing.gcp.get_cloud_run_monthly_price import get_cloud_run_prices
from pricing.gcp.get_lb_monthly_price import get_load_balancing_price
from pricing.gcp.get_cloud_sql_monthly_price import get_cloud_sql_price
import json
import base64


def gcp_container_three_tier_sql(workload, auto_scale, region, working_dir):
# def get_fargate_monthly_price(region, operating_system, architecture, pods_number, average_duration_in_mins, vcpu_number, memory_number_in_gb, storage_number_in_gb):

    prices = {}
    diagram_path = gcp_container_architecture(auto_scale, working_dir)
    if workload == "Low":
        request_per_month = 144000
        number_of_instances = 1
        cpu = 2
        ram = 2
    elif workload == "Medium":
        request_per_month = 1440000
        number_of_instances = 2
        cpu = 4
        ram = 4
    else:
        request_per_month = 14400000
        number_of_instances = 3
        cpu = 8
        ram = 8

    prices["Cloud_Run"] = get_cloud_run_prices(request_per_month, number_of_instances, cpu, ram, region)
    # prices["Load_Balancing"] = get_load_balancing_price(2, region)
    prices["Cloud_SQL"] = get_cloud_sql_price("db-standard-1", 10, region)

    # Read the image file as binary data
    with open(diagram_path, "rb") as image_file:
        image_data = image_file.read()

    # Encode the binary data as a base64 string
    base64_image = base64.b64encode(image_data).decode('utf-8')

    output = {
        "imageBase64": base64_image,
        "data": prices,
    }

    return output
    # return prices, diagram_path
    # return prices, diagram_path



# output = aws_container_three_tier_sql("High", "US East (N. Virginia)")
# print(output)
# print(f"Diagram's path: {diagram_path}")
