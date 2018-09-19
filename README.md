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

4. Create the task definition and configure container instance settings.

5. Create a scheduled task using Cron.




