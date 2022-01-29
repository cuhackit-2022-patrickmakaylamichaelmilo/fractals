cd src
poetry run uvicorn app:app --host 0.0.0.0 --port 80 --use-colors --reload --log-level debug
cd ..
