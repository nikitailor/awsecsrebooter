# AWS ECS Rebooter
AWS ECS Reboot scheduler can be used to schedule maintenance for the EC2 Instances running your ECS containers. It will reboot each EC2 Instance in the cluster that you specify. This was created to ensure that the kernel security updates are applied.

## How To Set Up:
1. Build the image from the Dockerfile. Clone this repo and run the following in the same folder as the Dockerfile and .py file.

```
docker build -t yourtagname:yourversionnumber .
```

**OPTIONAL: If you want to test the built image with your AWS Credentials from the cmd line you can run the following.**

```
sudo docker run -it -e AWS_DEFAULT_REGION=yourregionhere -e cluster=yourtargetcluster -e AWS_ACCESS_KEY_ID=????? -e AWS_SECRET_ACCESS_KEY=?????? yourtagname:yourversionnumber sh

python /var/runtime/kernelRebootscheduler.py
```

2. Add image to your AWS ECR. First you'll need to create a repo if you don't already have one under AWS ECS Repositories, then run the following.

```
aws ecr get-login --no-include-email --region yourregionhere
```

Login to docker using the command generated from the above, then you can tag and push the image to your repo.

```
docker tag yourtagname:yourversionnumber

docker push youraccountid.dkr.ecr.yourregionhere.amazonaws.com/yourreponame:yourversionnumber
```

3. Create a policy and role for the script to run, you can use the below examples.

### Policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KernelSchedulerPerms",
            "Effect": "Allow",
            "Action": [
                "ec2:RebootInstances",
                "ecs:UpdateContainerInstancesState",
                "ecs:ListContainerInstances",
                "ecs:ListClusters",
                "ecs:DescribeContainerInstances"
            ],
            "Resource": "*"
        }
    ]
}
```

### Roles
Make sure the policy above and the trust relationship role below are added to your role.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

4. Create the task definition and configure container instance settings. Ensure that you add the AWS_DEFAULT_REGION and cluster variables.

```
{
  "executionRoleArn": "arn:aws:iam::youraccountidhere:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "dnsSearchDomains": null,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/kernelRebootYourClusterName",
          "awslogs-region": "eu-west-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "entryPoint": null,
      "portMappings": [],
      "command": null,
      "linuxParameters": null,
      "cpu": 1,
      "environment": [
        {
          "name": "AWS_DEFAULT_REGION",
          "value": "yourregionhere"
        },
        {
          "name": "cluster",
          "value": "yourclustername"
        }
      ],
      "ulimits": null,
      "dnsServers": null,
      "mountPoints": [],
      "workingDirectory": null,
      "dockerSecurityOptions": null,
      "memory": null,
      "memoryReservation": null,
      "volumesFrom": [],
      "image": "youraccountid.dkr.ecr.yourregionhere.amazonaws.com/yourreponame:yourversionnumber",
      "disableNetworking": null,
      "interactive": null,
      "healthCheck": null,
      "essential": true,
      "links": null,
      "hostname": null,
      "extraHosts": null,
      "pseudoTerminal": null,
      "user": null,
      "readonlyRootFilesystem": null,
      "dockerLabels": null,
      "systemControls": null,
      "privileged": null,
      "name": "kernelRebooter"
    }
  ],
  "placementConstraints": [],
  "memory": "512",
  "taskRoleArn": "arn:aws:iam::youraccountid:role/yourrolename",
  "compatibilities": [
    "EC2",
    "FARGATE"
  ],
  "taskDefinitionArn": "arn:aws:ecs:yourregionhere:youraccountid:task-definition/kernelRebootyourclustername:yourlatestrevision",
  "family": "kernelRebootyourclustername",
  "requiresAttributes": [
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "ecs.capability.execution-role-ecr-pull"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "ecs.capability.task-eni"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "com.amazonaws.ecs.capability.ecr-auth"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "com.amazonaws.ecs.capability.task-iam-role"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "ecs.capability.execution-role-awslogs"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "com.amazonaws.ecs.capability.logging-driver.awslogs"
    },
    {
      "targetId": null,
      "targetType": null,
      "value": null,
      "name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"
    }
  ],
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "networkMode": "awsvpc",
  "cpu": "256",
  "revision": yourlatestrevision,
  "status": "ACTIVE",
  "volumes": []
}
```

5. Create a scheduled task using Cron.




