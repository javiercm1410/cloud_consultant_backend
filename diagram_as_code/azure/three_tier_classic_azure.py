from diagrams import Diagram, Cluster
from diagrams.azure.compute import VM
from diagrams.azure.database import ManagedDatabases
from diagrams.azure.network import ApplicationGateway 
from diagrams.azure.network import VirtualNetworkGateways
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet

def azure_classic_three_tier_sql_diagram(auto_scale):
    web_app_name = "Azure Three-tier Classic Web Application"
    root_path = "C://Users//fredd//OneDrive - Pontificia Universidad Católica Madre y Maestra//"
    output_path = f"{root_path}//cloud-consultant//backend//images//"
    if auto_scale == "Yes":
        web_app_name = web_app_name + " (With Auto Scaling)"
        filename = output_path + web_app_name.lower().replace(" ", "_")
        with Diagram(web_app_name, filename, show=False):
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
    else:
        web_app_name = web_app_name + " (Without Auto Scaling)"
        filename = output_path + web_app_name.lower().replace(" ", "_")
        with Diagram(web_app_name, filename, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("Virtual Network"):
                ALBFI = ApplicationGateway("ALB (Facing internet)")
                with Cluster ("Private Subnet"):
                    ALBFP = ApplicationGateway("ALB (Facing Private)")
                    with Cluster ("Frontend"):
                        VM_Web_Tier = [VM("Web"), VM("Web"), VM("Web")]
                    with Cluster ("Backend"):
                        VM_App_Tier = [VM("App"), VM("App"), VM("App")]
                    with Cluster("Database Tier"):
                        DB = ManagedDatabases("Managed SQL Database")
            clients >> internet >> ALBFI >> VM_Web_Tier >> ALBFP >> VM_App_Tier >> DB
    return filename

azure_classic_three_tier_sql_diagram("Yes")