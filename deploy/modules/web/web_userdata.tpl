#!/bin/bash
# unconditionally patch the system
yum -y update

# install ssm agent
yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm

# install some tools
yum -y install \
    mysql \
    git \
    httpd-tools \
    awscli \
    docker \
    python3 \
    python3-pip \
    jq

# install nginx
amazon-linux-extras install nginx1.12

# install docker compose
pip3 install docker-compose

# ensure ssm agent started and enabled
systemctl enable amazon-ssm-agent
systemctl restart amazon-ssm-agent

# ensure docker enabled and started
systemctl enable docker
systemctl start docker

# get parameters
git_key=$$(aws ssm get-parameter --region us-west-2 --name "mooches-git-key" --with-decryption | jq .Parameter.Value -r)
database_password=$$(aws ssm get-parameter --region us-west-2 --name "mooches-database-password-${environment}" --with-decryption | jq .Parameter.Value -r)
database_url=$$(aws rds describe-db-instances --region us-west-2 --db-instance-identifier mooches-mysql-${environment} | jq -r .DBInstances[0].Endpoint.Address)
web_password=$$(aws ssm get-parameter --region us-west-2 --name "mooches-web-password" --with-decryption | jq .Parameter.Value -r)

# write ssh key
cat << EOF > ~ec2-user/.ssh/id_rsa
$${git_key}
EOF


# create nginx config

sed -i 's/default_server//g' /etc/nginx/nginx.conf
cat << EOF >> /etc/nginx/conf.d/site.conf
${nginx_config}
EOF

echo "$${web_password}" | htpasswd -i -c /etc/nginx/.htpasswd admin

# start/enable nginx
systemctl enable nginx
systemctl start nginx

# get code
mkdir -p /opt/web && chown ec2-user: /opt/web
ssh-keyscan github.com >> ~ec2-user/.ssh/known_hosts
chown -R ec2-user: ~ec2-user/.ssh && chmod 0600 ~ec2-user/.ssh/id_rsa
cd /opt/web && sudo -u ec2-user git clone git@github.com:f00d4tehg0dz/45chaos

# write web config
cat << EOF > /opt/web/config.yml
database_engine: mysql
database_uri: $${database_url}
database_username: chaos
database_password: $${database_password}
database_name: chaos
EOF

# checkout, build, and run flask app
cd /opt/web/45chaos && git checkout ${git_branch}
cat << EOF > /opt/web/docker-compose.yml
version: '3'
services:
  web:
    build: ./45chaos/
    ports:
      - 5000:5000
    volumes:
      - /opt/web/config.yml:/opt/web/config.yml
EOF
cd /opt/web && docker-compose up -d
