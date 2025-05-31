# Run Flask App
```
cd backend
python app.py
```

# Celery commands
```
cd backend
// Worker
celery -A celery_app.celery worker --loglevel=info --pool=solo
// beat
celery -A celery_app.celery beat --loglevel=info
```

# Run Mailhog
```
cd backend
$HOME/go/bin/MailHog
```

# Run redis
```
cd backend
redis-cli
```

# Run Frontend
```
cd frontend
npm install...
```
