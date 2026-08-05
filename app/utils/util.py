from datetime import UTC, datetime, timedelta
from functools import wraps

from flask import jsonify, request
from jose import JWTError, jwt

# The secret key is used to sign the token. Never share this!
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"


def encode_token(customer_id):
    """Generates a token valid for 1 hour."""
    payload = {
        "exp": datetime.now(UTC) + timedelta(hours=1),  # Expiration time
        "iat": datetime.now(UTC),  # Issued at time
        "sub": str(customer_id),  # Subject (the user ID)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def token_required(f):
    """A decorator tool to protect specific routes."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 1. Look for the token in the Headers: "Authorization: Bearer "
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        # 2. If no token is found, kick them out
        if not token:
            return jsonify({"message": "Token is missing. Please log in."}), 401

        # 3. Try to decode the token and get the user's ID
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            customer_id = int(payload["sub"])
        except JWTError:
            return jsonify({"message": "Token is invalid or expired."}), 401

        # 4. If successful, pass the customer_id to the route function!
        return f(customer_id, *args, **kwargs)

    return decorated
