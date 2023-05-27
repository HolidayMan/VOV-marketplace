# VOV-marketplace


## Requirements
Python 3.11.2
Docker
Docker-compose

---

## Installation
Create a virtual environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```

If you use PyCharm:
1. Open settings
2. Go to Project: VOV-marketplace -> Python Interpreter
3. Click on the gear icon and select Add
4. Create a new environment using Virtualenv Environment
5. Select Base interpreter: python3.11.2
6. Click OK

Install the requirements
```bash
pip install -r requirements.txt
```

## Running the app
Configurations for starting the app must be already configured. If not, please contact @let45fc

Just press the green button in PyCharm or run the following commands in the terminal
```bash
docker-compose up -d
uvicorn main:app --reload
```

---

## Project structure
TODO

---

## Filters
There are some custom filters that can be used in templates

### make_static
Adds the static path to the file

Example: `{{ 'images/image.png'|make_static }}`


### make_media
Adds the media path to the file

Example: `{{ '/images/image.png'|make_media }}`

---

## Auth
There's a package *auth* that contains all the logic for authentication and authorization:
- logic.py - contains all the logic for managing passwords and tokens. 
- models.py - contains all the data models.
- repository.py - contains all the logic for working with the database.
- exceptions.py - contains all the exceptions that can be raised during the authentication process.
