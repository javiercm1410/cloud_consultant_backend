import requests
import json

def get_aci_monthly_price(region, pods_number, average_duration_in_hours, vcpu_number, memory_number_in_gb):
    # try:
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{region}' and serviceName eq 'Container Instances' and skuName eq 'Standard' and productName eq 'Container Instances' "
    response = requests.get(api_url, params={'$filter': query})
    
    if response.status_code != 200:
        print(f"Error: La API devolvió un código de estado {response.status_code}")
        return
    
    json_data = json.loads(response.text)
    # with open('prices-aci.json', 'w') as outfile:
    #    json.dump(json_data, outfile)
    
    # aci_cost_item = None
    
    for item in json_data["Items"]:
        if "Standard Memory Duration" in item["meterName"]:
            memory_duration_cost = item
        elif "Standard vCPU Duration" in item["meterName"]:
            vcpu_duration_cost = item
     
    if memory_duration_cost and vcpu_duration_cost:
        memory_duration_cost = float(memory_duration_cost["retailPrice"])
        vcpu_duration_cost = float(vcpu_duration_cost["retailPrice"])
    memory_cost = memory_number_in_gb * pods_number * average_duration_in_hours * memory_duration_cost
    vcpu_cost = vcpu_number * pods_number * average_duration_in_hours * vcpu_duration_cost
    aci_total_cost = round(memory_cost + vcpu_cost, 2)
    
    return aci_total_cost

# #region = "eastus"
# pods_number = 6
# average_duration_in_hours = 1
# vcpu_number = 3
# memory_number_in_gb = 4
# print(get_aci_monthly_price(region, pods_number, average_duration_in_hours, vcpu_number, memory_number_in_gb))
