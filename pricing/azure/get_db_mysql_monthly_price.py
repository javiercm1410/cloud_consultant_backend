#!/usr/bin/env python3
import requests
import json

def get_mysql_database_price(region, deployment_option, tier, compute_sku, storage):
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{region}' and contains(serviceName,'Azure Database for MySQL') and contains(productName, '{deployment_option}') and contains(productName, '{tier}') and contains(skuName, '{compute_sku}')"
    response = requests.get(api_url, params={'$filter': query})
    
    if response.status_code != 200:
        print(f"Error: La API devolvió un código de estado {response.status_code}")
        return
    
    json_data = json.loads(response.text)
    mysql_db_cost_item  = json_data["Items"][0]["retailPrice"]

    
            
    if mysql_db_cost_item:
        storage *= 0.115
        total_cost_per_month = mysql_db_cost_item * 730 + storage 
        return round(total_cost_per_month, 2)

## region = "eastus"
# deployment_option = "Flexible Server"
# tier = "Burstable"  
# compute_sku = "Basic" 
# storage = 5
# print(get_mysql_database_price(region, deployment_option, tier, compute_sku, storage))