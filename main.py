from aws_classic_three_tier_sql import aws_classic_three_tier_sql
from azure_classic_three_tier_sql import azure_classic_three_tier_sql
from aws_container_based_architecture import aws_container_three_tier_sql
from azure_container_based_architecture import azure_container_based_architecture
from os_path import get_current_dir
import json 

def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, region):
    FUNCTION_MAP = {
        ("AWS", "Classic-three-tier", "MySQL"): aws_classic_three_tier_sql,
        ("AWS", "Container-based", "MySQL"): aws_container_three_tier_sql,
        ("Azure", "Classic-three-tier", "MySQL"): azure_classic_three_tier_sql,
        ("Azure", "Container-based", "MySQL"): azure_container_based_architecture,
    }
    working_dir = get_current_dir()
    region = "US East (N. Virginia)" if region == "US_East" else region
    function = FUNCTION_MAP.get((cloud_provider_preference, architecture_type, database_type))
    #Cambiar else para que retorne todos los precios 
    output = function(workload, auto_scale, region, working_dir) if function else json.dumps({"result": "None"})
    return output

if __name__ == "__main__":
    import sys

    # Read the arguments from the command line
    cloud_provider_preference = sys.argv[1]
    workload = sys.argv[2]
    architecture_type = sys.argv[3]
    auto_scale = sys.argv[4].lower() == "true"
    database_type = sys.argv[5]

    # Call the cloud_design_and_prices function with the given arguments
    output = cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, region="US_East")

    # Convert the output to JSON and print it
    print(output)
    
# print(cloud_design_and_prices("Azure", "High", "Container-based", False, "SQL", "US_East"))
