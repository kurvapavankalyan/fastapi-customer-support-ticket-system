# Customer Support Ticket API

## Project structure

```text
support/
├── app/
│   ├── routers/
│   │   ├── _types.py
│   │   ├── auth.py
│   │   ├── client.py
│   │   └── admin.py
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── dependencies.py
├── .env.example
├── requirements.txt
└── README.md
```

## Run the API

Open a terminal in the `support` folder, activate the virtual environment,
install dependencies if needed, then start the server:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and set your database URL and a private
`SECRET_KEY`. Do not share or commit `.env`.

Open `http://127.0.0.1:8000/docs` to try the endpoints.
