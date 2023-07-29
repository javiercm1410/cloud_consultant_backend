from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.gcp.compute import Run
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.database import SQL

def gcp_container_architecture(auto_scale, working_dir):
    web_app_name = "Container-based architecture"
    if auto_scale:
        output_path = f"{working_dir}/backend/images/"
        filename = output_path + web_app_name.lower().replace(" ", "_")
        with Diagram(web_app_name,filename, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("Google Cloud Platform"):
                with Cluster("Cloud Run Services"):
                    LB = LoadBalancing("Load Balancer")
                    services = [Run("Service 1"), Run("Service 2"), Run("Service 3")]
                LB >> services
                DB = SQL("Cloud SQL (MySQL)")
                services >> DB
            clients >> internet >> LB
        return filename + ".png"
    else:
        output_path = f"{working_dir}/backend/images/"
        filename = output_path + web_app_name.lower().replace(" ", "_")
        with Diagram(web_app_name,filename, show=False):
            clients = Users("Clients")
            internet = Internet("Internet")
            with Cluster("Google Cloud Platform"):
                with Cluster("Cloud Run Services"):
                    LB = LoadBalancing("Load Balancer")
                    services = [Run("Service 1"), Run("Service 2"), Run("Service 3")]
                LB >> services
                DB = SQL("Cloud SQL (MySQL)")
                services >> DB
            clients >> internet >> LB
        return filename + ".png"
