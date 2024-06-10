# Setup

1. Clone repo locally
2. Create PostgreSQL database locally
3. `npm install`
4. Create .env file in root project directory
5. In .env write `SERVER_SESSION_SECRET = [Random hash of your choice]`
6. In .env write `LOCAL_DATABASE_URL = [Name your local database]`

Good to go. Happy coding.

-J

<center>
    <img src="https://8bitlogo.s3.us-east-2.amazonaws.com/8bit+no+background+copy.png" alt="8 bit logo" width="50"/>
</center>


# Creating local python virtual environment (using conda)

## Python version: 3.9.1
1. `cd` into root directory for project cloned locally
2. `conda create --name openpair python=3.9.1`
3. `conda activate openpair`
4. `pip install -r requirements.txt`

If `requirements.txt` is updated, with the openpair environment activated use the `pip install -r requirements.txt` again and 
the environment will update the packages appropriately.
