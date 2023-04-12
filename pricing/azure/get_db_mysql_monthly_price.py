#!/usr/bin/env python3
import requests
import json

def get_mysql_database_price(region, performance_tier, vcore):
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{region}' and contains(serviceName,'Database')"  #and contains(skuName, '{performance_tier}') and contains(skuName, '{vcore} vCore')"
    response = requests.get(api_url, params={'$filter': query})
    
    if response.status_code != 200:
        print(f"Error: La API devolvió un código de estado {response.status_code}")
        return
    
    json_data = json.loads(response.text)
    with open('prices-mysql-db.json', 'w') as outfile:
        json.dump(json_data, outfile)
    
    mysql_db_cost_item = None
    
    for item in json_data["Items"]:
        if "vCore" in item["meterName"]:
            mysql_db_cost_item = item
            break
            
    if mysql_db_cost_item:
        mysql_db_cost = float(mysql_db_cost_item["retailPrice"])
        total_cost_per_hour = mysql_db_cost
        total_cost_per_month = total_cost_per_hour * 730
        return total_cost_per_month

region = "eastus"
performance_tier = "General Purpose"  # You can also use "Basic" or "Memory Optimized"
vcore = 2  # The number of vCores
print(get_mysql_database_price(region, performance_tier, vcore))