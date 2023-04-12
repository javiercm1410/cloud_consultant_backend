#!/usr/bin/env python3
import requests
import json

def get_vpn_gateway_price(region, gateway_type, vpn_gateway_type):
    try:
        api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
        query = f"armRegionName eq '{region}' and serviceName eq 'VPN Gateway' and contains(skuName, '{vpn_gateway_type}') and contains(productName, '{gateway_type}')"
        response = requests.get(api_url, params={'$filter': query})
        
        if response.status_code != 200:
            print(f"Error: La API devolvió un código de estado {response.status_code}")
            return
        
        json_data = json.loads(response.text)
        with open('prices-vpn-gw.json', 'w') as outfile:
            json.dump(json_data, outfile)
            
        gateway_cost_item = None
        
        for item in json_data["Items"]:
            if "Data Transfer" not in item["meterName"]:
                gateway_cost_item = item
                break
                
        if gateway_cost_item:
            gateway_cost = float(gateway_cost_item["retailPrice"])
            total_cost_per_hour = gateway_cost
            total_cost_per_month = total_cost_per_hour * 730
            
            print(f"Precio por hora: ${total_cost_per_hour:.3f}")
            print(f"Precio mensual: ${total_cost_per_month:.3f}")
            
        else:
            print("No se encontraron precios para la combinación de región, gateway type y VPN gateway type especificados.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ejemplo de uso
region = "eastus"
gateway_type = "VPN Gateways"
vpn_gateway_type = "VPN"
get_vpn_gateway_price(region, gateway_type, vpn_gateway_type)
