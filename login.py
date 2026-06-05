from datetime import datetime, timedelta
from flask import (
    Blueprint,
    jsonify,
    request
)
from werkzeug.security import (
    check_password_hash
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
from extensions import (
    db,
    limiter
)
from auth.model import (
    User,
    TokenBlocklist
)
login_bp = Blueprint(
    "login",
    __name__
)
MAX_FAILED_ATTEMPTS = 5
LOCK_TIME_MINUTES = 30
@login_bp.route(
    "/login",
    methods=["POST"]
)
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request"
        }), 400
    email = data.get(
        "email",
        ""
    ).strip().lower()
    password = data.get(
        "password",
        ""
    )
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 400
    user = User.query.filter_by(
        email=email
    ).first()
    invalid_response = (
        jsonify({
            "success": False,
            "message": "Invalid credentials"
        }),
        401
    )
    if not user:
        return invalid_response
    if (
        user.locked_until
        and
        user.locked_until > datetime.utcnow()
    ):
        return jsonify({
            "success": False,
            "message":
            "Account temporarily locked"
        }), 403
    if not check_password_hash(
        user.password_hash,
        password
    ):
        user.failed_login_attempts += 1
        if (
            user.failed_login_attempts
            >= MAX_FAILED_ATTEMPTS
        ):
            user.locked_until = (
                datetime.utcnow()
                +
                timedelta(
                    minutes=LOCK_TIME_MINUTES
                )
            )
        db.session.commit()
        return invalid_response
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.session.commit()
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "token_version":
            user.refresh_token_version
        }
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={
            "token_version":
            user.refresh_token_version
        }
    )
    return jsonify({
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "username": user.username,
        "email": user.email
    }), 200
@login_bp.route(
    "/refresh",
    methods=["POST"]
)
@jwt_required(refresh=True)
def refresh():
    current_user_id = (
        get_jwt_identity()
    )
    claims = get_jwt()
    user = User.query.get(
        int(current_user_id)
    )
    if not user:
        return jsonify({
            "success": False
        }), 401
    if claims.get(
        "token_version"
    ) != user.refresh_token_version:
        return jsonify({
            "success": False,
            "message":
            "Token revoked"
        }), 401
    new_access_token = (
        create_access_token(
            identity=str(user.id),
            additional_claims={
                "token_version":
                user.refresh_token_version
            }
        )
    )
    return jsonify({
        "access_token":
        new_access_token
    }), 200
@login_bp.route(
    "/logout",
    methods=["POST"]
)
@jwt_required()
def logout():
    jwt_payload = get_jwt()
    jti = jwt_payload["jti"]
    blocked_token = (
        TokenBlocklist(
            jti=jti
        )
    )
    db.session.add(
        blocked_token
    )
    db.session.commit()
    return jsonify({
        "success": True,
        "message":
        "Logged out successfully"
    }), 200
@login_bp.route(
    "/profile",
    methods=["GET"]
)
@jwt_required()
def profile():
    user_id = (
        get_jwt_identity()
    )
    user = User.query.get(
        int(user_id)
    )
    if not user:
        return jsonify({
            "success": False
        }), 404
    return jsonify({
        "id": user.id,
        "username":
        user.username,
        "email":
        user.email,
        "verified":
        user.is_verified
    }), 200