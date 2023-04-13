from diagrams import Diagram, Cluster
# from diagrams.aws.database import Dynamodb
from diagrams.aws.network import ALB
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDS
from diagrams.onprem.client import Users    
from diagrams.onprem.network import Internet 


def aws_container_based_architecture_diagram(working_dir):
    web_app_name = "AWS Container Based Architecture"
    output_path = f"{working_dir}/backend/images/"
    filename = output_path + web_app_name.lower().replace(" ", "_")
    with Diagram(web_app_name, filename, show=False):
        clients = Users("Clients")
        internet = Internet("Internet")
        with Cluster("Public"):
            ALBFI = ALB("ALB")
            with Cluster ("Private Subnet"):
                with Cluster ("Container Cluster"):
                    Fargate_group = [Fargate("Container"), 
                                Fargate("Container"), 
                                Fargate("Container")]
                with Cluster("Database Tier"):
                        DB_group = RDS("RDS")

                        # DB_group = Dynamodb("Amazon Aurora")
        clients >> internet >> ALBFI >> Fargate_group >> DB_group
    return filename + ".png"

# print(azure_container_based_architecture_diagram(os.getcwd()))
     