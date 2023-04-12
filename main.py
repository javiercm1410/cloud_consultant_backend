import sys
from diagram.aws.three_tier_classic_aws import aws_classic_three_tier_sql_diagram
from aws_classic_three_tier_sql import aws_classic_three_tier_sql


def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type):
    if cloud_provider_preference == "None":
        if architecture_type == "Classic_Three_Tier" and database_type == "SQL":
            prices, diagram_path = aws_classic_three_tier_sql(workload, auto_scale)
            
            
            


        
        