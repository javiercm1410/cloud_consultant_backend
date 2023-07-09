from python_terraform import *


abs_path = 'C:\\Users\\fredd\\OneDrive\\Escritorio\\CloudProject\\backend\\deployment_templates\\aws\\three-tier-arch-mysql\\'

tf = Terraform(working_dir=abs_path, variables={
    "aws_access_key": "AKIA5W7CSMSU4YZO3AJD", 
    "aws_secret_key": "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", 
    "db_port": 3306, 
    "db_master_username": "animals4life",
    "db_master_password": "animals4life"})
tf.fmt()
tf.init()

#Deploy stack
return_code, stdout, stderr = tf.apply(skip_plan=True)
if return_code == 0 : print("Successful Deployment"); print(stdout)
else : print("Deployment Failed"); print(stderr)

#Detroy stack
# return_code, stdout, stderr = tf.apply(destroy=True, skip_plan=True)
# if return_code == 0 : print("Successful Elimination"); print(stdout)
# else : print("Elimination Failed"); print(stderr)
