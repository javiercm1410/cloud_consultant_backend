from diagrams import Diagram, Cluster
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import ALB
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDS


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
     