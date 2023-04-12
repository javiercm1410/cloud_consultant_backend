import requests
import json

def get_vm_price(api_key, vcpus, memory_gb, region):
    url = f"https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus?key={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching pricing data:", response.status_code, response.text)
        return

    pricing_data = response.json()

    with open('prices-vm-gcp.json', 'w') as outfile:
        json.dump(pricing_data, outfile)

    for sku in pricing_data['skus']:
        if sku['category']['resourceFamily'] == 'Compute' and sku['category']['usageType'] == 'OnDemand':
            # Check if the region matches
            if region in sku['serviceRegions']:
                
                # Check for the desired number of vCPUs
                if f"{vcpus} VCPU" in sku['description']:
                    # Check for the desired amount of memory
                    if f"{memory_gb} GB RAM" in sku['description'] or f"{memory_gb:.2f} GB RAM" in sku['description']:
                        price_per_hour = float(sku['pricingInfo'][0]['pricingExpression']['tieredRates'][0]['unitPrice']['nanos']) / 1e9
                        hours_per_month = 730
                        monthly_price = price_per_hour * hours_per_month
                        print(f"Estimated monthly price for {vcpus} vCPUs and {memory_gb}GB RAM VM in {region}: ${monthly_price:.2f}")
                        break

api_key = "AIzaSyAPll7_sm0cPFqrZ4yABfUYIPady97ZTYo"
vcpus = 1
memory_gb = 2
region = "us-east1"
get_vm_price(api_key, vcpus, memory_gb, region)
