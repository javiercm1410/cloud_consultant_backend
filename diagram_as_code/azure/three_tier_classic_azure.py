from diagrams import Diagram, Cluster
from diagrams.azure.compute import VM
from diagrams.azure.database import ManagedDatabases
from diagrams.azure.network import ApplicationGateway 
from diagrams.azure.network import VirtualNetworkGateways
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet

def azure_classic_three_tier_sql_diagram
web_app_name = "Azure Three-tier Classic Web Application"
with Diagram(web_app_name, show=False):
    clients = Users("Clients")
    internet = Internet("Internet")
    with Cluster("Virtual Network"):
        ALBFI = ApplicationGateway("ALB (Facing internet)")
        with Cluster ("Private Subnet"):
            ALBFP = ApplicationGateway("ALB (Facing Private)")
            with Cluster ("Frontend\nVM Scale Set"):
                VM_Web_Tier = [VM("Web"), VM("Web"), VM("Web")]
            with Cluster ("Backend\nVM Scale Set"):
                VM_App_Tier = [VM("App"), VM("App"), VM("App")]
            with Cluster("Database Tier"):
                DB = ManagedDatabases("Managed SQL Database")
    clients >> internet >> ALBFI >> VM_Web_Tier >> ALBFP >> VM_App_Tier >> DB