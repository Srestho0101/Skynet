#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/storage/shared/Skynet
# Only activate venv if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
