python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
source .env
export $(cat .env)
./api/manage.py makemigrations
./api/manage.py migrate
./api/manage.py runserver 0.0.0.0:8000
