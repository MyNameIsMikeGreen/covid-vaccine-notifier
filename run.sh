VENV_DIR=venv
if [[ ! -d "$VENV_DIR" ]]; then
    echo "$VENV_DIR directory not detected. Creating virtual environment..."
    virtualenv ${VENV_DIR}
fi
source venv/bin/activate
pip install -r requirements.txt
python main.py
deactivate
