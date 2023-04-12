#!/usr/bin/env python3
import requests
import json

def get_managed_disk_monthly_price(region, tier, disk_size):
    #try:
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{region}' and serviceName eq 'Storage' and contains(productName, '{tier}') and skuName eq '{disk_size}'"
    response = requests.get(api_url, params={'$filter': query})
    
    if response.status_code != 200:
        print(f"Error: La API devolvió un código de estado {response.status_code}")
        return
    
    json_data = json.loads(response.text)
    
    disk_cost_item = json_data["Items"][0]["retailPrice"]
            
    if disk_cost_item:
        return disk_cost_item
        
    # else:
    #     print("No se encontraron precios para la combinación de región, tier y disk size especificados.")
    
    # except requests.exceptions.RequestException as e:
    #     print(f"Error en la solicitud: {e}")
    # except json.JSONDecodeError as e:
    #     print(f"Error al decodificar la respuesta JSON: {e}")
    # except Exception as e:
    #     print(f"Error inesperado: {e}")

# Ejemplo de uso
## region = "eastus"
# tier = "Standard SSD"
# disk_size = "E4 LRS"
# print(get_managed_disk_monthly_price(region, tier, disk_size))
