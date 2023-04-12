from aws_classic_three_tier_sql import aws_classic_three_tier_sql


def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, region):
    if cloud_provider_preference == "None":
        if architecture_type == "Classic_Three_Tier" and database_type == "SQL":
            prices_aws, diagram_path_aws = aws_classic_three_tier_sql(workload, auto_scale)
            prices_azure, diagram_path_azure = azure_classic_three_tier_sql(workload, auto_scale)
            
            
            


        
        