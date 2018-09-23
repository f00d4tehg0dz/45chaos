#!/bin/bash
# unconditionally patch the system
yum -y update

# install ssm agent
yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm

# install some tools
yum -y install \
    mysql \
    git \
    python3 \
    python3-pip \
    awscli \
    docker \
    jq

# install docker compose
pip3 install docker-compose

# ensure ssm agent started and enabled
systemctl enable amazon-ssm-agent
systemctl restart amazon-ssm-agent

# ensure docker enabled and started
systemctl enable docker
systemctl start docker

# get and store ssh key for github
git_key=$(aws ssm get-parameter --region us-west-2 --name "mooches-git-key" --with-decryption | jq .Parameter.Value -r)
cat << EOF > ~ec2-user/.ssh/id_rsa
${git_key}
EOF

# get code
mkdir -p /opt/web && chown ec2-user: /opt/web
ssh-keyscan github.com >> ~ec2-user/.ssh/known_hosts
chown -R ec2-user: ~ec2-user/.ssh && chmod 0600 ~ec2-user/.ssh/id_rsa
cd /opt/web && sudo -u ec2-user git clone git@github.com:f00d4tehg0dz/45chaos

# checkout, build, and run flask app
cd /opt/web/45chaos && git checkout zimmerman
cat << EOF > /opt/web/docker-compose.yml
version: '3'
services:
  web:
    build: ./45chaos/flask
    ports:
      - 80:5000
EOF
cd /opt/web && docker-compose up -d
