from diagrams import Diagram, Cluster
from diagrams.aws.network import VPC     
from diagrams.aws.compute import EC2               
from diagrams.aws.database import RDS
from diagrams.aws.network import ALB 
from diagrams.aws.network import ClientVpn  
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet 

def aws_classic_three_tier_sql_diagram(auto_scale, current_dir):
    web_app_name = "AWS Three tier Classic Web Application"
    if auto_scale == "Yes":
        web_app_name = web_app_name + " (With Auto Scaling)"
        with Diagram(web_app_name, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("VPC"):
                ALBFI = ALB("ALB (Facing internet)")
                with Cluster ("Private Subnet"):
                    ALBFP = ALB("ALB (Facing Private)")
                    with Cluster ("Frontend\nAuto Scaling Group"):
                        EC2_Web_Tier = [EC2("Web Tier"), EC2("Web Tier"), EC2("Web Tier")]
                    with Cluster ("Backend\nAuto Scaling Group"):
                        EC2_App_Tier = [EC2("App Tier"), EC2("App Tier"), EC2("App Tier")]
                    with Cluster("Database Tier"):
                        DB = RDS("RDS")
            clients >> internet >> ALBFI >> EC2_Web_Tier >> ALBFP >> EC2_App_Tier >> DB
    else:
        web_app_name = web_app_name + " (Without Auto Scaling)"
        with Diagram(web_app_name, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("VPC"):
                ALBFI = ALB("ALB (Facing internet)")
                with Cluster ("Private Subnet"):
                    ALBFP = ALB("ALB (Facing Private)")
                    with Cluster ("Frontend"):
                        EC2_Web_Tier = [EC2("Web Tier"), EC2("Web Tier"), EC2("Web Tier")]
                    with Cluster ("Backend"):
                        EC2_App_Tier = [EC2("App Tier"), EC2("App Tier"), EC2("App Tier")]
                    with Cluster("Database Tier"):
                        DB = RDS("RDS")
            clients >> internet >> ALBFI >> EC2_Web_Tier >> ALBFP >> EC2_App_Tier >> DB
    
    return current_dir + "\\" + web_app_name.lower().replace(" ", "_") + ".png"



