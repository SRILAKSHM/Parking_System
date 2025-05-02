# Parking Management System 🚗

A **FastAPI** backend project for managing parking slots, bookings, user authentication, and feedback collection.

## Features

* **Authentication & User Management**

  * JWT-based login and registration
  * User roles: `user` and `admin`
* **Parking Slot Management**

  * Admin can add, update, delete slots
  * Users can view available slots
* **Booking Management**

  * Users can create, view, and cancel their bookings
* **User Feedback**

  * Users can submit feedback linked to bookings or slots
* **Administrative Tools**

  * Bulk operations (add/update slots)
  * Maintenance mode for slots/lot
* **Testing**

  * > 70% API test coverage using `pytest`


## Technology Stack

* **Backend**: FastAPI
* **ORM**: SQLAlchemy
* **Database**: SQLite
* **Authentication**: JWT (JSON Web Token)
* **Validation**: Pydantic
* **Testing**: pytest + FastAPI's TestClient


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/parking-management-system.git
cd parking-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# or
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

*No migrations needed for SQLite setup, the database will auto-create.*

### 5. Start the Server

```bash
uvicorn main:app --reload
```

* Server will be running at `http://127.0.0.1:8000`

---

## API Documentation

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can also import the provided **Postman Collection** (`postman_collection.json`) for easy API testing.

---

## Environment Variables

Create a `.env` file (optional) to configure:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./parking.db
```

---

## How to Run Tests

```bash
pytest --cov=.
```

* Ensure the line coverage is **above 70%**.

---

## Project Structure

```text
parking-management-system/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── crud.py
│   ├── auth.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── bookings.py
│   │   ├── slots.py
│   │   ├── feedback.py
│   │   └── admin.py
│   └── utils/
│       └── security.py
├── tests/
│   ├── test_auth.py
│   ├── test_booking.py
│   ├── test_slots.py
│   └── test_feedback.py
├── postman_collection.json
├── requirements.txt
└── README.md
```

---

## Important Notes

* Only **admins** can:

  * Add, update, delete parking slots
  * Perform bulk operations
  * Set maintenance mode
* **Users** can:

  * Book, view, and cancel their parking slots
  * Submit feedback
