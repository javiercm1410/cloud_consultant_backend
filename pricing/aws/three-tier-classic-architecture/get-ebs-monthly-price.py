import boto3
import json

session = boto3.Session(profile_name='default', region_name='us-east-1')

def get_ebs_monthly_price(region, volumeType, volumeSize):
    pricing_client = session.client('pricing', region_name='us-east-1')
    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Storage'},
            #{'Type': 'TERM_MATCH', 'Field': 'group', 'Value': 'EBS Block Storage'},
            #{'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': volumeType},
            {'Type': 'TERM_MATCH', 'Field': 'volumeApiName', 'Value': volumeType}, # Adding gp2 to ensure correct matching for General Purpose SSD (gp2)
            #{'Type': 'TERM_MATCH', 'Field': 'productAttributes', 'Value': f'volumeSize:{volumeSize}'} # Volume size filter
        ]
    )

    with open('prices-ebs.json', 'w') as outfile:
        json.dump(response, outfile)
        
    price_list = response.get('PriceList', [])
    if len(price_list) == 0:
        print(f"No EBS volumes found matching the specified criteria.")
        return
    
    product = response['PriceList'][0]
    ebs_product = json.loads(product)

    # Get the monthly price for the EBS volume
    monthly_price = None
    for term in ebs_product['terms']['OnDemand'].values():
        monthly_price_dimensions = term['priceDimensions'].values()
        monthly_price = list(monthly_price_dimensions)[0]['pricePerUnit']['USD']
        break
    monthly_price = float(monthly_price)
    monthly_price *= volumeSize
    print(f"Monthly price for {volumeType} EBS Volume of size {volumeSize}GB in {region}: {monthly_price}")

get_ebs_monthly_price(region='US East (N. Virginia)', volumeType='gp2', volumeSize=30)
