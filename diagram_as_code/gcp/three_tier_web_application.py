from diagrams import Diagram, Cluster
from diagrams.gcp.compute import ComputeEngine
from diagrams.gcp.database import SQL
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet   

def gcp_classic_three_tier_sql_diagram(auto_scale, working_dir):
    web_app_name = "GCP Three-tier Classic Web Application"
    output_path = f"{working_dir}/backend/images/"
    if auto_scale:
        web_app_name = web_app_name + " (With Auto Scaling)"
        filename = output_path + web_app_name.lower().replace(" ", "_")
        with Diagram(web_app_name, filename, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("Virtual Network"):
                LBFI = LoadBalancing("Load Balancer (Facing Internet)")
                with Cluster ("Private Subnet"):
                    LBFP = LoadBalancing("Load Balancer (Facing Private)")
                    with Cluster("Frontend\nManaged Instance Groups"):
                        VM_Web_Tier = [ComputeEngine("Web"), ComputeEngine("Web"), ComputeEngine("Web")]
                    with Cluster("Backend\nManaged Instance Groups"):
                        VM_App_Tier = [ComputeEngine("App"), ComputeEngine("App"), ComputeEngine("App")]
                    with Cluster("Database Tier"):
                        DB = SQL("Cloud SQL") 
            clients >> internet >> LBFI >> VM_Web_Tier >> LBFP >> VM_App_Tier >> DB
    else:
        web_app_name = web_app_name + " (With Auto Scaling)"
        filename = output_path + web_app_name.lower().replace(" ", "_")
        with Diagram(web_app_name, filename, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("Virtual Network"):
                LBFI = LoadBalancing("Load Balancer (Facing Internet)")
                with Cluster ("Private Subnet"):
                    LBFP = LoadBalancing("Load Balancer (Facing Private)")
                    with Cluster("Frontend"):
                        VM_Web_Tier = [ComputeEngine("Web"), ComputeEngine("Web"), ComputeEngine("Web")]
                    with Cluster("Backend"):
                        VM_App_Tier = [ComputeEngine("App"), ComputeEngine("App"), ComputeEngine("App")]
                    with Cluster("Database Tier"):
                        DB = SQL("Cloud SQL") 
            clients >> internet >> LBFI >> VM_Web_Tier >> LBFP >> VM_App_Tier >> DB
    return filename + ".png"
        

