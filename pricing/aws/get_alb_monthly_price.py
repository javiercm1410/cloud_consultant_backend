import boto3
import json


# Create a Session object that uses the 'default' profile in the ~/.aws/credentials file
session = boto3.Session(profile_name='admin', region_name='us-east-1')

def get_alb_monthly_price(region, elbType, usageType):
    # Get the ALB product code
    pricing_client = session.client('pricing', region_name='us-east-1')
    response = pricing_client.get_products(
        ServiceCode='AWSELB',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Load Balancer-Application'},
            # There are two ELB usage type that we can request: LoadBalancerUsage and LCUUsage (LoadBalancerUnits)
            {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': usageType},
            {'Type': 'TERM_MATCH', 'Field': 'operation', 'Value': elbType},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region}
        ]
    )

    product = response['PriceList'][0]
    alb_product = json.loads(product)

    # Get the monthly price for the ALB
    hourly_price = None
    for term in alb_product['terms']['OnDemand'].values():
        hourly_price_dimensions = term['priceDimensions'].values()
        hourly_price = list(hourly_price_dimensions)[0]['pricePerUnit']['USD']
        break

    monthly_price = round(float(hourly_price) * 730, 2)
    return monthly_price
