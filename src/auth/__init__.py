import requests
from flask import Blueprint, current_app, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from src.common.const import (
    github_api_url,
    github_base_url,
    github_client_id,
    github_client_secret,
)
from src.common.db import db

from .models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    return redirect(
        f"{github_base_url}/login/oauth/authorize?client_id={current_app.config[github_client_id]}&scope=repo,public_repo"
    )


@auth_bp.route("/callback")
def github_callback():
    code = request.args.get("code")

    response = requests.post(
        f"{github_base_url}/login/oauth/access_token",
        data={
            "client_id": current_app.config[github_client_id],
            "client_secret": current_app.config[github_client_secret],
            "code": code,
        },
    )

    access_token = response.json().get("access_token")
    user_data = requests.get(
        f"{github_api_url}/user", headers={"Authorization": f"token {access_token}"}
    ).json()

    user = db.session.get(User, user_data["id"])

    if not user:
        user = User(
            github_id=user_data["id"],
            username=user_data["login"],
            access_token=access_token,
            profile_url=f"{github_base_url}/{user_data["login"]}",
        )
        db.session.add(user)
    else:
        user.access_token = access_token
    db.session.commit()
    login_user(user)
    return redirect(url_for("dashboard.profile"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))
