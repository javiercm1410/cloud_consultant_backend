from aws_classic_three_tier_sql import aws_classic_three_tier_sql
from azure_classic_three_tier_sql import azure_classic_three_tier_sql
from aws_container_based_architecture import aws_container_three_tier_sql
from azure_container_based_architecture import azure_container_based_architecture
from gcp_classic_three_tier_sql import gcp_classic_three_tier_sql
from os_path import get_current_dir
import json 

# def get_classic_three_tier_sql_prices(function):
    
    
def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, general_region="US_East"):
    
    function_map = {
        ("AWS", "Classic-three-tier", "MySQL"): aws_classic_three_tier_sql,
        ("AWS", "Container-based", "MySQL"): aws_container_three_tier_sql,
        ("Azure", "Classic-three-tier", "MySQL"): azure_classic_three_tier_sql,
        ("Azure", "Container-based", "MySQL"): azure_container_based_architecture,
        ("GCP", "Classic-three-tier", "MySQL"): gcp_classic_three_tier_sql,
    }
    regions_map = {
        ("US_East", "AWS"): "US East (N. Virginia)",
        ("US_East", "Azure"): "eastus",
        ("US_East", "GCP"): "us-east1"
    }
    cloud_providers = ["AWS", "Azure", "GCP"]
    
    #Se busca la tupla en el diccionario y se retorna la funcion correspondiente 
    function = function_map.get((cloud_provider_preference, architecture_type, database_type))
    #Se busca la tupla en el diccionario y se retorna la region correspondiente
    region = regions_map.get((general_region, cloud_provider_preference))
    
    working_dir = get_current_dir()
    
    output = {}
    if function and region: 
        output = function(workload, auto_scale, region, working_dir) 
    
    elif cloud_provider_preference == "No":
        for cloud_provider in cloud_providers:
            function = function_map.get((cloud_provider, architecture_type, database_type))
            region = regions_map.get((general_region, cloud_provider))
            if function and region:
                tmp_output = json.loads(function(workload, auto_scale, region, working_dir))
                output[cloud_provider] = round(sum(tmp_output["data"].values()), 2)
        output = json.dumps(output)
    else:
        output = {"result": "None"}
        
    return output

    #Estructura de output cuando se llama una funcion:
    # output = {"imageBase64" : base64_image, "data": {"Service_n" : price_n}}

if __name__ == "__main__":
    import sys

    # Read the arguments from the command line
    cloud_provider_preference = sys.argv[1]
    workload = sys.argv[2]
    architecture_type = sys.argv[3]
    auto_scale = sys.argv[4].lower() == "true"
    database_type = sys.argv[5]

    # Call the cloud_design_and_prices function with the given arguments
    output = cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type)

    # Convert the output to JSON and print it
    print(output)
    
# print(cloud_design_and_prices("No", "High", "Classic-three-tier", False, "MySQL"))
