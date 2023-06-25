from aws_classic_three_tier_sql import aws_classic_three_tier_sql
from azure_classic_three_tier_sql import azure_classic_three_tier_sql
from aws_container_based_architecture import aws_container_three_tier_sql
from azure_container_based_architecture import azure_container_based_architecture
from gcp_classic_three_tier_sql import gcp_classic_three_tier_sql
from gcp_container_based_architecture import gcp_container_three_tier_sql
from os_path import get_current_dir
import json 

    
    
def cloud_design_and_prices(cloud_provider_preference, workload, architecture_type, auto_scale, database_type, general_region="US_East"):
    
    function_map = {
        ("AWS", "Classic-three-tier", "MySQL"): aws_classic_three_tier_sql,
        ("AWS", "Container-based", "MySQL"): aws_container_three_tier_sql,
        ("Azure", "Classic-three-tier", "MySQL"): azure_classic_three_tier_sql,
        ("Azure", "Container-based", "MySQL"): azure_container_based_architecture,
        ("GCP", "Classic-three-tier", "MySQL"): gcp_classic_three_tier_sql,
        ("GCP", "Container-based", "MySQL"): gcp_container_three_tier_sql
    }
    regions_map = {
        ("US_East", "AWS"): "US East (N. Virginia)",
        ("US_East", "Azure"): "eastus",
        ("US_East", "GCP"): "us-east1"
    }
    cloud_providers = ["AWS", "Azure", "GCP"]

    output = {}

    # Buscar la tupla en el diccionario y retornar la función correspondiente
    function = function_map.get((cloud_provider_preference, architecture_type, database_type))
    # Buscar la tupla en el diccionario y retornar la región correspondiente
    region = regions_map.get((general_region, cloud_provider_preference))

    working_dir = get_current_dir()
    if function and region:
        output = function(workload, auto_scale, region, working_dir)
    
    output.setdefault("Price", {})  # Asegurarse de que la clave 'Price' exista en 'output'

    for cloud_provider in cloud_providers:
        function = function_map.get((cloud_provider, architecture_type, database_type))
        region = regions_map.get((general_region, cloud_provider))
        if function and region:
            tmp_output = function(workload, auto_scale, region, working_dir)
            output["Price"].setdefault(cloud_provider, round(sum(tmp_output["data"].values()), 2))

    return json.dumps(output, ensure_ascii=False)


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
# cloud_design_and_prices("No", "High", "Classic-three-tier", False, "MySQL")
