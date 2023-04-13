import boto3
import json

session = boto3.Session(profile_name='admin', region_name='us-east-1')

def get_rds_mysql_monthly_price(region, instanceType, databaseEngine,deploymentOption, storage):
    pricing_client = session.client('pricing', region_name='us-east-1')
    response = pricing_client.get_products(
        ServiceCode='AmazonRDS',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': databaseEngine},
            {'Type': 'TERM_MATCH', 'Field': 'deploymentOption', 'Value': deploymentOption},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instanceType},
        ]
    )

    product = response['PriceList'][0]
    alb_product = json.loads(product)
    # with open('rds_mysql_product.json', 'w') as f:
    #     json.dump(alb_product, f, indent=4)
    # Get the monthly price for the ALB
    hourly_price = None
    for term in alb_product['terms']['OnDemand'].values():
        hourly_price_dimensions = term['priceDimensions'].values()
        hourly_price = list(hourly_price_dimensions)[0]['pricePerUnit']['USD']
        break

    storage *= 0.115
    monthly_price = round(float(hourly_price) * 730, 2) + storage
    return round(monthly_price, 2)

# print(get_rds_mysql_monthly_price(region="US East (N. Virginia)", instanceType='db.t3.micro', databaseEngine='MySQL', deploymentOption='Single-AZ', storage=5))