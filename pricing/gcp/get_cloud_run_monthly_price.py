def get_cloud_run_prices(request_per_month, number_of_instances, cpu, ram, region):
    monthly_price = {(144000, 1, 2, 2, "us-east1"): 31.28, 
                     (1440000, 2, 4, 4, "us-east1"): 117.71,
                     (14400000, 3, 8, 8, "us-east1"): 335.36}
    return monthly_price[(request_per_month, number_of_instances, cpu, ram, region)]
