---
title: Postgres (post 1)
feed: show
date: 01-08-2024
---
# 01-08-2024

## Installing Postgres locally and connecting to it from Python

First of all, what is Postgres and why do I care?

Over the course of our working with data, we come across a lot of ways of storing data - cache, in-mem, files, file based databases, SQL databases, NoSQL databases etc. Each option has a specific set of usecases that are best satisfied by said storage mechanism.

Postgres DB is one such storage mechanism - specifically an Open Source, Relational Database.

### *Installation* - 

There are two ways to set up a Postgres instance locally and use it -

a) As a standalone server on your Windows/Linux machine  
b) As a docker container that can be spun up on demand

##### a) As a standalone server on your Windows/Linux machine

The setup process is fairly simple on Windows. You just have to download the EXE installer and walk through the executable’s steps - [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

Note the password you enter for the `postgres` superuser.

One step that is missing from the installer is adding the path to the psql.exe executable in your PATH environment variable .

Now to access the postgres server , fire up a CMD terminal and use -

`psql.exe -U postgres -d postgres -p 5433`

The port flag can be set depending on where your postgres server starts.

##### b) As a docker container that can be spun up on demand

Put the following contents in a file called `docker-compose.yml`

```yaml
services:
  thanos:
    image: postgres
    restart: always
    shm_size: 128mb
    environment:
      POSTGRES_USER: abhi
      POSTGRES_DB: postgres
      POSTGRES_PASSWORD: abhi
    ports:
      - "6543:5432"
```

Breaking this file down, 
- The first line - Based on what service we want to start, we can specify that particular service in this section that is called, well, "service".
	- `thanos` is the name of the container we want to start. While I used a quirky name just so it would stand out, in production, typically this is more relevant to the type of container that we'd want to start . In this case, the container would be better off being called something like `db`.
	- The image we're using is that of `postgres` . We can get a whole host of what images are valid from https://hub.docker.com/ 

Assuming docker has been installed, start the docker container using :
```cmd
C:\Users\Abhiram\Desktop>docker-compose up -d
```

**Resulting in -** 

![Alt Text](/assets/img/postgres-1/docker-compose.png)

**If Docker desktop has been installed, you might even be able to see its creation there -** 

![Alt Text](/assets/img/postgres-1/docker-desktop.png)

### *Connecting to Postgres from Python* - 

- First, create a virtual environment using `virtualenv` (or `conda` or `uv` etc.) because we never pollute the global python environment with additional, specific-use packages
- Activate this virtual environment
- Install the psycopg2-binary package using `pip install psycopg2-binary`
- Test the postgres connection and the creation of the postgres container using this [code snippet](https://github.com/everythingpython/experiments/blob/main/llms/litellm_tracking/util_testers/postgres_connection_tester.py) 

```python
import psycopg2
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up argument parsing
parser = argparse.ArgumentParser(description='Connect to PostgreSQL database and get version.')
parser.add_argument('--dbname', type=str, required=True, help='Name of the database')
parser.add_argument('--user', type=str, required=True, help='Username for the database')
parser.add_argument('--password', type=str, required=True, help='Password for the database user')
parser.add_argument('--host', type=str, default='localhost', help='Database host (default: localhost)')
parser.add_argument('--port', type=str, default='6543', help='Database port (default: 6543)')
args = parser.parse_args()

try:
    conn = psycopg2.connect(
        dbname=args.dbname,
        user=args.user,
        password=args.password,
        host=args.host,
        port=args.port
    )     # Define the connection string

    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("SELECT version();")  # Execute a sample query
    db_version = cursor.fetchone()  # Fetch and display the result
    logger.info(f"Database version: {db_version}")

    cursor.close()
    conn.close()

except Exception as error:
    logger.error(f"Error connecting to PostgreSQL database: {error}")
```

Upon execution of this script that is intended to 
a) connect to a postgres instance running on port `6543` with user `abhi`
b) Get the version of postgres running, 

This is the response - 
```cmd
(pgdbenv) C:\Users\Admin\Desktop\postgres>python postgres_connect.py  --dbname postgres --user abhi --password abhi --port 6543
INFO:__main__:Database version: ('PostgreSQL 16.3 (Debian 16.3-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit',)
```


In summary, in this article we've seen how to install postgres locally and connect to it from Python. 
In the next article, we will explore more about Postgres.