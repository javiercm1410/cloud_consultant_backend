import boto3
import json

session = boto3.Session(profile_name='default', region_name='us-east-1')

def get_rds_mysql_monthly_price(region, instanceType, databaseEngine,deploymentOption):
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

    # Get the monthly price for the ALB
    hourly_price = None
    for term in alb_product['terms']['OnDemand'].values():
        hourly_price_dimensions = term['priceDimensions'].values()
        hourly_price = list(hourly_price_dimensions)[0]['pricePerUnit']['USD']
        break

    print(f"Hourly price for RDS {databaseEngine} in {region}: {hourly_price}")
    monthly_price = round(float(hourly_price) * 730, 2)
    print(f"Monthly price for RDS {databaseEngine} in {region}: {monthly_price}")
get_rds_mysql_monthly_price(region='US East (N. Virginia)', 
                            instanceType='db.t3.micro', 
                            databaseEngine='MySQL', 
                            deploymentOption='Single-AZ')
