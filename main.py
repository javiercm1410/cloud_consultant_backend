from aws_classic_three_tier_sql import aws_classic_three_tier_sql
from azure_classic_three_tier_sql import azure_classic_three_tier_sql
from aws_containter_based_architecture import aws_container_three_tier_sql
from os_path import get_current_dir

def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, region="US_East"):
    working_dir = get_current_dir()
    if cloud_provider_preference == "No":
        if region == "US_East":
                region_aws = "US East (N. Virginia)"
                region_azure = "eastus"
        if architecture_type == "Classic-three-tier" and database_type == "SQL":
            output_aws = aws_classic_three_tier_sql(workload, auto_scale, region_aws, working_dir)
            output_azure = azure_classic_three_tier_sql(workload, auto_scale, region_azure, working_dir)
        elif architecture_type == "Container-based" and database_type == "SQL":
            output_aws = aws_container_three_tier_sql(workload, region_aws, working_dir)
            output_azure = None
    return output_aws, output_azure

print(cloud_design_and_prices("No", "High", "Container-based", True, "SQL", "US_East"))
            


        
        