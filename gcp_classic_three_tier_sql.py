from diagram_as_code.gcp.three_tier_web_application import gcp_classic_three_tier_sql_diagram
from pricing.gcp.get_vm_monthly_price import get_compute_engine_price
from pricing.gcp.get_lb_monthly_price import get_load_balancing_price
from pricing.gcp.get_cloud_sql_monthly_price import get_cloud_sql_price
import json
import base64

def gcp_classic_three_tier_sql(workload, auto_scale, region, working_dir):
    prices = {}
    
    diagram_path = gcp_classic_three_tier_sql_diagram(auto_scale, working_dir)
    if workload == "Low":
        instance_type = "e2-small"
    elif workload == "Medium":
        instance_type = "e2-medium"
    else:
        instance_type = "e2-standard-2"
        
    prices["Compute_Engine"] = get_compute_engine_price(instance_type, region)*2
    prices["Load_Balancing"] = get_load_balancing_price(2, region)*2
    prices["Cloud_SQL"] = get_cloud_sql_price("db-standard-1", 10, region)*2
    
    # Read the image file as binary data
    with open(diagram_path, "rb") as image_file:
        image_data = image_file.read()

    # Encode the binary data as a base64 string
    base64_image = base64.b64encode(image_data).decode('utf-8')

    output = {
        "imageBase64": base64_image,
        "data": prices
    }

    return output
