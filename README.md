# AWS ECS Rebooter
AWS ECS Reboot scheduler can be used to schedule maintenance for the EC2 Instances running your ECS containers. It will reboot each EC2 Instance in the cluster that you specify. This was created to ensure that the kernel security updates are applied.

## Required:
- docker-lambda/python2.7/build/Dockerfile from https://github.com/lambci/docker-lambda/blob/master/python2.7/build/Dockerfile

## How To Set Up:
- Build Image
- Add image to ECR
- Roles
- Task Definition
- Configure container instance
- Schedule Task using Cron


