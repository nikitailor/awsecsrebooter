import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import time

ecs = boto3.client('ecs')


def rebootEcsInstances():
    # Create list of ec2instances to be returned
    cluster = os.environ['cluster']
    print("Current cluster: %s" % cluster)

    ecs_instances = ecs.list_container_instances(cluster=cluster)

    if not ecs_instances['containerInstanceArns']:
        print("No container instances")
        return False
    else:
        print("ECS Instances: %s" % ecs_instances)

        container_arns = ecs_instances['containerInstanceArns']

        if not container_arns:
            print("container_arns is empty")
        else:
            print("Container ARN list: %s" % container_arns)

            ecs_info = ecs.describe_container_instances(
                cluster=cluster, containerInstances=container_arns)

            if not ecs_info:
                print("No container information found")
                return False
            else:
                # Iterate over the each container in ecs_info
                # Get the EC2 instance id and set the container to draining
                # before reboot
                for container_instance in ecs_info['containerInstances']:
                    ec2instanceid = container_instance['ec2InstanceId']
                    print('ec2instanceid %s' %
                          container_instance['ec2InstanceId'])
                    ec2instancelist = []
                    ec2instancelist.append(ec2instanceid)
                    arnlist = []
                    arnlist.append(container_instance['containerInstanceArn'])
                    arn = container_instance['containerInstanceArn']
                    print("arn: %s" % container_instance['containerInstanceArn'])
                    drainedcontainers = []

                    # Check ECS instance state is drained and if not set to
                    # draining
                    if container_instance['status'] != 'DRAINING':
                        containerDrain(cluster, arnlist)
                        print("DRAINING")
                        drainedcontainers.append(arn)
                    elif container_instance['status'] == 'DRAINING':
                        drainedcontainers.append(arn)
                    else:
                        print("ERROR: container instance % s \
                              could not be set to draining" % ec2instanceid)
                        return False

                    mustend = datetime.utcnow() + timedelta(minutes=10)

                    while datetime.utcnow() <= mustend:
                        taskcount = taskCounter(cluster, container_arns, arn)
                        if taskcount == 0:
                            # Run reboot and re-activate container instance
                            print("No tasks running")
                            rebooter(ec2instancelist)
                            containerActivate(cluster, arnlist)
                            break
                        else:
                            time.sleep(60)
                    else:
                        # Abort after 10 minutes
                        print("ERROR: Max time reached aborting")
                        return False


def taskCounter(cluster, container_arns, arn):
    # Get the current running task count
    taskcount_info = ecs.describe_container_instances(
        cluster=cluster, containerInstances=container_arns)

    for container_instance in taskcount_info['containerInstances']:
        if arn == container_instance['containerInstanceArn']:
            currentcount = container_instance['runningTasksCount']
            print("Current ARN: %s and running tasks count of %s" %
                  (arn, currentcount))
            return currentcount


def containerDrain(cluster, arn):
    # Set status to draining and then run reboot
    print('Setting container instance %s (%s) to DRAINING' % (arn, cluster))
    ecs.update_container_instances_state(
        cluster=cluster, containerInstances=arn, status='DRAINING')


def containerActivate(cluster, arn):
    # Set status back to active
    print('Setting container instance %s (%s) to ACTIVE' % (arn, cluster))
    ecs.update_container_instances_state(
        cluster=cluster, containerInstances=arn, status='ACTIVE')


def rebooter(instance):
    ec2 = boto3.client('ec2')

    print("Rebooting instance: %s" % instance)

    try:
        ec2.reboot_instances(InstanceIds=instance, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print("You don't have permission to reboot instances.")
            raise

    try:
        response = ec2.reboot_instances(InstanceIds=instance, DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)


if __name__ == "__main__":
    rebootEcsInstances()
