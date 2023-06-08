from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.gcp.compute import Run
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.database import SQL

container_app_name = "Container Web Application"
with Diagram(container_app_name, show=False):
    clients = Users("Clients")
    internet = Internet("Internet")
    with Cluster("Google Cloud Platform"):
        LB = LoadBalancing("Load Balancer")
        with Cluster("Cloud Run Services"):
            services = [Run("Service 1"), Run("Service 2"), Run("Service 3")]
        LB >> services
        DB = SQL("Cloud SQL (MySQL)")
        services >> DB
    clients >> internet >> LB
