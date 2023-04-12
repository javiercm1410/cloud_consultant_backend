from diagrams import Diagram, Cluster
from diagrams.azure.network import CDNProfiles
from diagrams.azure.database import BlobStorage
from diagrams.azure.integration import APIManagement
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import CosmosDb

with Diagram("Grouped Workers", show=False, direction="TB"):
    with Cluster("Stactic Content"):
        CF = CDNProfiles("Cloud Front")
        bucket = BlobStorage("Frontend")
    with Cluster("API"):
        APILD = APIManagement("API Management")
        API_group = [FunctionApps("Internal API 1"), 
                    FunctionApps("Internal API 2"), 
                    FunctionApps("Internal API 3")]
    with Cluster("Database Tier"):
            DB_group = CosmosDb("NoSQL DB")
            DB_group - [CosmosDb("NoSQL DB")]
                
    CF >> bucket 
    APILD >> API_group >> DB_group

