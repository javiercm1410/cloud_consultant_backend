from python_terraform import *

def pretty_print_outputs(outputs):
    pretty_output = "Successful Deployment\n\n"
    for key, value in outputs.items():
        if not value['sensitive']:
            pretty_output += f"{key}: {value['value']}\n"
    return pretty_output


def aws_three_tier_mysql_deploy(abs_path, 
                                credentials,
                                db_port, 
                                db_master_username, 
                                db_master_password, 
                                web_tier_user_data, 
                                app_tier_user_data, 
                                app_alb_port, 
                                instance_type):
    
    parts = credentials.split(',')
    
    dict_credentials = dict(item.split('=') for item in parts)

    aws_access_key = dict_credentials['USER']
    aws_secret_key = dict_credentials['PASS']

    with open (abs_path + 'web_user_data.sh', 'w') as file:
        file.write(web_tier_user_data)
    
    with open (abs_path + 'app_user_data.sh', 'w') as file:
        file.write(app_tier_user_data)
    
    
    tf = Terraform(working_dir=abs_path, variables={
        "aws_access_key": aws_access_key, 
        "aws_secret_key": aws_secret_key, 
        "db_port": db_port, 
        "db_master_username": db_master_username,
        "db_master_password": db_master_password, 
        "app_alb_port ": app_alb_port, 
        "instance_type ": instance_type}) 
    
    tf.init()
    return_code, stdout, stderr = tf.apply(skip_plan=True)
    outputs = tf.output()
    ppoutputs = pretty_print_outputs(outputs)
    if return_code == 0 : return "Successful Deployment" + f"\n{ppoutputs}"
    else : return "Deployment Failed" + f"\n{stderr}"
    
    
if __name__ == "__main__":
    import sys

    # Read the arguments from the command line
    abs_path = sys.argv[1]
    credentials = sys.argv[2]
    db_port = 3306
    db_master_username = sys.argv[3]
    db_master_password = sys.argv[4]
    web_tier_user_data = sys.argv[5]
    app_tier_user_data = sys.argv[6]
    app_alb_port = sys.argv[7]
    workload = sys.argv[8]

    if workload == "Low":
        instance_type = "t2.small" # 1 vCPU, 2GB RAM
    elif workload == "Medium":
        instance_type = "t2.medium" # 2 vCPU, 4GB RAM
    else:
        instance_type = "t2.large" #2 vCPU, 8GB RAM

    # Call the cloud_design_and_prices function with the given arguments
    output = aws_three_tier_mysql_deploy(abs_path, 
                                         credentials, 
                                         db_port, 
                                         db_master_username, 
                                         db_master_password, 
                                         web_tier_user_data, 
                                         app_tier_user_data, 
                                         app_alb_port, 
                                         instance_type)

    # Convert the output to JSON and print it
    print(output)
