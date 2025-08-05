# PayCheck API

A simple credit bill payment API I built to learn FastAPI and practice building real-world applications. It simulates a basic payment system with user authentication, bill management, and transaction processing.

## What it does

This API lets you:
- Create user accounts and log in securely
- View bills for different users
- Process payments for those bills
- Check transaction history
- Run some basic health checks

I built this mainly to get comfortable with FastAPI, JWT authentication, and database operations. It's not meant for real financial transactions - just a learning project!

## Getting started

### Prerequisites
You'll need Python 3.11+ and pip installed on your machine.

### Setup

1. **Clone and navigate to the project**
   ```bash
   git clone <your-repo-url>
   cd paycheck
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

That's it! The API will be running at `http://localhost:8000`. You can check out the interactive docs at `http://localhost:8000/docs` to see all the available endpoints.

## How to use the API

### Authentication
First, you'll need to log in to get a token:

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "user_1", "password": "pass123"}'
```

This will give you a JWT token. Use it in the `Authorization` header for other requests:
```
Authorization: Bearer <your-token-here>
```

### Main endpoints

- `GET /users` - List all users (no auth needed)
- `GET /bills/{user_id}` - Get bills for a specific user
- `POST /pay` - Process a payment
- `GET /transactions/{user_id}` - View transaction history
- `GET /health` - Check if the API is running

## Testing

I've included some basic tests to make sure everything works:

```bash
# Run all tests
pytest

# Run with more details
pytest -v
```

The tests cover the main functionality - authentication, protected endpoints, and payment processing.

## Database

The app uses SQLite for simplicity. The database file (`paycheck.db`) gets created automatically when you first run the app. The schema includes:

- **Users**: user_id, name, hashed_password
- **Bills**: bill_id, amount, status, user_id  
- **Transactions**: transaction_id, amount, status, user_id, bill_id

## Docker (optional)

If you prefer using Docker:

```bash
# Build the image
docker build -t paycheck-api .

# Run it
docker run -p 8000:8000 paycheck-api
```

## Project structure

```
paycheck/
├── app.py              # Main FastAPI app
├── auth.py             # JWT authentication logic
├── database.py         # Database setup
├── models.py           # SQLAlchemy models
├── requirements.txt    # Dependencies
├── tests/
│   └── test_api.py     # Tests
└── README.md           # This file
```

## What I learned building this

- How to structure a FastAPI application
- JWT authentication implementation
- Database operations with SQLAlchemy
- Writing tests for APIs
- Basic security practices (password hashing, token expiration)

## Notes

- This is a learning project, not for production use
- The secret key in `auth.py` should be changed for any real deployment
- SQLite is fine for development but you'd want PostgreSQL/MySQL for production

Feel free to fork this and experiment with it! Let me know if you run into any issues or have questions.
