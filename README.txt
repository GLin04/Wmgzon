Make sure docker is downloaded


Step 1: Build the Docker image
docker build -t wmgzon-app .

# Step 2: Run the Docker container
docker run -p 3000:3000 wmgzon-app

# Step 3: Go to http://127.0.0.1:3000 on your web browser


-------------------------- Additional Info --------------------------

Default admin account:

Email: admin@admin
Password: admin


To run tests:
pip install pytest
Run test command:
python -m pytest

In case that database is locked, restart the application.