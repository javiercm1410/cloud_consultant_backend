#!/usr/bin/env python3
import requests
import json

def get_managed_disk_monthly_price(region, tier, disk_size):
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{region}' and serviceName eq 'Storage' and contains(productName, '{tier}') and skuName eq '{disk_size}'"
    response = requests.get(api_url, params={'$filter': query})
    
    if response.status_code != 200:
        print(f"Error: La API devolvió un código de estado {response.status_code}")
        return
    
    json_data = json.loads(response.text)
    
    disk_cost_item = json_data["Items"][0]["retailPrice"]
            
    if disk_cost_item:
        return round(disk_cost_item, 2)
        

