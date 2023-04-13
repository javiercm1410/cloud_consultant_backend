#!/usr/bin/env python3
import requests
import json

def get_vm_monthly_price(region, vm_type):
    #try:
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{region}' and skuName eq '{vm_type}' and priceType eq 'Consumption' and serviceName eq 'Virtual Machines'"
    response = requests.get(api_url, params={'$filter': query})
    
    if response.status_code != 200:
        print(f"Error: La API devolvió un código de estado {response.status_code}")
        return
    
    json_data = json.loads(response.text)
    
    non_windows_items = [item for item in json_data["Items"] if "Windows" not in item["productName"]]
    
    if len(non_windows_items) > 0:
        price_per_hour = float(non_windows_items[0]["retailPrice"])
        price_per_month = price_per_hour * 730
        
        return round(price_per_month, 2)

    #     else:
    #         print("No se encontraron precios para la combinación de región y tipo de VM especificados sin incluir Windows.")
    
    # except requests.exceptions.RequestException as e:
    #     print(f"Error en la solicitud: {e}")
    # except json.JSONDecodeError as e:
    #     print(f"Error al decodificar la respuesta JSON: {e}")
    # except Exception as e:
    #     print(f"Error inesperado: {e}")

# Ejemplo de uso
# #region = "eastus"
# vm_type = "D2s v3"
# print(get_vm_monthly_price(region, vm_type))
