# Rental App
## About
An app for renters to review the properties they have resided in.  
An app for landlords to review the renters that have resided in their properties.

## Development
### Local Development
Create a virtual environment
```bash
python3 -m venv venv && \
source venv/bin/activate
```

Spin the service up and down using the Makefile:  
start: `make local_build`  
setup local db: `make local_setup`  
stop: `make local_down`  
nuke it all: `make remove_images`  
