from python_terraform import *


def aws_three_tier_mysql_deploy(abs_path, 
                                aws_access_key, 
                                aws_secret_key, 
                                db_port, 
                                db_master_username, 
                                db_master_password, 
                                web_tier_user_data, 
                                app_tier_user_data, 
                                app_alb_port, 
                                instance_type):
    
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
        # "web_tier_user_data ": web_tier_user_data, 
        # "app_tier_user_data ": app_tier_user_data, 
        "app_alb_port ": app_alb_port, 
        "instance_type ": instance_type}) 
    
    tf.init()
    return_code, stdout, stderr = tf.apply(skip_plan=True)
    if return_code == 0 : return "Successful Deployment" + f"\n{stdout}\nTo connect to deployed compute instances you must access the AWS portal and go to the EC2 service"
    else : return "Deployment Failed" + f"\n{stderr}"
    
    
if __name__ == "__main__":
    import sys

    # Read the arguments from the command line
    abs_path = sys.argv[1]
    aws_access_key = sys.argv[2]
    aws_secret_key = sys.argv[3]
    db_port = sys.argv[4]
    db_master_username = sys.argv[5]
    db_master_password = sys.argv[6]
    web_tier_user_data = sys.argv[7]
    app_tier_user_data = sys.argv[8]
    app_alb_port = sys.argv[9]
    workload = sys.argv[10]

    if workload == "Low":
        instance_type = "t2.small" # 1 vCPU, 2GB RAM
    elif workload == "Medium":
        instance_type = "t2.medium" # 2 vCPU, 4GB RAM
    else:
        instance_type = "t2.large" #2 vCPU, 8GB RAM

    # Call the cloud_design_and_prices function with the given arguments
    output = aws_three_tier_mysql_deploy(abs_path, 
                                         aws_access_key, 
                                         aws_secret_key, 
                                         db_port, 
                                         db_master_username, 
                                         db_master_password, 
                                         web_tier_user_data, 
                                         app_tier_user_data, 
                                         app_alb_port, 
                                         instance_type)

    # Convert the output to JSON and print it
    print(output)

# aws_access_key = "AKIA5W7CSMSU4YZO3AJD"
# aws_secret_key = "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"
# db_port = 3306
# db_master_username = "admin"
# db_master_password = "administrator"

# web_tier_user_data = """#!/bin/bash
# sudo yum install git nginx nodejs npm -y
# cd /home/ec2-user
# git clone https://github.com/byFrederick/web-tier-demo
# cd web-tier-demo 
# sudo rm /etc/nginx/nginx.conf
# sudo mv nginx.conf /etc/nginx/
# sudo chmod -R 755 /home/ec2-user
# npm install 
# npm run build
# sudo systemctl start nginx 
# sudo systemctl enable nginx"""

# app_tier_user_data = """#!/bin/bash
# sudo yum install mariadb105 git nodejs npm -y
# npm install -g pm2
# cd /home/ec2-user
# git clone https://github.com/byFrederick/app-tier-demo
# cd app-tier-demo
# npm install
# pm2 start index.js"""

# app_alb_port = 4000

# instance_type = "t2.micro"

# abs_path = 'C:\\Users\\fredd\\OneDrive\\Escritorio\\CloudProject\\backend\\deployment_templates\\aws\\three-tier-arch-mysql\\'


# print(aws_three_tier_mysql_deploy(abs_path, 
#                             aws_access_key, 
#                             aws_secret_key, 
#                             db_port, 
#                             db_master_username, 
#                             db_master_password, 
#                             web_tier_user_data, 
#                             app_tier_user_data, 
#                             app_alb_port, 
#                             instance_type))