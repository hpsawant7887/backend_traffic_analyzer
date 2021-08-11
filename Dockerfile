#BASE IMAGE
FROM python:3.9-slim

#Set Working Directory in the container
WORKDIR /opt/backend_traffic_analyzer

#Copy the package
COPY . /opt/backend_traffic_analyzer

#Install Tools
RUN apt-get update && apt-get install -y vim

# install dependencies
RUN pip install setuptools
RUN pip install pytest

#Setup the tool
RUN python3 setup.py install
RUN python3 -m pytest
RUN mkdir /var/log/backend_traffic_analyzer

CMD ["traffic-analyze", "--help"]


