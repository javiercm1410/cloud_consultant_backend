from diagrams import Diagram, Cluster
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import ALB
from diagrams.aws.network import CloudFront
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3
from diagrams.aws.compute import Fargate

with Diagram("Grouped Workers", show=False, direction="TB"):
    with Cluster("VPC"):
        CF = CloudFront("Cloud Front") 
        with Cluster ("Private Subnet"):
            bucket = S3("Frontend")
            ALBFI = ALB("ALB")
            with Cluster ("ASG Web Tier"):
                ECS_group = [Fargate("Web Tier"), 
                            Fargate("Web Tier"), 
                            Fargate("Web Tier")]
            with Cluster("Database Tier"):
                    DB_group = Dynamodb("Amazon Aurora")
                    DB_group - [Dynamodb("Worker")]
                
    CF >> bucket >> ALBFI >> ECS_group >> DB_group
     