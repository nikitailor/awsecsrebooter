# AWS ECS Rebooter
AWS ECS Reboot scheduler can be used to schedule maintenance for the EC2 Instances running your ECS containers. It will reboot each EC2 Instance in the cluster that you specify. This was created to ensure that the kernel security updates are applied.

## How To Set Up:
1. Build the image from the Dockerfile

2. Add image to your AWS ECR

3. Create a role and policy for the script to run

4. Create the task definition and configure container instance settings

5. Create a scheduled task using Cron




