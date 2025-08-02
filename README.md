# PayCheck API v2

A mock credit bill payment simulation API built with FastAPI, featuring real database operations, JWT authentication, and comprehensive testing.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **JWT Authentication**: Secure token-based authentication system
- **SQLAlchemy ORM**: Database abstraction layer with SQLite backend
- **Pydantic Models**: Data validation and serialization
- **Comprehensive Testing**: Unit tests with pytest and FastAPI TestClient
- **Docker Support**: Containerized deployment
- **Load Testing**: Locust integration for performance testing
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 📋 Prerequisites

- Python 3.11+
- pip (Python package installer)
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd paycheck
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The database will be automatically created when you first run the application. You can also seed it with test data:

```bash
python seed.py
```

## 🚀 Running the Application

### Development Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

### Using Docker

```bash
# Build the Docker image
docker build -t paycheck-api .

# Run the container
docker run -p 8000:8000 paycheck-api
```

## 📚 API Endpoints

### Authentication

#### POST `/login`
Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "username": "user_1",
  "password": "pass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Users

#### GET `/users`
List all users (no authentication required).

**Response:**
```json
[
  {
    "user_id": "user_1",
    "name": "Pradyumna"
  }
]
```

### Bills

#### GET `/bills/{user_id}`
Get bills for a specific user (requires authentication).

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
[
  {
    "bill_id": "bill_101",
    "amount": 100.0,
    "status": "DUE"
  }
]
```

### Payments

#### POST `/pay`
Process a payment for a bill (requires authentication).

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Request Body:**
```json
{
  "user_id": "user_1",
  "bill_id": "bill_101",
  "amount": 100.0
}
```

**Response:**
```json
{
  "transaction_id": "txn_abc123",
  "amount": 100.0,
  "status": "SUCCESS"
}
```

### Transactions

#### GET `/transactions/{user_id}`
Get transaction history for a user (requires authentication).

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
[
  {
    "transaction_id": "txn_abc123",
    "amount": 100.0,
    "status": "SUCCESS"
  }
]
```

### Monitoring

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: Use the `/login` endpoint with username and password
2. **Token**: Include the received token in the `Authorization` header
3. **Format**: `Authorization: Bearer <your-jwt-token>`

**Security Features:**
- Password hashing with bcrypt
- JWT token expiration (30 minutes)
- User authorization checks
- Secure password verification

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

### Test Coverage

The test suite covers:
- ✅ Authentication (login success/failure)
- ✅ Protected endpoints (with/without authentication)
- ✅ Authorization (user access control)
- ✅ Bill retrieval
- ✅ Payment processing
- ✅ Transaction history

### Load Testing

The project includes Locust for load testing:

```bash
# Install Locust (if not already installed)
pip install locust

# Run load tests
locust -f locustfile.py
```

Then visit http://localhost:8089 to access the Locust web interface.

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `user_id` (Unique identifier)
- `name` (User's name)
- `hashed_password` (Encrypted password)

### Bills Table
- `id` (Primary Key)
- `bill_id` (Unique bill identifier)
- `amount` (Bill amount)
- `status` (DUE/PAID)
- `user_id` (Foreign key to users)

### Transactions Table
- `id` (Primary Key)
- `transaction_id` (Unique transaction identifier)
- `amount` (Transaction amount)
- `status` (SUCCESS/FAILED)
- `user_id` (Foreign key to users)
- `bill_id` (Foreign key to bills)

## 🔧 Configuration

### Environment Variables

Create a `.env` file for environment-specific configuration:

```env
SECRET_KEY=your-super-secret-key-change-me
DATABASE_URL=sqlite:///./paycheck.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Security Notes

⚠️ **Important**: Change the default `SECRET_KEY` in `auth.py` before deploying to production.

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t paycheck-api .

# Run container
docker run -d -p 8000:8000 --name paycheck-api paycheck-api

# Stop container
docker stop paycheck-api
```

### Production Considerations

1. **Database**: Use a production database (PostgreSQL, MySQL) instead of SQLite
2. **Security**: Change default secret keys and use environment variables
3. **HTTPS**: Use a reverse proxy (nginx) with SSL certificates
4. **Monitoring**: Add logging and monitoring solutions
5. **Backup**: Implement database backup strategies

## 📁 Project Structure

```
paycheck/
├── app.py              # Main FastAPI application
├── auth.py             # Authentication and JWT handling
├── database.py         # Database configuration
├── models.py           # SQLAlchemy models
├── seed.py             # Database seeding script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore       # Docker ignore file
├── .gitignore          # Git ignore file
├── tests/
│   └── test_api.py     # API tests
├── venv/               # Virtual environment
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API Documentation](http://localhost:8000/docs) when running locally
2. Review the test files for usage examples
3. Open an issue on the repository

## 🔄 Version History

- **v2.0.0**: Added JWT authentication, improved security, comprehensive testing
- **v1.0.0**: Initial release with basic CRUD operations

---

**Note**: This is a mock/simulation API for educational and testing purposes. Do not use for real financial transactions.
