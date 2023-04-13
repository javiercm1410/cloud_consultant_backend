from diagrams import Diagram, Cluster
from diagrams.azure.network import ApplicationGateway 
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.database import ManagedDatabases
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet 

def azure_container_based_architecture_diagram(working_dir):
    web_app_name = "Azure Container Based Architecture"
    output_path = f"{working_dir}/backend/images/"
    filename = output_path + web_app_name.lower().replace(" ", "_")
    with Diagram(web_app_name, filename, show=False):
        clients = Users("Clients")
        internet = Internet("Internet")
        with Cluster("Public"):
            ALBFI = ApplicationGateway("ALB")
            with Cluster ("Private Subnet"):
                with Cluster ("Container Cluster"):
                    ACI_group = [ContainerInstances("Container"), 
                                ContainerInstances("Container"), 
                                ContainerInstances("Container")]
                with Cluster("Database Tier"):
                        DB_group = ManagedDatabases("Managed SQL Database")

                        # DB_group = Dynamodb("Amazon Aurora")
        clients >> internet >> ALBFI >> ACI_group >> DB_group
    return filename + ".png"

# print(azure_container_based_architecture_diagram(os.getcwd()))
