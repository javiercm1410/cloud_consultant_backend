from diagram_as_code.azure.container_based_architecture_azure import azure_container_based_architecture_diagram
from pricing.azure.get_aci_monthly_price import get_aci_monthly_price
from pricing.azure.get_app_gw_monthly_price import get_app_gw_monthly_price
from pricing.azure.get_vpn_gw_monthly_price import get_vpn_gw_monthly_price
from pricing.azure.get_db_mysql_monthly_price import get_mysql_database_price
import json
import base64
import os

def azure_container_based_architecture(workload, auto_scale, region, working_dir):
    prices = {}
    pods_number = 4
    average_duration_in_hours = 730
    vcpu_number = 2
    memory_number_in_gb = 8
    if workload == "Low":
         pods_number = 1
         average_duration_in_hours = 730
         vcpu_number = 1
         memory_number_in_gb = 2
    elif workload == "Medium":
         pods_number = 2
         average_duration_in_hours = 730
         vcpu_number = 2
         memory_number_in_gb = 4
    
         
         
    diagram_path = azure_container_based_architecture_diagram(working_dir)
    prices["Azure_Container_Instances"] = get_aci_monthly_price(region, pods_number, average_duration_in_hours, vcpu_number, memory_number_in_gb)
    prices["App_Gateway"] = get_app_gw_monthly_price(region, "Standard v2", 5)
    prices["VPN_Gateway"] = get_vpn_gw_monthly_price(region, "VpnGw1") 
    prices["Azure_Database_MySQL"] = get_mysql_database_price(region, 
                                                              deployment_option="Flexible Server", 
                                                              tier="Burstable", 
                                                              compute_sku="Basic", 
                                                              storage=5)
    
    # # Read the image file as binary data
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

# print(azure_container_based_architecture("High", "eastus", os.getcwd()))
