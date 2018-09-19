FROM python:3
  
WORKDIR /var/runtime

RUN pip install boto3 awscli virtualenv pipenv --no-cache-dir

COPY kernelRebootScheduler.py /var/runtime/kernelRebootScheduler.py

CMD [ "python", "./kernelRebootScheduler.py" ]
