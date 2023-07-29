#!/bin/bash
sudo yum install git nginx nodejs npm -y
cd /home/ec2-user
git clone https://github.com/byFrederick/web-tier-demo
cd web-tier-demo 
sudo rm /etc/nginx/nginx.conf
sudo mv nginx.conf /etc/nginx/
sudo chmod -R 755 /home/ec2-user
npm install 
npm run build
sudo systemctl start nginx 
sudo systemctl enable nginx