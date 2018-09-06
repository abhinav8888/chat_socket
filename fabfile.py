import boto3
import os
import sys
from fabric2.connection import Connection
from fabric import task
from fabconif import *



@task
def update_sockets_branch(c):
    host = _get_public_dns()
    c = Connection(host=host)
    c.ssh_config['identityfile'] = key_filename
    c.user = 'ubuntu'

    with c.cd('chat_socket/'):
        c.run('git checkout feature/chat_with_user')

def _get_public_dns():
    ec2_client = get_aws_service_client('ec2', region_name)
    instance = get_ec2_instance_by_name(ec2_client, 'koinex')
    return instance['PublicDnsName']

def get_aws_service_client(service_name, region_name):  
        return boto3.client(
            service_name,                   
            region_name = region_name,        
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )

def get_ec2_instance_by_name(ec2_client, instance_name):
    ec2_instance = None
    print('Getting instance details...')
    idesc = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [instance_name]
            }
        ],
    )
    for reservation in idesc['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                    ec2_instance = instance
                    break
    return ec2_instance