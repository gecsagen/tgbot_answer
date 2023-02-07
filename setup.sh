apt update
apt install -y python3.10-venv nginx
python3 -m venv .venv
activate() {
    . .venv/bin/activate
    echo "installing requirements to virtual environment"
    pip install -r requirements.txt
}
activate
python3 manage.py migrate
python3 manage.py collectstatic
