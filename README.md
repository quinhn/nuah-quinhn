## Prepare for deploy:

### Step 1: Git clone
### Step 2: Install lib
- python3 -m venv env
- source env/bin/activate
- pip install -r requirement.txt
### Step 3: Add api info
- .env file
### Step 4: Add allow hosts
- ./front_end/settings.py file
### Step 5: Runserver
- python3 manage.py createsuperuser
- python3 manage.py runserver 

### Docker run
- docker-compose up -d