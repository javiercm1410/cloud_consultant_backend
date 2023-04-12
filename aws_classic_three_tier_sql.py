from diagram.aws.three_tier_classic_aws import aws_classic_three_tier_sql_diagram

def aws_classic_three_tier_sql(workload, auto_scale):
    prices = []
    diagram_path = aws_classic_three_tier_sql_diagram(auto_scale)
    if workload == "Low":
        