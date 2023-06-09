def get_load_balancing_price(forwarding_rules, region):
    monthly_price = {(2, "us-east1"): 18.63}
    return monthly_price[(forwarding_rules, region)]