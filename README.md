# Rental App
## About
An app for renters to review the properties they have resided in.  
An app for landlords to review the renters that have resided in their properties.

## Development
### Python Virtual Environment
Create a virtual environment
```bash
python3 -m venv .venv
```

Activate venv
```bash
source .venv/bin/activate
```

Deactivate venv
```bash
deactivate
```

### Django
Start server
```bash
docker-compose up
```

Debug
```bash
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
```