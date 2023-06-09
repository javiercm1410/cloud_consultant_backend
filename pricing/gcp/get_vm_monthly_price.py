def get_compute_engine_price(instance_type, region):
    monthly_price = {("e2-small", "us-east1"): 12.23, 
                     ("e2-medium", "us-east1"): 24.46,
                     ("e2-standard-2", "us-east1"): 48.92}
    return monthly_price[(instance_type, region)]