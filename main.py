from aws_classic_three_tier_sql import aws_classic_three_tier_sql
from azure_classic_three_tier_sql import azure_classic_three_tier_sql
from aws_containter_based_architecture import aws_container_three_tier_sql
from os_path import get_current_dir

def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, region="US_East"):
    working_dir = get_current_dir()
    if region == "US_East" and cloud_provider_preference == "AWS":
        region = "US East (N. Virginia)"
        if architecture_type == "Classic-three-tier" and database_type == "SQL":
            output = aws_classic_three_tier_sql(workload, auto_scale, region, working_dir)
        elif architecture_type == "Container-based" and database_type == "SQL":
            output = aws_container_three_tier_sql(workload, region, working_dir)
        else:
            output = None
    elif region == "US_East" and cloud_provider_preference == "Azure":
        region = "eastus"
        if architecture_type == "Classic-three-tier" and database_type == "SQL":
            output = azure_classic_three_tier_sql(workload, auto_scale, region, working_dir)
        elif architecture_type == "Container-based" and database_type == "SQL":
            output = None
        else:
            output = None
    return output 

print(cloud_design_and_prices("AWS", "High", "Classic-three-tier", True, "SQL", "US_East"))