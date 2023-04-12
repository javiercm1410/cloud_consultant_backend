import boto3
import json


# Create a Session object that uses the 'admin' profile in the ~/.aws/credentials file
session = boto3.Session(profile_name='admin', region_name='us-east-1')

# Create an EC2 client using the session
ec2_client = session.client('ec2', region_name='us-east-1')

# Call EC2 API methods
response = ec2_client.describe_instances()
def get_ec2_monthly_price(region, instanceType):
    # Get the EC2 product code
    pricing_client = session.client('pricing', region_name='us-east-1')
    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instanceType},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region}, 
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'}, 
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'}, 
            {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw','Value': 'NA'},
            {'Type': 'TERM_MATCH', 'Field': 'marketoption','Value': 'OnDemand'},
            {'Type': 'TERM_MATCH', 'Field': 'usagetype','Value': f'BoxUsage:{instanceType}'},
        ]
    )
    
    product = response['PriceList'][0]
    ec2_product = json.loads(product)

    # Get the hourly price for the instance
    hourly_price = None
    for term in ec2_product['terms']['OnDemand'].values():
        hourly_price_dimensions = term['priceDimensions'].values()
        hourly_price = list(hourly_price_dimensions)[0]['pricePerUnit']['USD']
        break
    monthly_price = round(float(hourly_price) * 730, 2)
    return monthly_price

