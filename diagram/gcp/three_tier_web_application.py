from diagrams import Diagram, Cluster
from diagrams.gcp.compute import ComputeEngine
from diagrams.gcp.database import SQL
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet   

web_app_name = "GCP Three-tier Classic Web Application"
with Diagram(web_app_name, show=False):
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

