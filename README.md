# todo-app

## Preparation

### frontend

```bash
cd frontend
npm run build
```

### backend

```bash
cd backend
pipenv install
```

## How to run

```bash
cd backend
pipenv run uwsgi --ini uwsgi.ini
```

Access to `localhost:5000`
