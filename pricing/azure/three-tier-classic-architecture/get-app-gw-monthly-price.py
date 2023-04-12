#!/usr/bin/env python3
import requests
import json

def get_application_gateway_price(region, tier, capacity_units):
    try:
        api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
        query = f"armRegionName eq '{region}' and contains(productName, '{tier}') and serviceName eq 'Application Gateway'"
        response = requests.get(api_url, params={'$filter': query})
        
        if response.status_code != 200:
            print(f"Error: La API devolvió un código de estado {response.status_code}")
            return
        
        json_data = json.loads(response.text)
        with open('prices-gw.json', 'w') as outfile:
            json.dump(json_data, outfile)
            
        fixed_cost_item = None
        capacity_units_cost_item = None
        
        for item in json_data["Items"]:
            if "Fixed Cost" in item["meterName"]:
                fixed_cost_item = item
            elif "Capacity Units" in item["meterName"]:
                capacity_units_cost_item = item
                
        if fixed_cost_item and capacity_units_cost_item:
            fixed_cost = float(fixed_cost_item["retailPrice"])
            capacity_units_cost = float(capacity_units_cost_item["retailPrice"])
            
            total_cost_per_hour = fixed_cost + (capacity_units_cost * capacity_units)
            total_cost_per_month = total_cost_per_hour * 730
            
            print(f"Precio por hora: ${total_cost_per_hour:.3f}")
            print(f"Precio mensual: ${total_cost_per_month:.3f}")
            
        else:
            print("No se encontraron precios para la combinación de región, tier, tamaño y datos procesados especificados.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ejemplo de uso
region = "eastus"
tier = "Standard v2"
capacity_units = 5
get_application_gateway_price(region, tier, capacity_units)
