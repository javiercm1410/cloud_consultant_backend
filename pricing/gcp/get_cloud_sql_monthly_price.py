def get_cloud_sql_price(instance_type, ssd_storage, region):
    monthly_price = {("db-standard-1", 10, "us-east1"): 18.63}
    return monthly_price[(instance_type, ssd_storage, region)]