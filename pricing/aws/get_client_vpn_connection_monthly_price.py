import boto3
import json


# Create a Session object that uses the 'default' profile in the ~/.aws/credentials file
session = boto3.Session(profile_name='default', region_name='us-east-1')


def get_client_vpn_connection_monthly_price(region, connections, hoursPerDay, workingDays):
    pricing_client = session.client('pricing', region_name='us-east-1')
    response = pricing_client.get_products(
        ServiceCode='AmazonVPC',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'group', 'Value': 'AWSClientVPN'},
            # There are two ClientVPN usage type that we can request: Hourly charge for Client VPN connections, 
            # and Hourly charge for Client VPN Endpoints
            {'Type': 'TERM_MATCH', 'Field': 'groupDescription', 'Value': 'Hourly charge for Client VPN connections'},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region}
        ]
    )

    product = response['PriceList'][0]
    vpn_product = json.loads(product)

    hourly_price = None
    for term in vpn_product['terms']['OnDemand'].values():
        hourly_price_dimensions = term['priceDimensions'].values()
        hourly_price = list(hourly_price_dimensions)[0]['pricePerUnit']['USD']
        break
    
    monthly_price = round(connections * hoursPerDay * workingDays * float(hourly_price), 2)
    return monthly_price

