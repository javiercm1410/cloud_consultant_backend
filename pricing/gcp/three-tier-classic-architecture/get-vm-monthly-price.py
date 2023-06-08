# import requests
# import json

# def get_vm_price(api_key, vcpus, memory_gb, region):
#     url = f"https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus?key={api_key}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         print("Error fetching pricing data:", response.status_code, response.text)
#         return

#     pricing_data = response.json()

#     with open('prices-vm-gcp.json', 'w') as outfile:
#         json.dump(pricing_data, outfile)

#     for sku in pricing_data['skus']:
#         if sku['category']['resourceFamily'] == 'Compute' and sku['category']['usageType'] == 'OnDemand':
#             # Check if the region matches
#             if region in sku['serviceRegions']:
                
#                 # Check for the desired number of vCPUs
#                 if f"{vcpus} VCPU" in sku['description']:
#                     # Check for the desired amount of memory
#                     if f"{memory_gb} GB RAM" in sku['description'] or f"{memory_gb:.2f} GB RAM" in sku['description']:
#                         price_per_hour = float(sku['pricingInfo'][0]['pricingExpression']['tieredRates'][0]['unitPrice']['nanos']) / 1e9
#                         hours_per_month = 730
#                         monthly_price = price_per_hour * hours_per_month
#                         print(f"Estimated monthly price for {vcpus} vCPUs and {memory_gb}GB RAM VM in {region}: ${monthly_price:.2f}")
#                         break

# api_key = "AIzaSyAPll7_sm0cPFqrZ4yABfUYIPady97ZTYo"
# vcpus = 1
# memory_gb = 2
## region = "us-east1"
# get_vm_price(api_key, vcpus, memory_gb, region)
import requests
import json

def get_compute_engine_price(instance_type, region):
    # Define your API Key
    api_key = "AIzaSyAPll7_sm0cPFqrZ4yABfUYIPady97ZTYo"

    # Set the URL endpoint for listing public services
    services_url = f"https://cloudbilling.googleapis.com/v1/services?key={api_key}"

    try:
        # Send a GET request to the Cloud Billing Catalog API to get the list of services
        services_response = requests.get(services_url)
        services_data = json.loads(services_response.text)

        # Save services_data to a JSON file
        with open('services_data.json', 'w') as file:
            json.dump(services_data, file)

        # Find the compute engine service
        compute_engine_service = next((service for service in services_data["services"] if service["displayName"] == "Compute Engine"), None)
        if not compute_engine_service:
            print("Error: Compute Engine service not found")
            return None

        # Get the service ID for Compute Engine
        compute_engine_service_id = compute_engine_service["serviceId"]

        # Set the URL endpoint for listing SKUs for Compute Engine
        skus_url = f"https://cloudbilling.googleapis.com/v1/services/{compute_engine_service_id}/skus?key={api_key}"

        # Send a GET request to the Cloud Billing Catalog API to get the list of SKUs for Compute Engine
        skus_response = requests.get(skus_url)
        skus_data = json.loads(skus_response.text)

        # Find the SKU for the specified instance type and region
        for sku in skus_data.get("skus", []):
            description = sku.get("description", "")
            service_regions = sku.get("serviceRegions", [])
            if instance_type in description and region in service_regions:
                pricing_info = sku.get("pricingInfo", [{}])[0]
                price_rate = pricing_info.get("pricingExpression", {}).get("tieredRates", [{}])[0].get("unitPrice", {}).get("nanos", 0) / 1000000000
                start_usage_amount = pricing_info.get("pricingExpression", {}).get("tieredRates", [{}])[0].get("startUsageAmount", 0)
                return price_rate * 730 + start_usage_amount

        # If SKU not found, return None
        print(f"No pricing information found for {instance_type} in {region}.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
instance_type = "n1-standard-2"  # Specify the instance type
region = "us-central1"  # Specify the region

# Call the function to get the monthly price
price = get_compute_engine_price(instance_type, region)

# Check if the price is available
if price is not None:
    print(f"The monthly price for {instance_type} in {region} is: ${price:.2f}")
else:
    print(f"Could not find pricing information for {instance_type} in {region}.")
