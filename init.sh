python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .env
export $(cat .env)
./api/api/manage.py migrate
./api/api/manage.py runserver 0.0.0.0:8000
