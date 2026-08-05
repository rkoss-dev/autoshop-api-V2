# **Mechanic Shop API**

A robust RESTful API built with Flask to manage the daily operations of a mechanic shop. This application handles customer registration, authentication, mechanic assignments, service ticket tracking, and inventory management.

## **Features**

- **User Authentication:** Secure customer registration and login using JWT (JSON Web Tokens) and secure password hashing.
- **Customer Management:** Paginated retrieval, updating, and deletion of customer profiles.
- **Mechanic Tracking:** Manage mechanic records and track top-performing mechanics, optimized with SQLAlchemy queries and caching.
- **Service Tickets:** Create and manage repair tickets, link vehicles (by VIN), assign/remove mechanics, and attach inventory parts to specific tickets.
- **Inventory Management:** Full CRUD (Create, Read, Update, Delete) operations for shop parts and pricing with paginated results.
- **Security & Performance:** Incorporates rate limiting to prevent spam and caching to speed up frequent database queries.

## **Technologies Used**

- **Framework:** Flask
- **Database & ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Serialization & Validation:** Marshmallow (Flask-Marshmallow)
- **Authentication:** python-jose (JWT), Werkzeug (Password Hashing)
- **Performance:** Flask-Caching, Flask-Limiter
- **Environment Management:** python-dotenv
- **Package Management:** uv

## **Prerequisites**

Before running this project, ensure you have the following installed:

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (An extremely fast Python package installer and resolver)

## **Installation & Setup**

**1\. Clone the repository**

git clone https://github.com/your-username/mechanic-shop-api.git  
cd mechanic-shop-api

**2\. Create a virtual environment with uv**

uv venv

**3\. Activate the virtual environment**

- On Windows: .venv\\Scripts\\activate
- On macOS/Linux: source .venv/bin/activate

**4\. Install dependencies**

uv pip install \-r requirements.txt

**5\. Set up environment variables**

Create a .env file in the root directory of the project and add the following variables:

FLASK_DEBUG=True  
SECRET_KEY=your_super_secret_jwt_key  
\# Add your database URI here if not using the default SQLite  
\# SQLALCHEMY_DATABASE_URI=sqlite:///shop.db

**6\. Initialize the database and run the server**

python main.py

_The server will start running at http://127.0.0.1:5000._

## **API Endpoints Overview**

Ensure you include the JWT in the Authorization header as Bearer \<your_token\> for protected routes.

### **Customers (/customers)**

| Method | Endpoint             | Description                             | Auth Required |
| :----- | :------------------- | :-------------------------------------- | :------------ |
| POST   | /                    | Register a new customer                 | No            |
| POST   | /login               | Login and receive a JWT                 | No            |
| GET    | /?page=1\&per_page=5 | Get a paginated list of customers       | No            |
| GET    | /my-tickets          | View tickets for the logged-in customer | Yes           |
| PUT    | /\<id\>              | Update customer details                 | Yes           |
| DELETE | /\<id\>              | Delete a customer profile               | Yes           |

### **Mechanics (/mechanics)**

| Method | Endpoint       | Description                           | Auth Required |
| :----- | :------------- | :------------------------------------ | :------------ |
| POST   | /              | Add a new mechanic                    | Yes           |
| GET    | /              | Get all mechanics (Cached)            | No            |
| GET    | /top-mechanics | Get mechanics sorted by ticket volume | No            |
| PUT    | /\<id\>        | Update mechanic details               | Yes           |
| DELETE | /\<id\>        | Delete a mechanic                     | Yes           |

### **Service Tickets (/tickets)**

| Method | Endpoint                                       | Description                            | Auth Required |
| :----- | :--------------------------------------------- | :------------------------------------- | :------------ |
| POST   | /                                              | Create a service ticket (Rate Limited) | Yes           |
| GET    | /                                              | Get all service tickets                | Yes           |
| PUT    | /\<ticket_id\>/assign-mechanic/\<mechanic_id\> | Assign a mechanic to a ticket          | Yes           |
| PUT    | /\<ticket_id\>/remove-mechanic/\<mechanic_id\> | Remove a mechanic from a ticket        | Yes           |
| PUT    | /\<ticket_id\>/edit                            | Batch add/remove mechanics             | Yes           |
| PUT    | /\<ticket_id\>/add-part/\<part_id\>            | Attach a part to a ticket              | Yes           |

### **Inventory (/inventory)**

| Method | Endpoint              | Description                   | Auth Required |
| :----- | :-------------------- | :---------------------------- | :------------ |
| POST   | /                     | Add a new part to inventory   | Yes           |
| GET    | /?page=1\&per_page=10 | Get a paginated list of parts | No            |
| PUT    | /\<id\>               | Update part details           | Yes           |
| DELETE | /\<id\>               | Delete a part                 | Yes           |
