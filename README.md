# Setup

1. Clone repo locally
2. Create PostgreSQL database locally named 'openpair'
3. `npm install`
4. Create .env file in root project directory
5. Write the following in the .env file\
    S3_API_KEY=[your api key]\
    S3_SECRET_KEY=[your secret key]\
    DJANGO_SECRET_KEY=[random hash of your choice]\
    SERVER_SESSION_SECRET=[random hash of your choice]\
    LOCAL_DATABASE_URL=openpair\
    DATABASE_NAME=openpair\
    DATABASE_USER=postgres
6. Create your virtual environment using python 3.9 (see below for making one in conda)
7. Activate your virtual environment
8. While in project root directory `pip install -r requirements.txt`


Good to go. Happy coding.

-J

<center>
    <img src="https://8bitlogo.s3.us-east-2.amazonaws.com/8bit+no+background+copy.png" alt="8 bit logo" width="50"/>
</center>
<br/>
<br/>
<br/>

# SOP for pulling an update from git

1. Make sure your virtual environment is activated
2. `git pull origin main`
3. `npm install` - Installs new javascript packages
4. `pip install -r requirements.txt` - Installs/updates python packages

<br/>

# Before submiting a new PR

1. Make sure your virtual environment is activated
2. `pip freeze > requirements.txt` - updates requirements.txt with any packages you added
3. `git commit`
4. `git push origin [your branch]`
5. Submit PR

<br/>

# Creating local python virtual environment (using conda)

**Python version: 3.9**
1. `cd` into root directory for project cloned locally
2. `conda create --name openpair python=3.9`
3. `conda activate openpair`
4. `pip install -r requirements.txt`