# deploy-task-definitions

Script to deploy ECS task definitions

Usage:

``` 
deploy-task-definitions [-h] -c CONFIG

Deploy task definition to ECS

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config directory or file
```
                        
                        
Example config

```
CLUSTER_NAME=name
REGION=us-east-2
FAMILY=family-name
SERVICE_NAME=service-name

TASK_CPU=1024
TASK_MEMORY=1024

TASK_IMAGE=1234.dkr.ecr.us-east-2.amazonaws.com/image
TASK_NAME=api
TASK_ROLE_ARN=arn:aws:iam::1234:role/role-name

PORT_MAPPING_CONTAINER_PORT=8080
PORT_MAPPING_HOST_PORT=8080
PORT_MAPPING_PROTOCOL=tcp

COMMAND=[]
ENTRYPOINT=[]
INSTANCE_CONSTRAINTS=[t2.large, m3.large, m4.large]

ENV_DB_HOSTNAME=${DEV_DB_HOSTNAME}
ENV_DB_NAME=${DEV_DB_NAME}
ENV_DB_PASSWORD=${DEV_DB_PASSWORD}
ENV_DB_USERNAME=${DEV_DB_USERNAME}
ENV_ENVIRONMENT=dev
ENV_TEST_VARIABLE=test

```
