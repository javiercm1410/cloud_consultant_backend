from python_terraform import *
import json

def pretty_print_outputs(outputs):
    pretty_output = "Successful Deployment\n\n"
    for key, value in outputs.items():
        if not value['sensitive']:
            pretty_output += f"{key}: {value['value']}\n"
    return pretty_output

def aws_three_tier_mysql_deploy(abs_path, 
                                credentials,
                                db_password,
                                db_name,
                                db_user,
                                db_version,
                                env_db_host,
                                env_db_name,
                                env_db_password,
                                env_db_user,
                                image,
                                image_port):


    with open ("/Users/simon/.google/credentials/cloudconsultant-fc0ed56f2037.json", 'w') as file:
        file.write(credentials)
    
    # db_version = "MYSQL_" + db_version.replace('.', '_')
        
    tf = Terraform(working_dir=abs_path, variables={
        "credentials_path": "/Users/simon/.google/credentials/cloudconsultant-fc0ed56f2037.json",
        "db_password": db_password,
        "db_name": db_name,
        "db_user": db_user,
        "db_version": db_version,
        "env_db_host": env_db_host,
        "env_db_name": env_db_name,
        "env_db_password": env_db_password,
        "env_db_user": env_db_user,
        "image": image,
        "image_port": image_port})
    
    tf.init()
    return_code, stdout, stderr = tf.apply(skip_plan=True)
    outputs = tf.output()
    ppoutputs = pretty_print_outputs(outputs)
    if return_code == 0 : return f"\n{ppoutputs}"
    else : return "Deployment Failed" + f"\n{stderr}"

    
if __name__ == "__main__":
    import sys

    # Read the arguments from the command line
    abs_path = sys.argv[1]
    credentials = sys.argv[2]
    db_password = sys.argv[3]
    db_name = sys.argv[4]
    db_user = sys.argv[4]
    db_version = sys.argv[5]
    environments = sys.argv[6]
    image = sys.argv[7]
    image_port = sys.argv[8]

    db_version = "MYSQL_" + db_version.replace('.', '_')
    environments_array = environments.split(",")
    env_db_host = environments_array[0]
    env_db_name = environments_array[1]
    env_db_password = environments_array[2]
    env_db_user = environments_array[3]


    # Call the cloud_design_and_prices function with the given arguments
    output = aws_three_tier_mysql_deploy(abs_path,
                                        credentials,
                                        db_password,
                                        db_name,
                                        db_user,
                                        db_version,
                                        env_db_host,
                                        env_db_name,
                                        env_db_password,
                                        env_db_user,
                                        image,
                                        image_port)

    # Convert the output to JSON and print it
    print(output)

# abs_path="/Users/simon/codes/CloudProject/backend/deployment_templates/gcp"
# credentials="""{
#   "type": "service_account",
#   "project_id": "cloudconsultant",
#   "private_key_id": "fc0ed56f203720a5fba50d716cc701cd698afb1a",
#   "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDQR6/hO90j1l/U\\nriNIAyk03VIJCYkwFvK58PcytgBKj2PMsNVVBcATSODmifdJth83m6EUTqlu81ON\\nI4X3+W0zDHT6niQcGFmMynn0MsUvYzE7Xlv+oik/8uRojvjJD/PiGe/TeLGkdsaT\\nX6jmf1cEHOESAgR1JOW6xZTIs9ZpwDR++Lt1qHz926jhS8dSGYQC/Of2EtED3/bS\\noMPCDe5cHNLyvttXeWJ4C4GH9dXG8vhZ86slQWkSXm8Trw75rcPTCyI5CrhZ5Pku\\nmwUza1X9ycNh3HJoF0yFnvN2S2tZR9M9teb5jxcTtStkmu7+1jSrXdInq6CNCk6l\\nVYq+YAZhAgMBAAECggEAEcyZNTsJHPpBr5/qF/SyiCKvKLfjPMmD7havqWpwVUQy\\nbS23gs/o/ZI+1goi/e5Ny1IbeUF3rVRSEZUK6omAUYUrrLc9ssD0oNmKLoT1i6Ut\\nxzsQdY76I3g9w3RkbRpV5z6m24BMU20VxJu/iA3d1oDOozFU8YXjtAsVOfRUddj1\\nfrAtzgquWwahdCktQkjD12ykBcisGS8e/IrAHXl0KbDZro330SpBuaVLvZa2Bhqy\\ndiOHoF6uiXBJz2IjdTCpyVCKcBsDVJFWLwfJP9HpV0aar7nwURGy6gMr/ajn30Xh\\n6BLb6CnOTyS9UnjWrw9eyMZPus1NTCaQSuKVJrxNWQKBgQD91hioYUhTGOayNKu+\\nyNGMQ/sPLYHaHQtW9gtBlBP7M7SgUTzAMWZuTz0PLSzZINoBgGVIPHhhEBfxy2cV\\n8BiCTz5OcfRLrayS3wi4E+8z5EwKmUz8ErY4ZRymNwnaNnURiq518NmMmy1gfhmw\\nfYbIzMki07MD0Q0pHwqeTQtpPwKBgQDSDi5WBInFYPcyVXmqGI/glAyg/8/N5GXh\\nHmqx63l2r6Df/GyDtZDi+jKbiyenA52GRsUvz7kFr/3/wBoDH8LzWo5HRQZ7kACx\\nInk1pYqlYc4UZjoyswVLyHhGsB2xECehN7O7+vLcTqTH+wk4iYFASX1KE+awmNRy\\nCTF6M6YIXwKBgQDhFPSeck0Qqlb+lGfqb+YoS6uWxNKNFw4UGW7XwreJG0tCkWae\\nQe/DRu4sw/Etw8ysYi7tQ/m2j++7j5KkSFdjTWNBahim9qS9Q5pWqA6G5BxtlYxH\\nRUxha39hABLzdTCP0npqyJwP6xXsp0SeVGCtM7Hy+OeXLctOuGDRCB5jPwKBgHcy\\nLt8G4jsL5Bo+4LRCDdrtiCEQKJZ4RcuyG+9sZNeRn+OadOVkcZwrR+51z4F5jrj0\\njc6svBxbGvI2y0v8iP7Y4yXUKHKTa6EYo9lqX7urPWrb+6hrZ9TyJDZQl/iy5xoX\\n5rkEFS4ovl7wt/HKLXsSeLNBicWqY9t2Fgp3Jn9XAoGBALANEm/XJ5pn2j+6/tnd\\nYUTEhnMbBPDxUhVygI6FlvyoBLrZCeRyUAQoBAgJD+36dvfzcJLOslFV2gbAoxO/\\nFEif4RKwCYtGIhz/H2PUKDiK/JgrU3cuFPYuTL2Pdv56gBSy4ggQPR4Fgj1+uA2u\\nH4KQ1xqgqx1IABJ1bZIdRk7o\\n-----END PRIVATE KEY-----\\n",
#   "client_email": "cloudconsultantterraform@cloudconsultant.iam.gserviceaccount.com",
#   "client_id": "108468317190908963190",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloudconsultantterraform%40cloudconsultant.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }"""
# db_password="admin123!"
# db_name="admin"
# db_user="admin"
# db_version="8.0"
# env_db_host="WORDPRESS_DB_HOST"
# env_db_name="WORDPRESS_DB_NAME"
# env_db_password="WORDPRESS_DB_PASSWORD"
# env_db_user="WORDPRESS_DB_USER"
# image="wordpress"
# image_port=80

# print(aws_three_tier_mysql_deploy(abs_path, 
#                                 credentials,
#                                 db_password,
#                                 db_name,
#                                 db_user,
#                                 db_version,
#                                 env_db_host,
#                                 env_db_name,
#                                 env_db_password,
#                                 env_db_user,
#                                 image,
#                                 image_port))




# WORDPRESS_DB_HOST,WORDPRESS_DB_NAME,WORDPRESS_DB_PASSWORD,WORDPRESS_DB_USER

# {
#   "type": "service_account",
#   "project_id": "cloudconsultant",
#   "private_key_id": "fc0ed56f203720a5fba50d716cc701cd698afb1a",
#   "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDQR6/hO90j1l/U\\nriNIAyk03VIJCYkwFvK58PcytgBKj2PMsNVVBcATSODmifdJth83m6EUTqlu81ON\\nI4X3+W0zDHT6niQcGFmMynn0MsUvYzE7Xlv+oik/8uRojvjJD/PiGe/TeLGkdsaT\\nX6jmf1cEHOESAgR1JOW6xZTIs9ZpwDR++Lt1qHz926jhS8dSGYQC/Of2EtED3/bS\\noMPCDe5cHNLyvttXeWJ4C4GH9dXG8vhZ86slQWkSXm8Trw75rcPTCyI5CrhZ5Pku\\nmwUza1X9ycNh3HJoF0yFnvN2S2tZR9M9teb5jxcTtStkmu7+1jSrXdInq6CNCk6l\\nVYq+YAZhAgMBAAECggEAEcyZNTsJHPpBr5/qF/SyiCKvKLfjPMmD7havqWpwVUQy\\nbS23gs/o/ZI+1goi/e5Ny1IbeUF3rVRSEZUK6omAUYUrrLc9ssD0oNmKLoT1i6Ut\\nxzsQdY76I3g9w3RkbRpV5z6m24BMU20VxJu/iA3d1oDOozFU8YXjtAsVOfRUddj1\\nfrAtzgquWwahdCktQkjD12ykBcisGS8e/IrAHXl0KbDZro330SpBuaVLvZa2Bhqy\\ndiOHoF6uiXBJz2IjdTCpyVCKcBsDVJFWLwfJP9HpV0aar7nwURGy6gMr/ajn30Xh\\n6BLb6CnOTyS9UnjWrw9eyMZPus1NTCaQSuKVJrxNWQKBgQD91hioYUhTGOayNKu+\\nyNGMQ/sPLYHaHQtW9gtBlBP7M7SgUTzAMWZuTz0PLSzZINoBgGVIPHhhEBfxy2cV\\n8BiCTz5OcfRLrayS3wi4E+8z5EwKmUz8ErY4ZRymNwnaNnURiq518NmMmy1gfhmw\\nfYbIzMki07MD0Q0pHwqeTQtpPwKBgQDSDi5WBInFYPcyVXmqGI/glAyg/8/N5GXh\\nHmqx63l2r6Df/GyDtZDi+jKbiyenA52GRsUvz7kFr/3/wBoDH8LzWo5HRQZ7kACx\\nInk1pYqlYc4UZjoyswVLyHhGsB2xECehN7O7+vLcTqTH+wk4iYFASX1KE+awmNRy\\nCTF6M6YIXwKBgQDhFPSeck0Qqlb+lGfqb+YoS6uWxNKNFw4UGW7XwreJG0tCkWae\\nQe/DRu4sw/Etw8ysYi7tQ/m2j++7j5KkSFdjTWNBahim9qS9Q5pWqA6G5BxtlYxH\\nRUxha39hABLzdTCP0npqyJwP6xXsp0SeVGCtM7Hy+OeXLctOuGDRCB5jPwKBgHcy\\nLt8G4jsL5Bo+4LRCDdrtiCEQKJZ4RcuyG+9sZNeRn+OadOVkcZwrR+51z4F5jrj0\\njc6svBxbGvI2y0v8iP7Y4yXUKHKTa6EYo9lqX7urPWrb+6hrZ9TyJDZQl/iy5xoX\\n5rkEFS4ovl7wt/HKLXsSeLNBicWqY9t2Fgp3Jn9XAoGBALANEm/XJ5pn2j+6/tnd\\nYUTEhnMbBPDxUhVygI6FlvyoBLrZCeRyUAQoBAgJD+36dvfzcJLOslFV2gbAoxO/\\nFEif4RKwCYtGIhz/H2PUKDiK/JgrU3cuFPYuTL2Pdv56gBSy4ggQPR4Fgj1+uA2u\\nH4KQ1xqgqx1IABJ1bZIdRk7o\\n-----END PRIVATE KEY-----\\n",
#   "client_email": "cloudconsultantterraform@cloudconsultant.iam.gserviceaccount.com",
#   "client_id": "108468317190908963190",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloudconsultantterraform%40cloudconsultant.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }
