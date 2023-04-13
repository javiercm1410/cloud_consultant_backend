# import boto3
# import json

# session = boto3.Session(profile_name='admin', region_name='us-east-1')

# def get_fargate_monthly_price(region, operating_system, architecture, pods_number, vcpu_number, average_duration):
#     pricing_client = session.client('pricing', region_name='us-east-1')
    
#     response = pricing_client.get_products(
#         ServiceCode='AmazonECS',
#         Filters=[
#             {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
#            # {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': operating_system},
#             #{'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'Used'},
#             #{'Type': 'TERM_MATCH', 'Field': 'ecs:ComputeFamily', 'Value': 'Fargate'},
#             #{'Type': 'TERM_MATCH', 'Field': 'architecture', 'Value': architecture},
#         ]
#     )

#     product = response['PriceList'][0]
#     fargate_product = json.loads(product)
#     with open('fargate_product.json', 'w') as f:
#         json.dump(fargate_product, f, indent=4)
#     vcpu_hourly_price = None
#     memory_hourly_price = None
#     for term in fargate_product['terms']['OnDemand'].values():
#         price_dimensions = term['priceDimensions'].values()
#         for dimension in price_dimensions:
#             if 'vCPU' in dimension['description']:
#                 vcpu_hourly_price = float(dimension['pricePerUnit']['USD'])
#             elif 'GB' in dimension['description']:
#                 memory_hourly_price = float(dimension['pricePerUnit']['USD'])

#     vcpu_monthly_price = vcpu_hourly_price * vcpu_number * average_duration * 30
#     memory_monthly_price = memory_hourly_price * pods_number * average_duration * 30
#     total_monthly_price = round(vcpu_monthly_price + memory_monthly_price, 2)

#     return total_monthly_price

## region = "US East (N. Virginia)"
# operating_system = "Linux"
# architecture = "x86"
# pods_number = 10
# vcpu_number = 2
# average_duration = 12  # in hours

# monthly_price = get_fargate_monthly_price(region, operating_system, architecture, pods_number, vcpu_number, average_duration)
# print(f"Fargate Monthly Price: ${monthly_price}")


def get_fargate_monthly_price(region, operating_system, architecture, pods_number, average_duration_in_mins, vcpu_number, memory_number_in_gb, storage_number_in_gb):
    pods_number = round(pods_number * (730/24), 2)
    average_duration_in_hours = round(average_duration_in_mins / 60, 2)
    cost_vcpu_hourly = round(pods_number * vcpu_number * average_duration_in_hours * 0.04048, 2)
    cost__memory_gb_hourly = round(pods_number * memory_number_in_gb * average_duration_in_hours * 0.004445, 2)
    cost_storage_gb_hourly = round(pods_number * (storage_number_in_gb - 20) * average_duration_in_hours * 0.000111, 2)
    total_cost =cost_vcpu_hourly + cost__memory_gb_hourly + cost_storage_gb_hourly
    return total_cost


# print(get_fargate_monthly_price("US East (N. Virginia)", "Linux", "x86", 10, 10, 2, 4, 50))