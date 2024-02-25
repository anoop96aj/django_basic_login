Basic authentication api using Django

Steps to configure:
1. create venv using requirements.txt.
2. set below env-variables after activating env:
export CLIENT_ID=""
export CLIENT_SECRET=""
export DEFAULT_REGION_NAME="ap-southeast-2"
export DB_PORT=""
export DB_HOST=""
export DB_PASSWORD=""
export DB_USER=""
export DB_NAME=""
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver 
