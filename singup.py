from flask import (Blueprint, request, jsonify )
from flask_wtf import FlaskForm
from wtforms import ( StringField, PasswordField)
from wtforms.validators import ( DataRequired, Email, Length, Regexp )
from werkzeug.security import ( generate_password_hash )
from extensions import limiter
from extensions import db
from auth.model import User


signup_bp = Blueprint(
    "signup",
    __name__
)


class SignupForm(FlaskForm):

    username = StringField(
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message="Invalid username"
            )
        ]
    )

    email = StringField(
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        validators=[
            DataRequired(),
            Length(min=12, max=128)
        ]
    )


def validate_password_strength(password):

    has_upper = any(c.isupper() for c in password)

    has_lower = any(c.islower() for c in password)

    has_digit = any(c.isdigit() for c in password)

    has_special = any(
        not c.isalnum()
        for c in password
    )

    return all([
        has_upper,
        has_lower,
        has_digit,
        has_special
    ])


@signup_bp.route(
    "/signup",
    methods=["POST"]
)
@limiter.limit("5 per minute")
def signup():

    form = SignupForm()

    if not form.validate():

        return jsonify({
            "success": False,
            "message": "Invalid input"
        }), 400

    username = form.username.data.strip()

    email = form.email.data.lower().strip()

    password = form.password.data

    if not validate_password_strength(
        password
    ):
        return jsonify({
            "success": False,
            "message":
            "Password must contain uppercase, lowercase, digit and special character"
        }), 400

    existing_user = User.query.filter(
        (
            User.email == email
        ) |
        (
            User.username == username
        )
    ).first()

    if existing_user:

        return jsonify({
            "success": False,
            "message":
            "User already exists"
        }), 409

    password_hash = generate_password_hash(
        password,
        method="scrypt"
    )

    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
        "Account created successfully"
    }), 201