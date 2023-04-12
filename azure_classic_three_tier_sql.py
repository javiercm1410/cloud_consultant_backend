from diagram_as_code.azure.three_tier_classic_azure import azure_classic_three_tier_sql_diagram
from pricing.azure.get_vm_monthly_price import get_vm_monthly_price
from pricing.azure.get_managed_disk_monthly_price import get_managed_disk_monthly_price
from pricing.azure.get_app_gw_monthly_price import get_app_gw_monthly_price
from pricing.azure.get_vpn_gw_monthly_price import get_vpn_gw_monthly_price
# from pricing.azure.get_client_vpn_connection_monthly_price import get_client_vpn_connection_monthly_price
# from pricing.azure.get_client_vpn_endpoint_monthly_price import get_client_vpn_endpoint_monthly_price

def azure_classic_three_tier_sql(workload, auto_scale, region):
    prices = {}
    
    diagram_path = azure_classic_three_tier_sql_diagram(auto_scale)
    if workload == "Low":
        vm_type = "A1 v2"
    elif workload == "Medium":
        vm_type = "A2 v2"
    else:
        vm_type = "D2as v5"
    prices["VM"] = get_vm_monthly_price(region, vm_type)
    prices["Managed_disk"] = get_managed_disk_monthly_price(region, "Standard SSD", "E4 LRS") #E4 32GB
    # There are two ELB usage type that we can request: LoadBalancerUsage and LCUUsage (LoadBalancerUnits)
    prices["App_Gateway"] = get_app_gw_monthly_price(region, "Standard v2", 5)
    prices["Client_VPN"] = get_vpn_gw_monthly_price(region, "VpnGw1") 
    # prices["RDS_MySQL"] = get_rds_mysql_monthly_price(region, 
    #                                                        instanceType='db.t3.micro', 
    #                                                        databaseEngine='MySQL',
    #                                                        deploymentOption='Single-AZ')
    
    return prices, diagram_path


prices, diagram_path = azure_classic_three_tier_sql("Medium", "No", "US East (N. Virginia)")
print(prices)
print(diagram_path)