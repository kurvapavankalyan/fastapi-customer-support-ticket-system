# Customer Support Ticket API

A REST API for customer registration, authentication, and support-ticket
management. Customers can create and manage their own tickets. Administrators
can review customers and tickets, update ticket details, and delete tickets.

The API is built with FastAPI. It uses SQLAlchemy for database access, Pydantic
for request validation, bcrypt for password hashing, and JWT bearer tokens for
authentication. SQLite is the default database in the example configuration;
PostgreSQL is also supported through the installed PostgreSQL driver.

## Project structure

```text
support/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── _types.py       # Shared database-session type
│   │   ├── auth.py         # Registration and login
│   │   ├── client.py       # Customer profile and tickets
│   │   └── admin.py        # Admin customer and ticket operations
│   ├── __init__.py
│   ├── database.py         # Database engine and sessions
│   ├── dependencies.py     # Authentication and authorization
│   ├── main.py             # Creates the FastAPI app and loads routers
│   ├── models.py           # Customer and ticket database tables
│   ├── schemas.py          # Validated API request/response shapes
│   └── security.py         # Password and JWT helpers
├── .env                    # Local settings; ignored by Git
├── .env.example            # Safe example settings
├── .gitignore
├── requirements.txt
└── README.md
```

The `.venv/`, `__pycache__/`, and `.git/` directories are created locally and
are intentionally omitted from this project overview.

## Requirements

- Python 3.10 or later
- pip

## Setup on Windows

Run these commands from the `support` directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks virtual-environment activation, you can run the
environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Edit `.env` and set `SECRET_KEY` to a long, private random value. `DATABASE_URL`
can be left as the example SQLite URL for local development:

```dotenv
DATABASE_URL=sqlite:///./support.db
SECRET_KEY=replace-this-with-a-long-random-secret
```

The SQLite database file is created automatically when the app starts. Keep
`.env` private; commit `.env.example`, not `.env`.

## Run the API

From the `support` directory:

```powershell
uvicorn app.main:app --reload
```

If your terminal is inside the `app` directory, use:

```powershell
uvicorn main:app --reload
```

When the server starts, open:

- Interactive API documentation: <http://127.0.0.1:8000/docs>
- Alternative API documentation: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/>

## Main endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/app/register` | Register a customer |
| POST | `/app/client/token` | Log in and get a bearer token |
| GET | `/app/client/profile` | View the authenticated customer's profile |
| POST | `/app/client/tickets` | Create a support ticket |
| GET | `/app/client/tickets` | List the authenticated customer's tickets |
| GET | `/app/client/tickets/{ticket_id}` | View one of the customer's tickets |
| PATCH | `/app/client/tickets/{ticket_id}` | Update one of the customer's tickets |
| GET | `/app/admin/customers` | List customers (admin only) |
| GET | `/app/admin/tickets` | List all tickets (admin only) |
| PATCH | `/app/admin/tickets/{ticket_id}` | Update ticket details (admin only) |
| DELETE | `/app/admin/tickets/{ticket_id}` | Delete a ticket (admin only) |

## Using authentication in Swagger

1. Register a customer using `POST /app/register`.
2. Click **Authorize** in `/docs`.
3. Enter the customer's email in the **username** field and their password.
4. Swagger sends these credentials to `/app/client/token` and uses the returned
   bearer token for protected customer endpoints.

The login form's field is named `username` by the OAuth2 standard; enter the
email address there.

Admin endpoints require a valid token for a customer whose role is `Admin`.

## Development notes

- Passwords are stored as bcrypt hashes, not plaintext.
- Access tokens are JWT bearer tokens with a 30-minute expiration.
- Database tables are created automatically at application startup.
- The default development server uses auto-reload. Do not expose it directly
  to the public internet in production.
