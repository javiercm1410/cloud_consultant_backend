from diagram_as_code.azure.three_tier_classic_azure import azure_classic_three_tier_sql_diagram
from pricing.azure.get_vm_monthly_price import get_vm_monthly_price
from pricing.azure.get_managed_disk_monthly_price import get_managed_disk_monthly_price
from pricing.azure.get_app_gw_monthly_price import get_app_gw_monthly_price
# from pricing.azure.get_vpn_gw_monthly_price import get_vpn_gw_monthly_price
from pricing.azure.get_db_mysql_monthly_price import get_mysql_database_price
import json
import base64

def azure_classic_three_tier_sql(workload, auto_scale, region, working_dir):
    prices = {}
        
    diagram_path = azure_classic_three_tier_sql_diagram(auto_scale, working_dir)
    if workload == "Low":
        vm_type = "A1 v2" # 1 vCPU, 2GB RAM
    elif workload == "Medium":
        vm_type = "A2 v2" # 2 vCPU, 4GB RAM
    else:
        vm_type = "D2s v3" #2 vCPU, 8GB RAM
    prices["VM"] = get_vm_monthly_price(region, vm_type)*2 + get_managed_disk_monthly_price(region, "Standard SSD", "E4 LRS")*2 
    # There are two ELB usage type that we can request: LoadBalancerUsage and LCUUsage (LoadBalancerUnits)
    prices["App_Gateway"] = get_app_gw_monthly_price(region, "Standard v2", 5)*2
    # prices["VPN_Gateway"] = get_vpn_gw_monthly_price(region, "VpnGw1") 
    prices["Azure_Database_MySQL"] = get_mysql_database_price(region, 
                                                              deployment_option="Flexible Server", 
                                                              tier="Burstable", 
                                                              compute_sku="Basic", 
                                                              storage=10)*2
    
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


# output = azure_classic_three_tier_sql("High", "Yes", "eastus")
# print(output)
