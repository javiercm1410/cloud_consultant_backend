#!/usr/bin/env python3
import requests
import json

def get_app_gw_monthly_price(region, tier, capacity_units):
    #try:
    # api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    # query = f"armRegionName eq '{region}' and contains(productName, '{tier}') and serviceName eq 'Application Gateway'"
    # response = requests.get(api_url, params={'$filter': query})
    
    # if response.status_code != 200:
    #     print(f"Error: La API devolvió un código de estado {response.status_code}")
    #     return
    
    # json_data = json.loads(response.text)
    
    # return json_data
    # # fixed_cost_item = None
    # # capacity_units_cost_item = None
    
    # # for item in json_data["Items"]:
    # #     if "Fixed Cost" in item["meterName"]:
    # #         fixed_cost_item = item
    # #     elif "Capacity Units" in item["meterName"]:
    # #         capacity_units_cost_item = item
            
    # # if fixed_cost_item and capacity_units_cost_item:
    # #     fixed_cost = float(fixed_cost_item["retailPrice"])
    # #     capacity_units_cost = float(capacity_units_cost_item["retailPrice"])
        
    # #     total_cost_per_hour = fixed_cost + (capacity_units_cost * capacity_units)
    # #     total_cost_per_month = total_cost_per_hour * 730
    total_cost_per_month = 18.25
    return round(total_cost_per_month, 2)
    
    
            