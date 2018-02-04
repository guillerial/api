python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .env
export $(cat .env)
./api/manage.py migrate
./api/manage.py runserver 0.0.0.0:8000
