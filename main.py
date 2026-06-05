# import os
# from datetime import timedelta
# from dotenv import load_dotenv
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from flask_wtf.csrf import CSRFProtect
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# load_dotenv()
# from extensions import (
#     db,
#     jwt,
#     csrf,
#     limiter
# )
# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#     app.config["SQLALCHEMY_DATABASE_URI"] = (
#         f"postgresql://{os.getenv('DB_USER')}:"
#         f"{os.getenv('DB_PASSWORD')}@"
#         f"{os.getenv('DB_HOST')}:"
#         f"{os.getenv('DB_PORT')}/"
#         f"{os.getenv('DB_NAME')}"
#     )
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
#     app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
#     app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
#     app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
#     app.config["JWT_COOKIE_SECURE"] = True
#     app.config["JWT_COOKIE_HTTPONLY"] = True
#     app.config["JWT_COOKIE_SAMESITE"] = "Strict"
#     app.config["JWT_COOKIE_CSRF_PROTECT"] = True
#     app.config["SESSION_COOKIE_SECURE"] = True
#     app.config["SESSION_COOKIE_HTTPONLY"] = True
#     app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
#     app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
#     db.init_app(app)
#     jwt.init_app(app)
#     csrf.init_app(app)
#     limiter.init_app(app)
#     @app.after_request
#     def add_security_headers(response):
#         response.headers["X-Frame-Options"] = "DENY"
#         response.headers["X-Content-Type-Options"] = "nosniff"
#         response.headers["Referrer-Policy"] = (
#             "strict-origin-when-cross-origin"
#         )
#         response.headers["Permissions-Policy"] = (
#             "camera=(), microphone=(), geolocation=()"
#         )
#         response.headers["Cache-Control"] = (
#             "no-store, no-cache, must-revalidate"
#         )
#         response.headers["Pragma"] = "no-cache"
#         response.headers["Content-Security-Policy"] = (
#             "default-src 'self'; "
#             "img-src 'self' data:; "
#             "style-src 'self' 'unsafe-inline'; "
#             "script-src 'self';"
#         )
#         return response
#     @jwt.token_in_blocklist_loader
#     def check_if_token_revoked(jwt_header, jwt_payload):
#         from auth.model import TokenBlocklist
#         jti = jwt_payload["jti"]
#         token = TokenBlocklist.query.filter_by(
#             jti=jti
#         ).first()
#         return token is not None
#     from auth.model import User
#     from auth.model import TokenBlocklist
#     from auth.singup import signup_bp
#     from auth.login import login_bp
#     app.register_blueprint(signup_bp)
#     app.register_blueprint(login_bp)
#     return app
from datetime import timedelta
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

from extensions import (
    db,
    jwt,
    csrf,
    limiter
)

def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Environment
    # -----------------------------
    is_production = (
        os.getenv("FLASK_ENV") == "production"
    )

    # -----------------------------
    # CORS
    # -----------------------------
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000"
                ]
            }
        }
    )

    # -----------------------------
    # Flask Config
    # -----------------------------
    app.config["SECRET_KEY"] = (
        os.getenv("SECRET_KEY")
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # -----------------------------
    # JWT
    # -----------------------------
    app.config["JWT_SECRET_KEY"] = (
        os.getenv("JWT_SECRET_KEY")
    )

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = (
        timedelta(minutes=15)
    )

    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = (
        timedelta(days=7)
    )

    app.config["JWT_TOKEN_LOCATION"] = [
        "cookies"
    ]

    app.config["JWT_COOKIE_HTTPONLY"] = True

    app.config["JWT_COOKIE_SECURE"] = (
        is_production
    )

    app.config["JWT_COOKIE_SAMESITE"] = (
        "Strict"
    )

    app.config["JWT_COOKIE_CSRF_PROTECT"] = True

    # -----------------------------
    # Session Security
    # -----------------------------
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    app.config["SESSION_COOKIE_SECURE"] = (
        is_production
    )

    app.config["SESSION_COOKIE_SAMESITE"] = (
        "Strict"
    )

    # -----------------------------
    # Upload Limits
    # -----------------------------
    app.config["MAX_CONTENT_LENGTH"] = (
        16 * 1024 * 1024
    )

    # -----------------------------
    # Extensions
    # -----------------------------
    db.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    @app.route("/test")
    def test():
        return {"message": "working"}, 200
    # -----------------------------
    # Security Headers
    # -----------------------------
    @app.after_request
    def add_security_headers(response):

        response.headers[
            "X-Frame-Options"
        ] = "DENY"

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"

        response.headers[
            "Permissions-Policy"
        ] = (
            "camera=(), microphone=(), geolocation=()"
        )

        response.headers[
            "Cache-Control"
        ] = (
            "no-store, no-cache, must-revalidate"
        )

        response.headers[
            "Pragma"
        ] = "no-cache"

        response.headers[
            "Content-Security-Policy"
        ] = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self';"
        )

        return response

    # -----------------------------
    # JWT Blocklist
    # -----------------------------
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(
        jwt_header,
        jwt_payload
    ):
        from auth.model import (
            TokenBlocklist
        )

        jti = jwt_payload["jti"]

        token = (
            TokenBlocklist.query
            .filter_by(jti=jti)
            .first()
        )

        return token is not None

    # -----------------------------
    # Import Models
    # -----------------------------
    from auth.model import User
    from auth.model import TokenBlocklist

    # -----------------------------
    # Blueprints
    # -----------------------------
    from auth.singup import signup_bp
    from auth.login import login_bp

    app.register_blueprint(signup_bp)
    app.register_blueprint(login_bp)

    return app