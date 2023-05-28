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


## DB
There's a module *db.py* that contains all the abstractions for working with the MySQL database asynchronously:
- **AsyncSession** - a class that represents an asynchronous session with the database.
- **session_maker** - a function that accepts params for connecting to DB and returns factory for getting sessions.

Example of working with session:

```python
from db import DEFAULT_SESSION_FACTORY

async def some_function():
    async with DEFAULT_SESSION_FACTORY() as session:
        session = await DEFAULT_SESSION_FACTORY()
        async with session.cursor() as cursor:
            await cursor.execute('SELECT * FROM users')
            result = await cursor.fetchall()
            session.close()  # don't forget to close the session
            return result
```

### Unit of work
There's a module *services.unit_of_work.py* that contains all the logic for working with the database in the context of a single transaction:
- **AsyncUnitOfWork** - an abstract class that represents an asynchronous unit of work.
- **MySQLAsyncUnitOfWork** - an abstract class that represents an asynchronous unit of work for MySQL database.

Example of creating custom unit of work:

```python
from services.unit_of_work import MySQLAsyncUnitOfWork
from auth.repository import MySQLUserRepository

class MySQLAsyncUserUnitOfWork(MySQLAsyncUnitOfWork):
        users: MySQLUserRepository

        async def __aenter__(self):
            self.session = await self.session_factory()
            self.users = MySQLUserRepository(self.session)
            await super().__aenter__()
```

Example of working with unit of work:

```python
from domain.user import User
from auth.unit_of_work import MySQLAsyncUserUnitOfWork

async def some_function(user: User):
    async with MySQLAsyncUserUnitOfWork() as uow:
        await uow.users.create_user(user, 'hashed_password')
        await uow.commit()
```
