# Backend_Traffic_Analyzer (Endpoint Checker)
This application/tool `backend_traffic_analyzer` gathers and aggregates status report from given list of endpoints and writes the aggregated report to STDOUT and to a local log file

##  Package Structure
```
├─- bin
│ ├── __init__.py
│ └── get_app_success_rate.py
├── src
│ ├── __init__.py
│ ├── aggregator.py
│ └── call_endpoint.py
├── test
│ └── test_backend_traffic_analyzer.py
├── Dockerfile
├── README.md
├── servers.txt
└── setup.py
```

## Description of files in Package

The driver code or main script `get_app_success_rate.py` in `bin` directory uses `call_endpoint.py` and `aggregator.py` modules in `src` directory

- `call_endpoint.py` module uses python `urllib.request` to query the endpoint to get the app status report
- `aggregator.py` module aggregates the Success Rate of the Applications by their Versions.
- The file containing list of endpoints is user-input to `get_app_success_rate.py`
- Python's threading module is utilized to concurrently call 25 endpoints in parallel. This number can be tuned as per requirement.

## System Requirements
- A Linux or Unix Host/Machine with Internet Connection (for building docker image) 
- A Docker runtime is installed on the host/machine
	 ```
	 % docker --version
	 Docker version 19.03.13, build 4484c46d9d
	 ```


## Installation/Build Instructions
The project is packaged into a tar archive. Installation steps are as follows:

1. Extract the archive into your home
    `% tar -xvzf backend_traffic_analyzer.tar.gz`

A `backend_traffic_analyzer` directory will be extracted into the folder from where above command is run. 

2.  Enter the `backend_traffic_analyzer` directory using `cd`
3. Ensure the contents of the `backend_traffic_analyzer` directory
    ```
    % ls
    Dockerfile  README.md  bin  servers.txt  setup.py  src  test
    ```
5. Build the `backend_traffic_analyzer` docker image
     `docker build -t backend_traffic_analyzer .`
6. Check if docker image is available
     ```
     % docker images
     REPOSITORY		TAG 	IMAGE ID  		CREATED 		SIZE
     backend_traffic_analyzer latest  3632cab0ba0a  14 minutes ago  178MB
     ```
    
7. Run the docker image
    `% docker run -it backend_traffic_analyzer:latest /bin/bash`
    The above command will give you interactive shell (bash) and pseudo-tty to the container.
    `root@760a2db24e2e:/opt/backend_traffic_analyzer#`
    
8. Ensure that the DNS settings or `/etc/hosts` are set-up correctly. If required make use of `vi` which is available in this container. This is to ensure that the endpoints are resolved when the code is run.
    https://docs.docker.com/config/containers/container-networking/

## Running the Tool/Code
Following is the Usage for the tool
```
root@760a2db24e2e:/opt/backend_traffic_analyzer# traffic-analyze --help
usage: traffic-checker [-h] -f FILE

optional arguments:
  -h, --help  show this help message and exit
  -f FILE, --file FILE  File containing list of endpoints (example: servers.txt)
```

When inside the container, run the tool executing following command.
```
root@760a2db24e2e:/opt/backend_traffic_analyzer# traffic-analyze --file servers.txt
2021-08-06 12:35:23,205 - root - INFO - Success_rate by App and Version
		Cache1
			version=0.0.2,success_rate_%=27.22
		Database1
			version=1.1.0,success_rate_%=10.62
			version=0.1.0,success_rate_%=76.85
		Webapp1
			version=1.2.2,success_rate_%=50.91
```
The above output is also written to a log file `/var/log/backend_traffic_analyzer/get_app_success_rate.log`
