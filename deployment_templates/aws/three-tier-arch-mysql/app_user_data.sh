#!/bin/bash
sudo yum install mariadb105 git nodejs npm -y
npm install -g pm2
cd /home/ec2-user
git clone https://github.com/byFrederick/app-tier-demo
cd app-tier-demo
npm install
pm2 start index.js