cd src
python3 -m poetry run gunicorn -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker app:app --workers 2
cd ..
