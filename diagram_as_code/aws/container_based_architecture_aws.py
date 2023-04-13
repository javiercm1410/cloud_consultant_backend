from diagrams import Diagram, Cluster
# from diagrams.aws.database import Dynamodb
from diagrams.aws.network import ALB
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDS

def azure_container_based_architecture_diagram(working_dir):
    web_app_name = "AWS Container Based Architecture"
    output_path = f"{working_dir}/backend/images/"
    filename = output_path + web_app_name.lower().replace(" ", "_")
    
with Diagram("Grouped Workers", show=False):
    with Cluster("Public"):
        ALBFI = ALB("ALB")
        with Cluster ("Private Subnet"):
            with Cluster ("Container Cluster"):
                Fargate_group = [Fargate("Container"), 
                            Fargate("Container"), 
                            Fargate("Container")]
            with Cluster("Database Tier"):
                    DB_group = RDS("Amazon Aurora")

                    # DB_group = Dynamodb("Amazon Aurora")
                
    ALBFI >> Fargate_group >> DB_group
     