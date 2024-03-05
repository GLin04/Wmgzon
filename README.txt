Make sure docker is installed

Step 1:
cd to directory /Wmgzon

Step 2: Build the Docker image
docker build -t wmgzon-app .

# Step 3: Run the Docker container
docker run -p 3000:3000 wmgzon-app

# Step 4: Go to http://127.0.0.1:3000 on your web browser


-------------------------- Additional Info --------------------------
Use main branch if cloning from git


Default admin account:

Email: admin@admin
Password: admin


To run tests:
pip install pytest
Run test command:
python -m pytest

In case that database is locked, restart the application.
